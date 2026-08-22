(function(global){
  const session = (global.crypto && global.crypto.randomUUID) ? global.crypto.randomUUID() : `ccc-${Date.now()}`;

  async function emit(actionType, options={}) {
    const payload = {
      operator_session: session,
      action_type: actionType,
      source_context: options.source_context || document.body.dataset.world || 'CCC_HORIZON',
      target_object: options.target_object || 'ccc-dashboard',
      requested_effect: options.requested_effect || null,
      authority_required: Boolean(options.authority_required),
      state_before: options.state_before || null,
      state_after: options.state_after || null,
      evidence_ref: options.evidence_ref || null,
      run_id: options.run_id || null
    };
    try {
      const response = await fetch('/api/interaction-event', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload)
      });
      return await response.json();
    } catch (error) {
      return {accepted:false, reason:'TELEMETRY_UNAVAILABLE', detail:error.message};
    }
  }

  global.CCCInteraction = {emit, session};
})(window);
