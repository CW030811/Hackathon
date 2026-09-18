"""Build a self-contained replay from a frozen, recorded RCA run; never calls a model."""
import argparse
import csv
import hashlib
import json
from pathlib import Path


def build(run, repo, destination):
    audit = json.loads((run / 'audit.json').read_text())
    summary = json.loads((repo / 'eval/results/workflow-repair-20260917/verification-summary.json').read_text())
    manifest = json.loads((run / 'manifest.json').read_text())
    expected = summary['planned_row_ids']
    predictions = {int(r['row_id']): r for r in csv.DictReader((run / 'predictions.csv').open())}
    assert list(predictions) == expected
    attempts = [json.loads(p.read_text()) for p in (run / 'diagnostics/attempts').glob('*.json')]
    mapping = {int(k): int(v) for a in attempts for k, v in a['invocation_rows'].items()}
    routes = [json.loads(line) for line in (run / 'diagnostics/routes.jsonl').read_text().splitlines()]
    audits = {r['row_id']: r for r in audit['cases']}
    cases = []
    event_fields = ('event', 'stage', 'tool', 'status', 'latency_s', 'candidate_count',
                    'evidence_count', 'coverage', 'question', 'components', 'requested_model',
                    'actual_model', 'reason', 'fallback', 'prompt_tokens', 'completion_tokens',
                    'estimated_cost_usd', 'retained_reservation_usd', 'confidence',
                    'selection_applied', 'interruptions')
    for invocation, row_id in sorted(mapping.items()):
        ledger = json.loads((run / f'diagnostics/evidence/{invocation}.json').read_text())
        decision = ledger['decision']
        by_id = {e['evidence_id']: e for e in ledger['evidence']}
        support = [by_id[x] for x in decision['supporting_ids'] if x in by_id]
        evidence = []
        for e in support[:6]:
            params, values = e['transform_params'], e['values']
            evidence.append({
                'id': e['evidence_id'], 'kind': e['kind'], 'components': e['component_ids'],
                'metric': params.get('kpi_name', params.get('field', e['transform'])),
                'source_files': e['source_files'], 'interval': e['interval'],
                'values': {k: values[k] for k in ('baseline_median', 'window_median', 'window_max',
                           'baseline_n', 'window_n', 'sampling_interval_s', 'strength') if k in values},
                'units': e['units'], 'source_records': e['source_records'][:3],
                'limitations': e['limitations'][:3], 'transform': e['transform'],
            })
        a = audits[row_id]
        cases.append({
            'id': row_id, 'task': a['task'], 'partial': a['partial'], 'strict': a['fully_solved'],
            'wall': a['wall_s'], 'known_cost': a['known_cost_usd'], 'cost': a['cost_usd'],
            'case': ledger['case'], 'workflow': ledger['workflow'],
            'confidence': decision['confidence'], 'answers': decision['answers'],
            'limitations': decision['limitations'], 'stop_reason': decision['stop_reason'],
            'alternatives': decision['alternatives'][:5], 'evidence': evidence,
            'evidence_total': len(ledger['evidence']), 'support_total': len(support),
            'evidence_markdown': (run / f'evidence/{row_id}.md').read_text(),
            'prediction': predictions[row_id]['prediction'],
            'events': [{k: e[k] for k in event_fields if k in e} for e in routes
                       if e['invocation_index'] == invocation],
        })
    assert len(cases) == 20 and sum(c['strict'] for c in cases) == 5
    assert abs(sum(c['partial'] for c in cases)/20 - .346) < 1e-9
    assert sum(c['workflow']['complete'] for c in cases) == 19
    assert sum(e['event']=='request' for c in cases for e in c['events']) == 41
    runtime = {p: h for p, h in manifest['source_hashes'].items() if '/tests/' not in p}
    assert all(hashlib.sha256((repo / p).read_bytes()).hexdigest() == h for p, h in runtime.items())
    payload = {'cases': cases, 'summary': summary, 'by_task': audit['by_task'],
               'source_commit': '97c759682d72832d4f008fdf13b1d1c4f218f03e',
               'submission_commit': 'd5142782de9b841651ab2ae2fcfa83c3a7170925',
               'runtime_files_verified': len(runtime)}
    root = Path(__file__).parent
    encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False).replace('<', '\\u003c')
    chart = (root / 'vendor/chart.umd.min.js').read_text().replace('</script', '<\\/script')
    html = (root / 'template.html').read_text().replace('__CHART_LIBRARY__', chart).replace('__DEMO_DATA__', encoded)
    destination.write_text(html)
    print(json.dumps({'output': str(destination), 'cases': len(cases), 'requests': 41,
                      'bytes': destination.stat().st_size, 'verified_runtime_files': len(runtime)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path(__file__).with_name('index.html'))
    args = parser.parse_args()
    build(args.run, args.repo, args.out)
