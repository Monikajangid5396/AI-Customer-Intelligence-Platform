import pandas as pd

def ask_ai(question, sales):
    question = question.lower().strip()

    # Create full customer name if not already present
    if "customer_name" not in sales.columns:
        sales = sales.copy()
        sales["customer_name"] = (
            sales["first_name"].fillna("") + " " +
            sales["last_name"].fillna("")
        ).str.strip()

    # Highest Revenue State
    if any(x in question for x in [
        "highest revenue state",
        "top state",
        "best state",
        "highest state"
    ]):
        state_sales = sales.groupby("state")["total_amount"].sum()
        state = state_sales.idxmax()
        revenue = state_sales.max()

        return f"🏆 {state} generated the highest revenue of ₹{revenue:,.2f}"

    # Top Brand
    elif any(x in question for x in [
        "top brand",
        "best brand",
        "highest brand"
    ]):
        brand_sales = sales.groupby("brand")["total_amount"].sum()
        brand = brand_sales.idxmax()
        revenue = brand_sales.max()

        return f"⭐ {brand} is the best performing brand with revenue of ₹{revenue:,.2f}"

    # Payment Method
    elif "payment" in question:
        payment = sales["payment_method"].value_counts().idxmax()
        count = sales["payment_method"].value_counts().max()

        return f"💳 Most used payment method is {payment} ({count} orders)."

    # Top Customer
    elif any(x in question for x in [
        "top customer",
        "best customer",
        "highest customer"
    ]):
        customer_sales = sales.groupby("customer_name")["total_amount"].sum()
        customer = customer_sales.idxmax()
        revenue = customer_sales.max()

        return f"👑 Top customer is {customer} with purchases worth ₹{revenue:,.2f}"

    # Highest Revenue Category
    elif "category" in question:
        category_sales = sales.groupby("category")["total_amount"].sum()
        category = category_sales.idxmax()
        revenue = category_sales.max()

        return f"📦 {category} is the highest revenue category with ₹{revenue:,.2f}"

    # Total Revenue
    elif "total revenue" in question:
        revenue = sales["total_amount"].sum()
        return f"💰 Total Revenue is ₹{revenue:,.2f}"

    # Total Orders
    elif "total order" in question:
        return f"🛒 Total Orders: {sales['order_id'].nunique()}"

    # Total Customers
    elif "total customer" in question:
        return f"👥 Total Customers: {sales['customer_id'].nunique()}"

    else:
        return (
            "🤖 I can answer questions like:\n\n"
            "• Top State\n"
            "• Top Brand\n"
            "• Top Customer\n"
            "• Payment Method\n"
            "• Highest Revenue Category\n"
            "• Total Revenue\n"
            "• Total Orders\n"
            "• Total Customers"
        )