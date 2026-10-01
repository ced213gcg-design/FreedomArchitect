from typing import TypedDict
try:
    from langgraph.graph import StateGraph, START, END
except Exception:
    StateGraph = START = END = None

MIT_TRIGGERS = {
    "price","pricing","token","digital asset","settlement","custody",
    "marketplace","incentive","ledger","blockchain","chain","smart contract"
}

class FlowState(TypedDict, total=False):
    text: str
    mit_gate: bool
    stage: str
    final_state: str
    response: str

def mit_required(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in MIT_TRIGGERS)

def _precheck(s: FlowState) -> FlowState:
    s["stage"] = "PRECHECK"
    return s

def _authority(s: FlowState) -> FlowState:
    s["stage"] = "AUTHORITY"
    return s

def _plan(s: FlowState) -> FlowState:
    s["stage"] = "PLAN"
    s["mit_gate"] = mit_required(s.get("text", ""))
    if s["mit_gate"]:
        s["final_state"] = "HOLD"
        s["response"] = "MIT_GATE_ON: complete the mechanism worksheet before economic execution."
    else:
        s["final_state"] = "SAFE"
    return s

def build_graph():
    if StateGraph is None:
        return None
    g = StateGraph(FlowState)
    g.add_node("precheck", _precheck)
    g.add_node("authority", _authority)
    g.add_node("plan", _plan)
    g.add_edge(START, "precheck")
    g.add_edge("precheck", "authority")
    g.add_edge("authority", "plan")
    g.add_edge("plan", END)
    return g.compile()

GRAPH = build_graph()

def analyze(text: str) -> FlowState:
    seed: FlowState = {"text": text}
    if GRAPH is None:
        seed = _precheck(seed)
        seed = _authority(seed)
        return _plan(seed)
    return GRAPH.invoke(seed)