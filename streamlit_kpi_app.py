# %%

# =============================================================================
# E-COMMERCE KPI DASHBOARD - STREAMLIT APP
# Uses data generated from the KPI modeling pipeline
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="E-commerce KPI Projections 2026",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# DATA LOADER
# =============================================================================

@st.cache_data
def load_pipeline_data():
    """Load the data generated from the KPI modeling pipeline"""
    try:
        with open('streamlit_data.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error("Pipeline data not found. Please run the KPI modeling pipeline first.")
        st.stop()

# Load data
data = load_pipeline_data()
annual_df = data['annual_projections']
baseline_df = data['baseline_projections'] 
holiday_df = data['holiday_projections']
summary_metrics = data['summary_metrics']

# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================

st.sidebar.header("🎛️ Scenario Controls")

# Spend range selector
min_annual_spend = int(annual_df['total_annual_spend'].min())
max_annual_spend = int(annual_df['total_annual_spend'].max())

spend_range = st.sidebar.slider(
    "Annual Spend Range ($M)",
    min_value=min_annual_spend // 1_000_000,
    max_value=max_annual_spend // 1_000_000,
    value=(0, max_annual_spend // 1_000_000),
    step=5
)

# ROAS threshold
min_roas = st.sidebar.selectbox(
    "Minimum ROAS Threshold",
    options=[0.0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
    index=0
)

# Analysis type
analysis_type = st.sidebar.radio(
    "Analysis Type",
    ["📊 Annual Overview", "📈 Marginal Returns", "🎯 Scenario Comparison", "📋 Data Table"]
)

# Filter data based on selections
filtered_df = annual_df[
    (annual_df['total_annual_spend'] >= spend_range[0] * 1_000_000) &
    (annual_df['total_annual_spend'] <= spend_range[1] * 1_000_000) &
    (annual_df['blended_roas'] >= min_roas)
].copy()

# =============================================================================
# MAIN DASHBOARD
# =============================================================================

# Header
st.title("🚀 E-commerce KPI Projections 2026")
st.markdown("*Data-driven spend optimization using fitted mathematical models*")

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Scenarios",
        f"{len(filtered_df):,}",
        f"{len(filtered_df) - len(annual_df)} from filters"
    )

with col2:
    if not filtered_df.empty:
        max_sales = filtered_df['total_annual_sales'].max()
        st.metric(
            "Max Annual Sales",
            f"${max_sales/1_000_000:.1f}M",
            f"${max_sales/1_000_000 - annual_df['total_annual_sales'].min()/1_000_000:.1f}M potential"
        )

with col3:
    if not filtered_df.empty:
        best_roas = filtered_df['blended_roas'].max()
        st.metric(
            "Best ROAS",
            f"{best_roas:.2f}x",
            f"{best_roas - annual_df['blended_roas'].min():.2f}x range" 
        )

with col4:
    if not filtered_df.empty:
        optimal_spend = filtered_df.loc[filtered_df['blended_roas'].idxmax(), 'total_annual_spend']
        st.metric(
            "Optimal Spend",
            f"${optimal_spend/1_000_000:.1f}M",
            "Highest ROAS"
        )

# =============================================================================
# ANALYSIS SECTIONS
# =============================================================================

if analysis_type == "📊 Annual Overview":
    st.header("📊 Annual Performance Overview")
    
    if filtered_df.empty:
        st.warning("No scenarios match your filters. Please adjust the controls.")
    else:
        # Main performance chart
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.scatter(
                filtered_df,
                x='total_annual_spend',
                y='total_annual_sales',
                color='blended_roas',
                size='blended_roas',
                title="Annual Sales vs Spend (colored by ROAS)",
                labels={
                    'total_annual_spend': 'Annual Spend ($)',
                    'total_annual_sales': 'Annual Sales ($)',
                    'blended_roas': 'ROAS'
                },
                color_continuous_scale='Viridis'
            )
            fig1.update_layout(height=500)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.line(
                filtered_df,
                x='total_annual_spend',
                y='blended_roas',
                title="ROAS Curve - Diminishing Returns",
                labels={
                    'total_annual_spend': 'Annual Spend ($)',
                    'blended_roas': 'Blended ROAS'
                }
            )
            fig2.add_hline(y=2.0, line_dash="dash", line_color="red", 
                          annotation_text="2.0x ROAS Threshold")
            fig2.update_layout(height=500)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Performance breakdown
        st.subheader("🎯 Key Performance Indicators")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig3 = px.line(
                filtered_df,
                x='total_annual_spend',
                y='blended_conversion_rate',
                title="Conversion Rate vs Spend"
            )
            fig3.update_layout(yaxis_tickformat='.1%')
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            fig4 = px.line(
                filtered_df,
                x='total_annual_spend',
                y='blended_aov',
                title="Average Order Value vs Spend"
            )
            fig4.update_layout(yaxis_tickformat='$,.0f')
            st.plotly_chart(fig4, use_container_width=True)
        
        with col3:
            fig5 = px.line(
                filtered_df,
                x='total_annual_spend',
                y='total_annual_traffic',
                title="Annual Traffic vs Spend"
            )
            fig5.update_layout(yaxis_tickformat=',.0f')
            st.plotly_chart(fig5, use_container_width=True)

elif analysis_type == "📈 Marginal Returns":
    st.header("📈 Marginal Returns Analysis")
    
    if filtered_df.empty:
        st.warning("No scenarios match your filters. Please adjust the controls.")
    else:
        # Check if we have the marginal ROAS from 137M column
        has_marginal_137m = 'marginal_roas_from_137m' in filtered_df.columns
        
        if has_marginal_137m:
            st.info("📊 Showing marginal ROAS calculated from $137M baseline")
        
        # Marginal ROAS analysis
        baseline_filtered = baseline_df[
            (baseline_df['weekly_spend'] >= spend_range[0] * 1_000_000 / 52) &
            (baseline_df['weekly_spend'] <= spend_range[1] * 1_000_000 / 52)
        ].copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if has_marginal_137m:
                # Plot marginal ROAS from $137M baseline
                fig1 = px.line(
                    filtered_df.dropna(subset=['marginal_roas_from_137m']),
                    x='total_annual_spend',
                    y='marginal_roas_from_137m',
                    title="Marginal ROAS from $137M Baseline",
                    labels={
                        'total_annual_spend': 'Annual Spend ($)',
                        'marginal_roas_from_137m': 'Marginal ROAS from $137M'
                    }
                )
                
                # Add threshold lines
                for threshold in [3.0, 2.5, 2.0, 1.5, 1.0, 0.5]:
                    fig1.add_hline(y=threshold, line_dash="dash", line_color="rgba(255,0,0,0.3)",
                                  annotation_text=f"{threshold}x")
                
                fig1.update_layout(height=500)
                st.plotly_chart(fig1, use_container_width=True)
            else:
                # Fallback to regular marginal ROAS
                fig1 = px.line(
                    baseline_filtered,
                    x='weekly_spend',
                    y='marginal_roas',
                    title="Weekly Marginal ROAS",
                    labels={
                        'weekly_spend': 'Weekly Spend ($)',
                        'marginal_roas': 'Marginal ROAS'
                    }
                )
                
                # Add threshold lines
                for threshold in [3.0, 2.5, 2.0, 1.5, 1.0]:
                    fig1.add_hline(y=threshold, line_dash="dash", line_color="rgba(255,0,0,0.3)",
                                  annotation_text=f"{threshold}x")
                
                fig1.update_layout(height=500)
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Compare blended vs marginal ROAS
            if has_marginal_137m:
                marginal_data = filtered_df.dropna(subset=['marginal_roas_from_137m'])
                fig2 = go.Figure()
                
                fig2.add_trace(go.Scatter(
                    x=marginal_data['total_annual_spend'],
                    y=marginal_data['blended_roas'],
                    mode='lines',
                    name='Blended ROAS',
                    line=dict(color='#1f77b4', width=2)
                ))
                
                fig2.add_trace(go.Scatter(
                    x=marginal_data['total_annual_spend'],
                    y=marginal_data['marginal_roas_from_137m'],
                    mode='lines',
                    name='Marginal ROAS from $137M',
                    line=dict(color='#ff7f0e', width=2)
                ))
                
                fig2.update_layout(
                    title="Blended vs Marginal ROAS from $137M Baseline",
                    xaxis_title="Annual Spend ($)",
                    yaxis_title="ROAS",
                    height=500
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            else:
                fig2 = px.line(
                    baseline_filtered,
                    x='weekly_spend',
                    y='sales_increase',
                    title="Incremental Sales per $25k Spend Increase",
                    labels={
                        'weekly_spend': 'Weekly Spend ($)',
                        'sales_increase': 'Incremental Weekly Sales ($)'
                    }
                )
                fig2.update_layout(height=500)
                st.plotly_chart(fig2, use_container_width=True)
        
        # Threshold analysis
        st.subheader("🎯 Marginal Returns Thresholds")
        
        if has_marginal_137m:
            # Analysis based on marginal ROAS from $137M
            thresholds_data = []
            marginal_data = filtered_df.dropna(subset=['marginal_roas_from_137m'])
            
            for threshold in [3.0, 2.5, 2.0, 1.5, 1.0, 0.5]:
                below_threshold = marginal_data[marginal_data['marginal_roas_from_137m'] < threshold]
                if not below_threshold.empty:
                    first_below = below_threshold.iloc[0]
                    incremental_spend = first_below['total_annual_spend'] - 137_200_000
                    thresholds_data.append({
                        'Marginal ROAS Threshold': f"{threshold:.1f}x",
                        'Annual Spend': f"${first_below['total_annual_spend']/1e6:.1f}M",
                        'Incremental from $137M': f"${incremental_spend/1e6:.1f}M",
                        'Annual Sales': f"${first_below['total_annual_sales']/1e6:.1f}M",
                        'Blended ROAS': f"{first_below['blended_roas']:.2f}x"
                    })
        else:
            # Fallback to weekly analysis
            thresholds_data = []
            for threshold in [4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0]:
                below_threshold = baseline_filtered[baseline_filtered['marginal_roas'] < threshold]
                if not below_threshold.empty:
                    first_below = below_threshold.iloc[0]
                    annual_spend = first_below['weekly_spend'] * 52
                    thresholds_data.append({
                        'ROAS Threshold': f"{threshold:.1f}x",
                        'Weekly Spend': f"${first_below['weekly_spend']:,.0f}",
                        'Annual Spend': f"${annual_spend:,.0f}",
                        'Annual Sales': f"${first_below['sales'] * 52:,.0f}"
                    })
        
        if thresholds_data:
            thresholds_df = pd.DataFrame(thresholds_data)
            st.dataframe(thresholds_df, use_container_width=True)

elif analysis_type == "🎯 Scenario Comparison":
    st.header("🎯 Scenario Comparison")
    
    # Scenario selector
    st.subheader("Select Scenarios to Compare")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        scenario_1_spend = st.selectbox(
            "Scenario 1 - Annual Spend",
            options=filtered_df['total_annual_spend'].round(-6).unique(),
            format_func=lambda x: f"${x/1_000_000:.1f}M"
        )
    
    with col2:
        scenario_2_spend = st.selectbox(
            "Scenario 2 - Annual Spend", 
            options=filtered_df['total_annual_spend'].round(-6).unique(),
            index=min(len(filtered_df['total_annual_spend'].round(-6).unique())-1, 5),
            format_func=lambda x: f"${x/1_000_000:.1f}M"
        )
    
    with col3:
        scenario_3_spend = st.selectbox(
            "Scenario 3 - Annual Spend",
            options=filtered_df['total_annual_spend'].round(-6).unique(),
            index=min(len(filtered_df['total_annual_spend'].round(-6).unique())-1, 10),
            format_func=lambda x: f"${x/1_000_000:.1f}M"
        )
    
    # Get scenario data
    scenarios = []
    for i, spend in enumerate([scenario_1_spend, scenario_2_spend, scenario_3_spend], 1):
        scenario_data = filtered_df[
            (filtered_df['total_annual_spend'] >= spend * 0.99) & 
            (filtered_df['total_annual_spend'] <= spend * 1.01)
        ].iloc[0]
        
        scenarios.append({
            'Scenario': f"Scenario {i}",
            'Annual Spend': f"${scenario_data['total_annual_spend']/1_000_000:.1f}M",
            'Annual Sales': f"${scenario_data['total_annual_sales']/1_000_000:.1f}M",
            'ROAS': f"{scenario_data['blended_roas']:.2f}x",
            'Traffic': f"{scenario_data['total_annual_traffic']:,.0f}",
            'Conv Rate': f"{scenario_data['blended_conversion_rate']:.2%}",
            'AOV': f"${scenario_data['blended_aov']:.0f}",
            'Transactions': f"{scenario_data['total_annual_transactions']:,.0f}"
        })
    
    # Display comparison
    comparison_df = pd.DataFrame(scenarios)
    st.dataframe(comparison_df, use_container_width=True)

elif analysis_type == "📋 Data Table":
    st.header("📋 Complete Data Table")
    
    if filtered_df.empty:
        st.warning("No scenarios match your filters. Please adjust the controls.")
    else:
        # Format data for display
        display_df = filtered_df.copy()
        display_df['Annual Spend ($M)'] = (display_df['total_annual_spend'] / 1_000_000).round(1)
        display_df['Annual Sales ($M)'] = (display_df['total_annual_sales'] / 1_000_000).round(1)
        display_df['ROAS'] = display_df['blended_roas'].round(2)
        display_df['Conv Rate (%)'] = (display_df['blended_conversion_rate'] * 100).round(2)
        display_df['AOV ($)'] = display_df['blended_aov'].round(0)
        display_df['Annual Traffic'] = display_df['total_annual_traffic'].round(0)
        display_df['Marginal ROAS'] = display_df['marginal_roas'].round(3)
        
        # Add marginal ROAS from $137M if available
        columns_to_show = [
            'Annual Spend ($M)', 'Annual Sales ($M)', 'ROAS', 'Conv Rate (%)', 
            'AOV ($)', 'Annual Traffic', 'Marginal ROAS'
        ]
        
        if 'marginal_roas_from_137m' in display_df.columns:
            display_df['Marginal ROAS from $137M'] = display_df['marginal_roas_from_137m'].round(3)
            columns_to_show.append('Marginal ROAS from $137M')
            st.info("📊 Table includes Marginal ROAS calculated from $137M baseline")
        
        st.dataframe(
            display_df[columns_to_show],
            use_container_width=True,
            height=600
        )
        
        # Download button
        csv = display_df[columns_to_show].to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"kpi_projections_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📊 Data Generated:**")
    st.markdown(f"Pipeline run: {data['data_timestamp'].strftime('%Y-%m-%d %H:%M')}")

with col2:
    st.markdown("**🔧 Model Details:**")
    st.markdown("Mathematical models fitted to historical data")

with col3:
    st.markdown("**💡 Usage:**")
    st.markdown("Adjust filters to explore different scenarios")

# %%
