from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]

def _pressure_module():
    path = ROOT / "21_CCC_Orchestra" / "pressure_loss.py"
    spec = importlib.util.spec_from_file_location("ccc_pressure_loss_for_workforce", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def score_worker(worker: dict):
    required = ["Progress", "Evidence", "Compliance", "Resilience", "EconomicValue"]
    if any(worker.get(k) is None for k in required):
        return {"worker": worker.get("id"), "PressureLoss": None, "validation": "UNKNOWN_RUNTIME_EVIDENCE_REQUIRED"}
    out = _pressure_module().calculate({k: worker[k] for k in required})
    return {"worker": worker.get("id"), **out, "validation": "CALCULATED_FROM_PROVIDED_RUNTIME_METRICS"}

def workforce_pressure(workers: list[dict]):
    rows = [score_worker(w) for w in workers]
    scored = [r for r in rows if r.get("PressureLoss") is not None]
    weakest = min(scored, key=lambda r: r["PressureLoss"]) if scored else None
    return {"workers": rows, "system_weakest": weakest, "validation": "NO_INVENTED_METRICS"}
