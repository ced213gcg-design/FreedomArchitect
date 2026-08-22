# CCC Drag / Drop Authority

State: **DEFERRED_P1**

Drag/drop is not active in the SOC Live P0 mission.

When implemented later, drag/drop may express a proposed relationship only, such as task -> worker or evidence -> case. The drop event must generate a REQUEST PREVIEW that identifies source, target, expected effect, risk, authority requirement and rollback where applicable.

Consequential drops require confirmation and policy/approval routing. Invalid targets must reject visibly and explain why. No drag/drop operation may bypass Trust Fabric, human approval, Orchestra placement, registered executors or Ledger result recording.
