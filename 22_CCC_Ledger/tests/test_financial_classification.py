from importlib import import_module
m=import_module("22_CCC_Ledger.classify_financial_state")

def test_pipeline_not_revenue():
    assert m.classify_financial_state("PIPELINE")["realized_revenue"] is False

def test_invoice_not_revenue():
    assert m.classify_financial_state("INVOICED")["classification"]=="RECEIVABLE_NOT_COLLECTED"

def test_reconciled_commercial_is_realized_but_not_surplus():
    r=m.classify_financial_state("RECONCILED","COMMERCIAL_RECEIPT")
    assert r["realized_revenue"] is True and r["deployable_surplus"] is False

def test_restricted_funding_not_unrestricted_revenue():
    assert m.classify_financial_state("RECONCILED","RESTRICTED_GRANT")["realized_revenue"] is False
