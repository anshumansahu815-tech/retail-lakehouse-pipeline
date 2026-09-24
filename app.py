import streamlit as st
import pandas as pd

st.set_page_config(page_title="RetailLens Lakehouse Dashboard", layout="wide")

st.title("RetailLens: Store Hourly Performance Dashboard")
st.caption("Capstone Project 2026 | Anshuman Sahu (Roll: 23053678) | Databricks & Snowflake Lakehouse")

# Top KPI Summary Cards
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Revenue", "$44.77M")
kpi2.metric("Total Footfall", "483,233")
kpi3.metric("Total Transactions", "86,594")
kpi4.metric("Avg Conversion Rate", "17.92%")
kpi5.metric("Active Stores", "12 Locations")

st.divider()

# Hourly Performance Section
st.subheader("Hourly Revenue & Footfall Distribution (10:00 - 21:00)")
hourly_data = pd.DataFrame({
    "Store Hour": ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"],
    "Footfall (Visitors)": [33800, 33900, 35900, 37900, 22500, 22800, 20200, 33800, 68400, 68200, 68100, 37800],
    "Revenue ($)": [3690000, 3670000, 3710000, 3660000, 1020000, 1010000, 990000, 3660000, 6640000, 6540000, 6530000, 3640000]
}).set_index("Store Hour")

col_left, col_right = st.columns(2)
with col_left:
    st.write("**Total Sales Revenue ($)**")
    st.bar_chart(hourly_data["Revenue ($)"], color="#FFB000")
with col_right:
    st.write("**Customer Footfall (Visitors)**")
    st.bar_chart(hourly_data["Footfall (Visitors)"], color="#2979FF")

st.divider()

# Store Performance Rankings Table
st.subheader("Store Performance & Efficiency Rankings")
store_data = pd.DataFrame({
    "Store ID": ["ST04", "ST08", "ST02", "ST10", "ST01", "ST05", "ST07", "ST12", "ST03", "ST06", "ST11", "ST09"],
    "City": ["CITY3", "CITY1", "CITY0", "CITY4", "CITY0", "CITY3", "CITY2", "CITY5", "CITY1", "CITY4", "CITY5", "CITY2"],
    "Format": ["High Street", "High Street", "High Street", "High Street", "Mall", "High Street", "Mall", "High Street", "Mall", "Mall", "Mall", "Mall"],
    "Footfall": [40250, 40180, 40310, 40220, 40150, 40290, 40200, 40350, 40120, 40280, 40190, 40100],
    "Transactions": [9152, 8840, 8560, 8490, 7520, 7480, 7120, 6890, 6510, 6240, 5680, 3122],
    "Total Revenue ($)": [5154320.10, 4982140.50, 4812300.20, 4790100.80, 4120300.00, 4080120.40, 3890450.00, 3650200.00, 3320100.50, 3120400.00, 2720100.20, 1726224.34],
    "Avg Conversion Rate": ["22.74%", "22.00%", "21.23%", "21.11%", "18.73%", "18.57%", "17.71%", "17.08%", "16.23%", "15.49%", "14.13%", "7.78%"]
})
st.dataframe(store_data, use_container_width=True, hide_index=True)

st.info("Architecture: Medallion Lakehouse (Bronze -> Silver -> Gold) processed via Databricks Delta Lake and served on Snowflake RETAIL_DW.")
