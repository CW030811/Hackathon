"""Synthetic scope evidence; never benchmark labels."""
import unittest
from dataclasses import replace
from datetime import timedelta

from agents.rca.contracts import Component, ComponentCatalog
from agents.rca.ranking import prepare_candidates, _same_episode
from tests.m4.helpers import candidate, case, evidence


class ServiceScopeTests(unittest.TestCase):
    def fixtures(self, same_node=False):
        catalog = ComponentCatalog({"shop": Component("shop", "service", service="shop")})
        cs, es = [], []
        for i in range(3):
            pod = f"shop-{i}"
            catalog.components[pod] = Component(pod, "container", node_id="n0" if same_node else f"n{i}", service="shop")
            cs.append(candidate(f"c{i}", pod, eid=f"e{i}"))
            es.append(evidence(f"e{i}", pod))
        return catalog, cs, es

    def test_majority_cross_node_adds_scope_without_erasing_pods(self):
        cat, cs, es = self.fixtures()
        result = prepare_candidates(case(), cs[:2], cat, es)
        scope = next(c for c in result if c.component == "shop")
        self.assertEqual(scope.features["scope.members"], ["shop-0", "shop-1"])
        self.assertEqual(scope.supporting_ids, ["e0", "e1"])
        self.assertEqual(len(result), 3)
        self.assertTrue(_same_episode(scope, cs[0]))

    def test_single_pod_or_single_node_does_not_prove_service_scope(self):
        cat, cs, es = self.fixtures()
        self.assertFalse(any(c.component == "shop" for c in prepare_candidates(case(), cs[:1], cat, es)))
        cat, cs, es = self.fixtures(same_node=True)
        self.assertFalse(any(c.component == "shop" for c in prepare_candidates(case(), cs, cat, es)))

    def test_different_mechanisms_or_times_do_not_aggregate(self):
        cat, cs, es = self.fixtures()
        cs[1].reason = "container memory load"
        cs[2] = replace(cs[2], onset_interval=tuple(t + timedelta(minutes=5) for t in cs[2].onset_interval))
        self.assertFalse(any(c.component == "shop" for c in prepare_candidates(case(), cs, cat, es)))

    def test_unknown_reason_expansion_is_not_service_evidence(self):
        cat, cs, es = self.fixtures()
        for c in cs:
            c.reason = None
        self.assertFalse(any(c.component == "shop" for c in prepare_candidates(case(), cs, cat, es)))

    def test_trace_scope_preserves_unknown_onset_and_weak_subtype(self):
        cat, cs, es = self.fixtures()
        for c in cs:
            c.reason = None
            c.onset_interval = c.onset_estimate = None
            c.features = {"traces.network_family": True, "traces.anomaly_score": 3}
        scopes = [c for c in prepare_candidates(case(), cs, cat, es) if c.component == "shop"]
        self.assertEqual(len(scopes), 4)
        self.assertTrue(all(c.features["m4.weak_reason"] and c.onset_estimate is None and c.onset_interval is None for c in scopes))
