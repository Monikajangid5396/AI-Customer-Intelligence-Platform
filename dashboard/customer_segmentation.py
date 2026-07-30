import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def customer_segmentation(sales):
    # Customer-wise summary
    customer_data = (
        sales.groupby("customer_id")
        .agg({
            "total_amount": "sum",
            "quantity": "sum"
        })
        .reset_index()
    )

    # Scale features
    scaler = StandardScaler()
    scaled = scaler.fit_transform(
        customer_data[["total_amount", "quantity"]]
    )

    # KMeans clustering
    kmeans = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    customer_data["Cluster"] = kmeans.fit_predict(scaled)

    return customer_data