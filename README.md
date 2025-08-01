# E-commerce KPI Dashboard 2026

A comprehensive Streamlit dashboard for analyzing e-commerce KPI projections and optimization scenarios for 2026.

## Features

- **📊 Annual Overview**: Interactive visualizations of sales vs spend with ROAS analysis
- **📈 Marginal Returns**: Advanced marginal ROAS analysis with threshold breakdowns  
- **🎯 Scenario Comparison**: Side-by-side comparison of different spend scenarios
- **📋 Data Export**: Complete data table with CSV download functionality
- **🎛️ Interactive Controls**: Dynamic filtering by spend range and ROAS thresholds

## Dashboard Components

### Key Metrics
- Total scenarios analysis
- Maximum annual sales projections
- Best ROAS identification
- Optimal spend recommendations

### Visualizations
- Sales vs Spend scatter plots (colored by ROAS)
- ROAS diminishing returns curves
- Conversion rate trends
- Average order value analysis
- Traffic volume projections
- Marginal returns analysis

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/2026_Scenarios.git
cd 2026_Scenarios
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Dashboard

### Prerequisites
This dashboard requires pre-processed data from a KPI modeling pipeline. The app expects a `streamlit_data.pkl` file containing:
- Annual projections data
- Baseline projections 
- Holiday projections
- Summary metrics
- Data timestamp

### Launch the App

```bash
streamlit run streamlit_kpi_app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

## Data Requirements

The dashboard loads data from `streamlit_data.pkl` which should contain:
- `annual_projections`: DataFrame with annual KPI scenarios
- `baseline_projections`: DataFrame with baseline projections
- `holiday_projections`: DataFrame with holiday-adjusted projections  
- `summary_metrics`: Dictionary of key summary statistics
- `data_timestamp`: Timestamp of when data was generated

## Usage Guide

1. **Adjust Filters**: Use the sidebar to set spend ranges and ROAS thresholds
2. **Explore Analysis Types**: Switch between different analysis views
3. **Compare Scenarios**: Select multiple spend levels for detailed comparison
4. **Export Data**: Download filtered results as CSV for further analysis

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository and the main file (`streamlit_kpi_app.py`)
6. Deploy!

### Deploy to other platforms

This app can also be deployed to:
- Heroku
- Railway
- Render
- Google Cloud Platform
- AWS

## Project Structure

```
2026_Scenarios/
├── streamlit_kpi_app.py    # Main KPI dashboard application
├── app.py                  # Alternative simple dashboard
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── .gitattributes         # Git configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
