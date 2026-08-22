import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; BACK=ROOT/'19_Live_Adaptive_Dashboard'/'backend'; sys.path.insert(0,str(BACK))
from soc_latency import reconcile_latency

def test_latency_is_calculated_for_monotonic_timestamps():
    row={'state':'PASS','trigger_time':'2026-08-22T10:00:00+00:00','source_event_time':'2026-08-22T10:00:00.100000+00:00','detection_time':'2026-08-22T10:00:00.200000+00:00','ledger_time':'2026-08-22T10:00:00.300000+00:00','dashboard_time':'2026-08-22T10:00:00.500000+00:00'}
    out=reconcile_latency(row)
    assert out['clock_skew'] is False and out['end_to_end_ms']==500.0

def test_material_reverse_clock_order_becomes_verify_clock_skew():
    row={'state':'PASS','trigger_time':'2026-08-22T10:00:05+00:00','source_event_time':'2026-08-22T10:00:00+00:00','detection_time':'2026-08-22T10:00:01+00:00','ledger_time':'2026-08-22T10:00:02+00:00','dashboard_time':'2026-08-22T10:00:03+00:00'}
    out=reconcile_latency(row)
    assert out['clock_skew'] is True and out['state']=='VERIFY_CLOCK_SKEW'
    assert out['end_to_end_ms'] is None
