import pandas as pd

def rfm_analysis(sales):
    sales = sales.copy()

    # Ensure order_date is datetime
    sales["order_date"] = pd.to_datetime(sales["order_date"])

    # Create customer full name if needed
    if "customer_name" not in sales.columns:
        sales["customer_name"] = (
            sales["first_name"].fillna("") + " " +
            sales["last_name"].fillna("")
        ).str.strip()

    snapshot_date = sales["order_date"].max() + pd.Timedelta(days=1)

    rfm = sales.groupby("customer_name").agg({
        "order_date": lambda x: (snapshot_date - x.max()).days,
        "order_id": "nunique",
        "total_amount": "sum"
    }).reset_index()

    rfm.columns = [
        "Customer",
        "Recency",
        "Frequency",
        "Monetary"
    ]

    # Create scores (1-5)
    rfm["R_Score"] = pd.qcut(
        rfm["Recency"],
        5,
        labels=[5,4,3,2,1],
        duplicates="drop"
    ).astype(int)

    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"),
        5,
        labels=[1,2,3,4,5],
        duplicates="drop"
    ).astype(int)

    rfm["M_Score"] = pd.qcut(
        rfm["Monetary"],
        5,
        labels=[1,2,3,4,5],
        duplicates="drop"
    ).astype(int)

    rfm["RFM_Score"] = (
        rfm["R_Score"] +
        rfm["F_Score"] +
        rfm["M_Score"]
    )

    # Segment customers
    def segment(score):
        if score >= 13:
            return "Champions"
        elif score >= 10:
            return "Loyal Customers"
        elif score >= 8:
            return "Potential Loyalists"
        elif score >= 6:
            return "At Risk"
        else:
            return "Lost Customers"

    rfm["Segment"] = rfm["RFM_Score"].apply(segment)

    return rfm