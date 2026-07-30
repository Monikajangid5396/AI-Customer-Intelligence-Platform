from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(sales):
    """
    Detect anomalous transactions using Isolation Forest.
    """

    sales = sales.copy()

    # Required columns
    required_cols = ["total_amount", "quantity"]

    for col in required_cols:
        if col not in sales.columns:
            raise ValueError(f"Missing required column: {col}")

    # Handle missing values
    sales["total_amount"] = sales["total_amount"].fillna(0)
    sales["quantity"] = sales["quantity"].fillna(0)

    # Features for model
    X = sales[["total_amount", "quantity"]]

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    sales["Anomaly"] = model.fit_predict(X)

    # Convert prediction to readable labels
    sales["Status"] = sales["Anomaly"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    return sales