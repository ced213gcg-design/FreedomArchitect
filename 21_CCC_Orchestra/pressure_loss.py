DIMENSIONS=("Progress","Evidence","Compliance","Resilience","EconomicValue")
def calculate(scores: dict) -> dict:
    missing=[d for d in DIMENSIONS if d not in scores]
    if missing: raise ValueError("missing pressure dimensions: "+", ".join(missing))
    clean={d:max(0,min(100,float(scores[d]))) for d in DIMENSIONS}
    weakest=min(clean,key=clean.get)
    return {"PressureLoss":clean[weakest],"weakest_dimension":weakest,"scores":clean}
