from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(_name_)

TARGET_NUTRIENTS = {'N': 100, 'P': 60, 'K': 80, 'S': 50}
FERTILIZER_COSTS = {'N': 0.5, 'P': 0.7, 'K': 0.6, 'S': 0.4}
FERTILIZER_EFFICIENCIES = {'N': 0.8, 'P': 0.75, 'K': 0.7, 'S': 0.65}

CROP_REQUIREMENTS = {
    'Wheat': {'N': 80, 'P': 40, 'K': 60, 'S': 40},
    'Corn': {'N': 120, 'P': 50, 'K': 100, 'S': 50},
    'Soybean': {'N': 60, 'P': 30, 'K': 40, 'S': 30},
    'Rice': {'N': 100, 'P': 60, 'K': 80, 'S': 50},
    'Barley': {'N': 90, 'P': 35, 'K': 65, 'S': 45},
    'Oats': {'N': 85, 'P': 45, 'K': 55, 'S': 40},
 
}

def calculate_fertilizer_need(soil_data):
    for nutrient in TARGET_NUTRIENTS:
        if nutrient in soil_data.columns:
            soil_data[f'{nutrient}_deficit'] = TARGET_NUTRIENTS[nutrient] - soil_data[nutrient]
        else:
            soil_data[f'{nutrient}_deficit'] = TARGET_NUTRIENTS[nutrient]
        soil_data[f'{nutrient}_amount_needed'] = soil_data[f'{nutrient}_deficit'] / FERTILIZER_EFFICIENCIES[nutrient]
        soil_data[f'{nutrient}_cost'] = soil_data[f'{nutrient}_amount_needed'] * FERTILIZER_COSTS[nutrient]
    soil_data['Total_cost'] = soil_data[[f'{nutrient}_cost' for nutrient in TARGET_NUTRIENTS]].sum(axis=1)
    soil_data['Total_fertilizer_amount'] = soil_data[[f'{nutrient}_amount_needed' for nutrient in TARGET_NUTRIENTS]].sum(axis=1)
    return soil_data

def recommend_crops(soil_data):
    def crop_recommendation(row):
        recommendations = []
        for crop, requirements in CROP_REQUIREMENTS.items():
            if all(row[nutrient] >= requirements[nutrient] for nutrient in requirements):
                recommendations.append(crop)
        return ', '.join(recommendations)
    soil_data['Recommended_crops'] = soil_data.apply(crop_recommendation, axis=1)
    return soil_data