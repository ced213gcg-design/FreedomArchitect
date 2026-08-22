from pressure_loss import calculate
from release_gate import evaluate as evaluate_release

def evaluate_organ(organ_id, scores, evidence, owner, blocking_dependency, next_action):
    pressure=calculate(scores)
    return {"organ":organ_id,**pressure,"evidence":evidence,"owner":owner,"blocking_dependency":blocking_dependency,"next_action":next_action}
