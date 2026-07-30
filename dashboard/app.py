import streamlit as st
import pandas as pd
import plotly.express as px

from database import load_data
from forecast import sales_forecast
from customer_segmentation import customer_segmentation
from ai_insights import generate_insights
from ai_chat import ask_ai
from anomaly_detection import detect_anomalies
from pdf_report import generate_pdf_report
from rfm_analysis import rfm_analysis

st.set_page_config(
    page_title="AI Customer Intelligence Dashboard",
    layout="wide"
)
st.markdown("""
<style>

/* Main background */
.stApp{
    background-color:#0E1117;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#1E1E2F;
}

/* Metric Cards */
[data-testid="metric-container"]{
    background:#262730;
    border:1px solid #404040;
    border-radius:12px;
    padding:15px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.3);
}

/* Dashboard Title */
h1{
    color:#4CAF50;
}

</style>
""", unsafe_allow_html=True)

st.title("📊 AI Customer Intelligence Dashboard")

customers, products, orders, sales = load_data()

st.success("Database Connected Successfully!")


st.sidebar.title("Filters")

segment = st.sidebar.multiselect(
    "Customer Segment",
    sales["customer_segment"].unique(),
    default=sales["customer_segment"].unique(),
)

payment = st.sidebar.multiselect(
    "Payment Method",
    sales["payment_method"].unique(),
    default=sales["payment_method"].unique(),
)
category = st.sidebar.multiselect(
    "📦 Product Category",
    sales["category"].unique(),
    default=sales["category"].unique(),
)

state = st.sidebar.multiselect(
    "🌍 State",
    sales["state"].unique(),
    default=sales["state"].unique(),
)

brand = st.sidebar.multiselect(
    "🏷 Brand",
    sorted(sales["brand"].unique()),
    default=sorted(sales["brand"].unique()),
)

# ================= Reset Filters =================

if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()
    
# ================= Date Filter =================

sales["order_date"] = pd.to_datetime(sales["order_date"])

min_date = sales["order_date"].min()
max_date = sales["order_date"].max()

date_range = st.sidebar.date_input(
    "📅 Select Date Range",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date(),
)

sales = sales[
    (sales["customer_segment"].isin(segment))
    &
    (sales["payment_method"].isin(payment))
    &
    (sales["category"].isin(category))
    &
    (sales["state"].isin(state))
    &
    (sales["brand"].isin(brand))
]

# Apply Date Filter
if len(date_range) == 2:
    start_date, end_date = date_range

    sales = sales[
        (sales["order_date"].dt.date >= start_date)
        &
        (sales["order_date"].dt.date <= end_date)
    ]


# ================= Empty Data Check =================

if sales.empty:
    st.warning("⚠️ No data found for the selected filters.")
    st.stop()
# ================= KPI =================

total_revenue = sales["total_amount"].sum()
total_orders = sales["order_id"].nunique()
total_customers = len(customers)
avg_order = sales["total_amount"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("📦 Orders", total_orders)
c3.metric("👥 Customers", total_customers)
c4.metric("🛒 Avg Order", f"₹{avg_order:,.0f}")

# ================= Monthly Revenue Chart =================

monthly = (
    sales.groupby(sales["order_date"].dt.to_period("M"))["total_amount"]
    .sum()
    .reset_index()
)

monthly["order_date"] = monthly["order_date"].astype(str)

fig = px.line(
    monthly,
    x="order_date",
    y="total_amount",
    title="Monthly Revenue Trend",
    markers=True,
)
fig.update_layout(height=400)

st.plotly_chart(fig, width="stretch")


# ================= Top Products & Payment Method =================

col1, col2 = st.columns(2)

with col1:
    top_products = (
        sales.groupby("product_name", as_index=False)
        .agg(Revenue=("total_amount", "sum"))
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    fig_products = px.bar(
        top_products,
        x="Revenue",
        y="product_name",
        orientation="h",
        title="🏆 Top 10 Products by Revenue",
    )
    fig_products.update_layout(height=450)

    st.plotly_chart(fig_products, width="stretch")

with col2:
    payment_data = (
        sales.groupby("payment_method", as_index=False)
        .agg(Revenue=("total_amount", "sum"))
    )

    fig_payment = px.pie(
        payment_data,
        names="payment_method",
        values="Revenue",
        title="💳 Revenue by Payment Method",
        hole=0.4
    )
    fig_payment.update_layout(height=450)

    st.plotly_chart(fig_payment, width="stretch")

# ================= Revenue by Customer Segment =================

st.subheader("📊 Revenue by Customer Segment")

segment_data = (
    sales.groupby("customer_segment", as_index=False)
    .agg(Revenue=("total_amount", "sum"))
)

fig_segment = px.bar(
    segment_data,
    x="customer_segment",
    y="Revenue",
    color="customer_segment",
    title="Revenue by Customer Segment",
)
fig_segment.update_layout(height=400)

st.plotly_chart(fig_segment, width="stretch")

st.subheader("📦 Revenue by Product Category")

category_data = (
    sales.groupby("category", as_index=False)
    .agg(Revenue=("total_amount", "sum"))
    .sort_values("Revenue", ascending=False)
)

fig_category = px.bar(
    category_data,
    x="category",
    y="Revenue",
    color="category",
    title="Revenue by Product Category",
)
fig_category.update_layout(height=400)
st.plotly_chart(fig_category, width="stretch")


st.subheader("🌍 Revenue by State")

state_data = (
    sales.groupby("state", as_index=False)
    .agg(Revenue=("total_amount", "sum"))
    .sort_values("Revenue", ascending=False)
)

fig_state = px.bar(
    state_data,
    x="state",
    y="Revenue",
    color="Revenue",
    title="Revenue by State",
)
fig_state.update_layout(height=400)

st.plotly_chart(fig_state, width="stretch")

st.subheader("🏷 Revenue by Brand")

brand_data = (
    sales.groupby("brand", as_index=False)
    .agg(Revenue=("total_amount","sum"))
    .sort_values("Revenue",ascending=False)
)

fig_brand = px.bar(
    brand_data,
    x="brand",
    y="Revenue",
    color="brand",
    title="Revenue by Brand"
)
fig_brand.update_layout(height=400)
st.plotly_chart(fig_brand, width="stretch")

st.subheader("⭐ Product Rating Distribution")

fig_rating = px.histogram(
    sales,
    x="rating",
    nbins=10,
    title="Product Rating Distribution"
)

fig_rating.update_layout(height=400)

st.plotly_chart(fig_rating, width="stretch")

st.subheader("👨‍🦰 Revenue by Gender")

gender_data = (
    sales.groupby("gender",as_index=False)
    .agg(Revenue=("total_amount","sum"))
)

fig_gender = px.pie(
    gender_data,
    names="gender",
    values="Revenue",
    hole=0.5,
    title="Revenue by Gender"
)

fig_gender.update_layout(height=400)
st.plotly_chart(fig_gender, width="stretch")

st.subheader("💰 Customer Annual Income Distribution")

fig_income = px.histogram(
    sales,
    x="annual_income",
    nbins=20,
    title="Customer Annual Income Distribution",
)

fig_income.update_layout(height=400)
st.plotly_chart(fig_income, width="stretch")

st.subheader("📦 Order Status Analysis")

status_data = (
    sales.groupby("order_status", as_index=False)
    .agg(Orders=("order_id", "count"))
)

fig_status = px.bar(
    status_data,
    x="order_status",
    y="Orders",
    color="order_status",
    title="Orders by Status",
)
fig_status.update_layout(height=400)
st.plotly_chart(fig_status, width="stretch")

# ================= Top Brands =================

top_brands = (
    sales.groupby("brand", as_index=False)
    .agg(
        Revenue=("total_amount", "sum"),
        Products=("product_id", "nunique"),
    )
    .sort_values("Revenue", ascending=False)
    .head(10)
)

monthly_orders = (
    sales.groupby(sales["order_date"].dt.to_period("M"))
    .size()
    .reset_index(name="Orders")
)

monthly_orders["order_date"] = monthly_orders["order_date"].astype(str)
st.subheader("📈 Monthly Orders Trend")
fig_orders = px.line(
    monthly_orders,
    x="order_date",
    y="Orders",
    markers=True,
    title="Monthly Orders Trend",
)
fig_orders.update_layout(height=400)
st.plotly_chart(fig_orders, width="stretch")


st.subheader("📊 Revenue vs Quantity")

fig_scatter = px.scatter(
    sales,
    x="quantity",
    y="total_amount",
    color="category",
    size="quantity",
    hover_data=["product_name"],
    title="Revenue vs Quantity Sold",
)
fig_scatter.update_layout(height=400)
st.plotly_chart(fig_scatter, width="stretch")


# ================= Top Customers =================

top_customers = (
    sales.groupby(
        ["customer_id", "first_name", "last_name"],
        as_index=False,
    )
    .agg(
        Revenue=("total_amount", "sum"),
        Orders=("order_id", "count"),
    )
    .sort_values("Revenue", ascending=False)
    .head(10)
)

# ================= Top Customers & Top Brands =================

col1, col2 = st.columns(2)

with col1:
    st.subheader("👑 Top 10 Customers")
    st.dataframe(
        top_customers.rename(
            columns = {
                "customer_id": "Customer ID",
                "first_name": "First Name",
                "last_name": "Last Name",
                "Revenue": "Total Revenue",
                "Orders": "Total Orders"
            }
        ),
        width="stretch",
    )

with col2:
    st.subheader("🏆 Top 10 Brands")
    st.dataframe(
        top_brands.rename(
            columns = {
                "brand": "Brand",
                "Revenue": "Total Revenue",
                "Products": "Unique Products"
            }
        ),
        width="stretch",
    )

# ================= Data Preview =================

st.subheader("📋 Recent Orders")

st.dataframe(
    sales[
        [
            "order_id",
            "customer_id",
            "product_name",
            "total_amount",
            "payment_method",
            "order_status",
        ]
    ].head(15),
    width="stretch",
)

st.download_button(
    label="📥 Download Filtered Data",
    data=sales.to_csv(index=False),
    file_name="filtered_sales.csv",
    mime="text/csv",
)

st.markdown("---")
st.header("🤖 AI Sales Forecast")

try:
    model, forecast = sales_forecast(sales)

    fig = px.line(
        forecast,
        x="ds",
        y=["yhat", "yhat_lower", "yhat_upper"],
        labels={
            "value": "Predicted Revenue",
            "ds": "Date"
        },
        title="Next 30 Days Sales Forecast"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, width="stretch")

    st.success("✅ Forecast generated successfully!")

except Exception as e:
    st.error(f"Forecast Error: {e}")
    

st.markdown("---")
st.header("👥 AI Customer Segmentation")

try:
    customer_clusters = customer_segmentation(sales)

    # Cluster labels
    cluster_summary = (
        customer_clusters.groupby("Cluster")["total_amount"]
        .mean()
        .sort_values()
    )

    mapping = {
        cluster_summary.index[0]: "Low Value",
        cluster_summary.index[1]: "Medium Value",
        cluster_summary.index[2]: "High Value"
    }

    customer_clusters["Segment"] = customer_clusters["Cluster"].map(mapping)

    fig = px.scatter(
        customer_clusters,
        x="quantity",
        y="total_amount",
        color="Segment",
        hover_data=["customer_id"],
        title="AI Customer Segmentation"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, width="stretch")

    st.subheader("Segment Summary")

    st.dataframe(
        customer_clusters.groupby("Segment")
        .agg(
            Customers=("customer_id", "count"),
            Revenue=("total_amount", "sum"),
            Quantity=("quantity", "sum")
        )
        .reset_index(),
        width="stretch"
    )

except Exception as e:
    st.error(f"Segmentation Error: {e}")
    
st.markdown("---")
st.header("🤖 AI Business Insights")

try:
    insights = generate_insights(sales)

    for insight in insights:
        st.info(insight)

except Exception as e:
    st.error(f"AI Insights Error: {e}")
    
st.markdown("---")
st.header("💬 AI Business Assistant")

question = st.text_input(
    "Ask anything about your business data",
    placeholder="Example: Which state has highest revenue?"
)

if st.button("Ask AI"):
    if question.strip():
        answer = ask_ai(question, sales)
        st.success(answer)
    else:
        st.warning("Please enter a question.")
        
st.markdown("---")
st.header("🚨 AI Anomaly Detection")

try:
    anomaly_data = detect_anomalies(sales)

    anomaly_data["Status"] = anomaly_data["Anomaly"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    fig = px.scatter(
        anomaly_data,
        x="quantity",
        y="total_amount",
        color="Status",
        hover_data=[
            "first_name",
            "last_name",
            "product_name",
            "state",
            "total_amount"
        ],
        title="Transaction Anomaly Detection"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, width="stretch")

    st.subheader("🚨 Suspicious Transactions")

    st.dataframe(
        anomaly_data[anomaly_data["Status"] == "Anomaly"],
        width="stretch"
    )

except Exception as e:
    st.error(f"Anomaly Detection Error: {e}")
    
    
    
st.markdown("---")
st.header("📄 AI Business Report")

pdf_file = generate_pdf_report(sales)

with open(pdf_file, "rb") as file:
    st.download_button(
        label="📥 Download Business Report (PDF)",
        data=file,
        file_name="Business_Report.pdf",
        mime="application/pdf"
    )
    
    
st.markdown("---")
st.header("👥 RFM Customer Segmentation")

try:
    rfm = rfm_analysis(sales)

    col1, col2 = st.columns(2)

    # Segment counts
    segment_counts = (
        rfm["Segment"]
        .value_counts()
        .rename_axis("Segment")
        .reset_index(name="Customers")
    )

    with col1:
        fig = px.bar(
            segment_counts,
            x="Segment",
            y="Customers",
            color="Segment",
            text="Customers",
            title="Customer Segments"
        )

        fig.update_layout(height=450)

        st.plotly_chart(fig, width="stretch")

    with col2:
        fig = px.pie(
            segment_counts,
            names="Segment",
            values="Customers",
            title="Customer Distribution",
            hole=0.4
        )

        fig.update_layout(height=450)

        st.plotly_chart(fig, width="stretch")

    st.subheader("🏆 Top Customers by Monetary Value")

    st.dataframe(
        rfm.sort_values(
            by="Monetary",
            ascending=False
        ).head(20),
        width="stretch"
    )

except Exception as e:
    st.error(f"❌ RFM Analysis Error: {e}")