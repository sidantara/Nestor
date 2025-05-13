# Nestor: The Nest Advisor
Capstone Project for MDA 720 - Nestor Real Estate Recommendation Engine

## Overview
Nestor is a data-driven real estate recommendation engine that helps prospective homebuyers identify optimal U.S. states based on their personal lifestyle and financial preferences. Unlike traditional property listing platforms, Nestor provides multi-factor rankings that consider affordability, school quality, safety, employment factors, and healthcare access.

## Key Features
- **Multi-Criteria Desirability Scoring** (Affordability, Education, Safety)
- **User-Defined Filters** (Budget, Bedrooms, School Rating, Crime Rate, Healthcare Access)
- **Interactive Streamlit Dashboard**
- **Real-Time Personalized Rankings**
- **CSV Export of Ranked Results**
- **Visual Insights via Charts and Scorecards**

## Project Structure
Nestor-RealEstate-Advisor/
├── nestor_app.py
├── combined_data_final.csv
├── Recommendations Output.csv
├── Nestor Project Report.pdf
├── README.md


## How to Run the App
1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the Streamlit app:
```
streamlit run nestor_app.py
```

## Dataset Sources
Zillow Research: https://www.zillow.com/research/data/

FRED Economic Data: https://fred.stlouisfed.org/

HUD School Proficiency Index: https://hudgis-hud.opendata.arcgis.com/

FBI Crime Data Explorer: https://cde.ucr.cjis.gov/

Simulated Healthcare Access Data (Prototype)

## Future Enhancements
City or ZIP-level recommendations

Live API integrations

User-weighted scoring options

Machine learning-based personalization

Cloud deployment
