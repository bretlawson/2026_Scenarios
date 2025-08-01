import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="2026 Scenarios Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📊 2026 Scenarios Dashboard")
st.markdown("Welcome to the 2026 Scenarios Analysis Dashboard")

# Sidebar
st.sidebar.header("Dashboard Controls")
scenario_type = st.sidebar.selectbox(
    "Select Scenario Type",
    ["Baseline", "Optimistic", "Pessimistic", "Conservative"]
)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sample Data Visualization")
    
    # Generate sample data
    dates = pd.date_range("2024-01-01", "2026-12-31", freq="M")
    data = {
        "Date": dates,
        "Revenue": np.random.randint(100000, 500000, len(dates)),
        "Costs": np.random.randint(50000, 200000, len(dates)),
        "Profit": np.random.randint(20000, 150000, len(dates))
    }
    df = pd.DataFrame(data)
    
    # Line chart
    fig = px.line(df, x="Date", y=["Revenue", "Costs", "Profit"], 
                  title=f"{scenario_type} Scenario - Financial Trends")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Key Metrics")
    
    # Metrics
    total_revenue = df["Revenue"].sum()
    total_costs = df["Costs"].sum()
    total_profit = df["Profit"].sum()
    
    st.metric("Total Revenue", f"${total_revenue:,}")
    st.metric("Total Costs", f"${total_costs:,}")
    st.metric("Total Profit", f"${total_profit:,}")
    
    # Bar chart
    metrics_df = pd.DataFrame({
        "Metric": ["Revenue", "Costs", "Profit"],
        "Value": [total_revenue, total_costs, total_profit]
    })
    
    fig_bar = px.bar(metrics_df, x="Metric", y="Value", 
                     title=f"{scenario_type} Scenario - Summary")
    st.plotly_chart(fig_bar, use_container_width=True)

# Data table
st.subheader("Data Table")
st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit 🎈")
