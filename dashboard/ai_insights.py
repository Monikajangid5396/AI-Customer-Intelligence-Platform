def generate_insights(sales):
    insights = []

    # Top Category
    top_category = (
        sales.groupby("category")["total_amount"]
        .sum()
        .idxmax()
    )

    insights.append(
        f"🏆 Highest Revenue Category: {top_category}"
    )

    # Top State
    top_state = (
        sales.groupby("state")["total_amount"]
        .sum()
        .idxmax()
    )

    insights.append(
        f"🌍 Best Performing State: {top_state}"
    )

    # Top Brand
    top_brand = (
        sales.groupby("brand")["total_amount"]
        .sum()
        .idxmax()
    )

    insights.append(
        f"⭐ Best Selling Brand: {top_brand}"
    )

    # Payment Method
    payment = (
        sales["payment_method"]
        .value_counts()
        .idxmax()
    )

    insights.append(
        f"💳 Most Preferred Payment Method: {payment}"
    )

    # Average Order Value
    avg_order = sales["total_amount"].mean()

    insights.append(
        f"💰 Average Order Value: ₹{avg_order:,.2f}"
    )

    return insights