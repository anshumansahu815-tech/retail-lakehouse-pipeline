import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="RetailLens: Store Hourly Lakehouse",
    page_icon="🛍️",
    layout="wide"
)

# 1. Load Production Gold Mart Dataset
@st.cache_data
def load_gold_data():
    data = pd.read_csv("gold_store_hour.csv")
    data.columns = [col.upper() for col in data.columns]
    return data

df = load_gold_data()

# 2. Executive Business KPIs (Full Gold Mart: 12,960 store-hours)
total_revenue = df["REVENUE"].sum()
total_footfall = int(df["FOOTFALL"].sum())
total_bills = int(df["BILLS"].sum())
active_stores = df["STORE_ID"].nunique()

# Sensor-Valid Aggregate Conversion Rate (Strict Topic 05 Schema Requirement)
sensor_valid_df = df[df["SENSOR_OK"] == True]
clean_footfall = sensor_valid_df["FOOTFALL"].sum()
clean_bills = sensor_valid_df["BILLS"].sum()
valid_conv_rate = (clean_bills / clean_footfall * 100) if clean_footfall > 0 else 0.0

# 3. Header & Metric Cards
st.title("RetailLens: Store Hourly Performance Lakehouse")
st.caption("Topic 05: Store Footfall vs Sales Conversion | Gold Mart Dashboard")
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Revenue", f"${total_revenue/1e6:.2f}M")
col2.metric("Total Footfall", f"{total_footfall:,}")
col3.metric("Total Transactions", f"{total_bills:,}")
col4.metric("Valid Conversion Rate", f"{valid_conv_rate:.2f}%")
col5.metric("Active Stores", f"{active_stores}")

st.markdown("---")

# 4. Store Performance Rankings (Reconciled with Snowflake GOLD query)
st.subheader("Store Performance Rankings")
st.caption("Aggregated across all 12,960 store-operating hours (Sorted by Total Revenue)")

store_rankings = df.groupby(["STORE_ID", "CITY", "FORMAT"]).agg(
    FOOTFALL=("FOOTFALL", "sum"),
    TRANSACTIONS=("BILLS", "sum"),
    TOTAL_REVENUE=("REVENUE", "sum")
).reset_index()

# Individual store conversion rate calculated on sensor-valid hours
store_valid_metrics = sensor_valid_df.groupby("STORE_ID").agg(
    VALID_FOOTFALL=("FOOTFALL", "sum"),
    VALID_BILLS=("BILLS", "sum")
).reset_index()
store_valid_metrics["CONV_RATE_%"] = (
    store_valid_metrics["VALID_BILLS"] / store_valid_metrics["VALID_FOOTFALL"] * 100
).round(2)

store_rankings = store_rankings.merge(
    store_valid_metrics[["STORE_ID", "CONV_RATE_%"]], on="STORE_ID", how="left"
)
store_rankings = store_rankings.sort_values(by="TOTAL_REVENUE", ascending=False)

st.dataframe(
    store_rankings.style.format({
        "FOOTFALL": "{:,}",
        "TRANSACTIONS": "{:,}",
        "TOTAL_REVENUE": "${:,.2f}",
        "CONV_RATE_%": "{:.2f}%"
    }),
    use_container_width=True
)

st.markdown("---")

# 5. Hourly Revenue Profile (10:00 to 21:00 Operating Window)
st.subheader("Hourly Revenue Profile")
hourly_profile = df.groupby("HOUR").agg(
    TOTAL_REVENUE=("REVENUE", "sum"),
    TOTAL_FOOTFALL=("FOOTFALL", "sum"),
    TOTAL_BILLS=("BILLS", "sum")
).reset_index()

st.bar_chart(hourly_profile.set_index("HOUR")["TOTAL_REVENUE"])
