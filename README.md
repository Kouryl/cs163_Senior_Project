# CS163 Senior Project
 Repo for CS 163 project
 [Website link](https://evenergy163.uw.r.appspot.com)

 ## Project Overview

 We analyzed monthly EV charging sessions and energy delivered across Pacific-region metros to uncover growth trends and seasonal cycles. Historical gasoline and electricity rates were converted into a common cost-per-mile metric to compare operating costs, and we examined both their short-term volatility and long-term co-movement. We then used 39 months of historical energy data to forecast next year’s Pacific-region electricity demand using Facebook Prophet which handles non-stationary seasonal patterns.

## Broader Impacts

Understanding EV adoption trends enables utilities and policymakers to assess energy demand on local distribution networks guiding upgrades to substations, feeders, and fast-charging stations. Metro‐area growth maps reveal which Pacific-region corridors will experience the fastest EV uptake, guiding strategic placement of new fast-charging stations. Five-year forecasts of energy prices could allow a more accurate budget setting, hedging strategies, and investment timing.

## Pipeline

### 1. Problem Definition
- **Objective**: Analyze EV adoption trends, forecast growth, and assess infrastructure and cost factors.
- **Key Questions**:
  - How is EV adoption changing over time and by region?
  - Where is additional charging infrastructure needed?
  - Is EV ownership more cost-effective than gasoline vehicles?

### 2. Data Collection
- Sources:
  - Electricity and gasoline price data (2000–2024)
  - Public EV charging station data from EVWatts (2019-2022)
- Methods: CSV import and data merging

### 3. Data Cleaning and Preprocessing
- Removed missing or inconsistent entries
- Standardized date formats and units
- Merged EV session data with EVSE data

### 4. Exploratory Data Analysis (EDA)
- Visualized trends in EV growth over time and across regions
- Investigated correlations between electric and gas price trends
- Forecasted future electric and gas prices.
- Forecasted future energy usage in the Pacific region

### 5. Feature Engineering
- Created additional metrics:
  - Annual fuel cost and electric rate comparison
  - 

### 6. Modeling and Prediction
- Applied regression and time series models to:
  - Forecast EV growth in the Pacific region using charging ssession counts and energy usage.
  - Estimate electricity and fuel prices

### 7. Evaluation and Interpretation
- Validated model predictions against historical data
- Generated insights to support infrastructure and policy planning

### 8. Visualization and Communication
- Built clear plots and charts using matplotlib and Plotly
- Included geographic and statistical visuals

### 9. Deployment
- Delivered results interactive web dashboard
  - Website uses plotly for visualization, and loads images of plots for large datasets.

## SETUP Instructions

run the command below with gcloud in the repo directory, to create website.
```
gcloud app deploy
```

## Project Directories

- website - folder for making website
- notebook - folder for notebooks for analysis
