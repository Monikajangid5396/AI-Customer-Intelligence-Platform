from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def generate_pdf_report(sales):

    filename = "Business_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>AI CUSTOMER INTELLIGENCE REPORT</b>", styles["Title"])
    )

    elements.append(Spacer(1,20))

    revenue = sales["total_amount"].sum()
    orders = sales["order_id"].nunique()
    customers = sales["customer_id"].nunique()

    state = (
        sales.groupby("state")["total_amount"]
        .sum()
        .idxmax()
    )

    brand = (
        sales.groupby("brand")["total_amount"]
        .sum()
        .idxmax()
    )

    category = (
        sales.groupby("category")["total_amount"]
        .sum()
        .idxmax()
    )

    avg_order = sales["total_amount"].mean()

    report = [

        f"<b>Total Revenue:</b> ₹{revenue:,.2f}",

        f"<b>Total Orders:</b> {orders}",

        f"<b>Total Customers:</b> {customers}",

        f"<b>Best State:</b> {state}",

        f"<b>Best Brand:</b> {brand}",

        f"<b>Top Category:</b> {category}",

        f"<b>Average Order Value:</b> ₹{avg_order:,.2f}",

    ]

    for line in report:

        elements.append(
            Paragraph(line, styles["BodyText"])
        )

        elements.append(
            Spacer(1,12)
        )

    doc.build(elements)

    return filename