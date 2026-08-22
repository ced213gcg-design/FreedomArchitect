from __future__ import annotations

def classify_financial_state(stage: str, financial_class: str="COMMERCIAL_RECEIPT") -> dict:
    """Keep opportunities, claims, cash collection, reconciliation and deployable surplus distinct."""
    stage=str(stage or "").upper()
    cls=str(financial_class or "COMMERCIAL_RECEIPT").upper()
    if cls in {"INTERNAL_SAVINGS","AVOIDED_COST","EFFICIENCY_GAIN"}:
        return {"classification":"ECONOMIC_VALUE_NOT_CASH","realized_revenue":False,"deployable_surplus":False}
    if stage in {"SIGNAL","QUALIFIED","BUILD","FOUNDRY","SALE_READY","PIPELINE"}:
        return {"classification":"OPPORTUNITY_NOT_REVENUE","realized_revenue":False,"deployable_surplus":False}
    if stage=="CONTRACTED":
        return {"classification":"CONTRACTUAL_CLAIM_NOT_COLLECTED","realized_revenue":False,"deployable_surplus":False}
    if stage=="INVOICED":
        return {"classification":"RECEIVABLE_NOT_COLLECTED","realized_revenue":False,"deployable_surplus":False}
    if stage=="COLLECTED":
        return {"classification":"COLLECTED_UNRECONCILED","realized_revenue":False,"deployable_surplus":False}
    if stage=="RECONCILED":
        if cls in {"RESTRICTED_GRANT","RESTRICTED_FUNDING"}:
            return {"classification":"RESTRICTED_FUNDS_RECONCILED","realized_revenue":False,"deployable_surplus":False}
        return {"classification":"REALIZED_REVENUE_RECONCILED","realized_revenue":True,"deployable_surplus":False}
    if stage=="SURPLUS_ELIGIBLE":
        return {"classification":"DEPLOYABLE_SURPLUS_ELIGIBLE","realized_revenue":True,"deployable_surplus":True}
    if stage=="REINVESTED":
        return {"classification":"REINVESTED_CAPITAL","realized_revenue":True,"deployable_surplus":False}
    return {"classification":"UNKNOWN_FINANCIAL_STATE","realized_revenue":False,"deployable_surplus":False}
