"""
This module handles the initial user profile setup for the Health Twin.
It calculates base metabolic rates and targets, and initializes the state.json file.
"""

import json
import os

def calculate_daily_target(weight, height, age, activity_level):
    """Calculates the daily calorie target using the Mifflin-St Jeor equation."""
    # BMR Calculation (Mifflin-St Jeor)
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161 
    multipliers = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
    return int(bmr * multipliers.get(activity_level, 1.2))

def create_new_profile():
    """Prompts the user for health data and creates a new state.json profile."""
    print("\n--- 🧬 HEALTH TWIN USER SETUP ---")
    name = input("Enter your name: ")
    weight = float(input("Weight (kg): "))
    height = float(input("Height (cm): "))
    age = int(input("Age: "))
    print("Activity Levels: sedentary, light, moderate, active")
    activity = input("Level: ").lower()

    bmi = round(weight / ((height/100)**2), 1)
    target = calculate_daily_target(weight, height, age, activity)

    profile = {
        "user_profile": {
            "name": name, 
            "weight_kg": weight, 
            "height_cm": height, 
            "bmi": bmi, 
            "daily_calorie_target": target
        },
        "current_day": {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0,
            "sugar": 0,
            "last_meal": "No meals recorded yet."
        }
    }
    with open('state.json', 'w') as f:
        json.dump(profile, f, indent=4)
    print(f"✅ Profile Created for {name}! BMI: {bmi}, Goal: {target}kcal")

if __name__ == "__main__":
    # If the file exists, we ask to overwrite it to ensure the new schema is applied
    if os.path.exists('state.json'):
        print("⚠️  Existing profile found with old schema.")
        choice = input("Do you want to reset and use the new nutrient-tracking schema? (y/n): ").lower()
        if choice == 'y':
            create_new_profile()
        else:
            print("Using existing file (Warning: might cause KeyError if keys are missing).")
    else:
        create_new_profile()