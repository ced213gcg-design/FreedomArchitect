from importlib import import_module
m=import_module("25_CCC_Exception_Intelligence.fit_score")
def test_missing_evidence_earns_zero_effective_points():
    comps={name:{"score":100,"evidence_refs":["repo://proof"]} for name in m.EMPLOYMENT_WEIGHTS}; comps["Education"]={"score":100,"evidence_refs":[]}; r=m.employment_fit(comps)
    assert r["score"]==90.0 and "Education" in r["missing_evidence_components"]
