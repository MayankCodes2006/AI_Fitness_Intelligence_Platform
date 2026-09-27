"""
==============================================================
Project    : AI Fitness Intelligence Platform

Module     : Weight Prediction

Author     : Mayank Khandelwal

Description:
Loads the trained Random Forest model and predicts
user weight based on fitness and nutrition features.
==============================================================
"""

from pathlib import Path

import joblib
import pandas as pd

from src.utils.logger import logger


# ======================================================
# Model Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "artifacts"
    / "models"
    / "weight_prediction_model.pkl"
)

FEATURE_PATH = (
    BASE_DIR
    / "artifacts"
    / "models"
    / "feature_columns.pkl"
)


# ======================================================
# Load Model
# ======================================================

try:

    model = joblib.load(MODEL_PATH)

    feature_columns = joblib.load(FEATURE_PATH)

    logger.info("Weight prediction model loaded successfully.")

except Exception as e:

    logger.exception("Failed to load ML model.")

    raise RuntimeError(
        f"Unable to load model artifacts.\n{e}"
    )


# ======================================================
# Prediction Function
# ======================================================

def predict_weight(
    age: int,
    height_cm: float,
    calories_consumed: float,
    calories_burned: float,
    workout_minutes: float,
    sleep_hours: float,
    protein: float,
    carbs: float,
    fat: float
) -> float:

    """
    Predict user's weight.

    Returns
    -------
    float
        Predicted weight in KG.
    """

    # --------------------------------------------
    # Basic Validation
    # --------------------------------------------

    if age <= 0:
        raise ValueError("Age must be greater than 0.")

    if height_cm <= 0:
        raise ValueError("Height must be greater than 0.")

    if calories_consumed < 0:
        raise ValueError("Calories consumed cannot be negative.")

    if calories_burned < 0:
        raise ValueError("Calories burned cannot be negative.")

    if workout_minutes < 0:
        raise ValueError("Workout minutes cannot be negative.")

    if sleep_hours <= 0:
        raise ValueError("Sleep hours must be greater than 0.")

    if protein < 0 or carbs < 0 or fat < 0:
        raise ValueError("Macronutrients cannot be negative.")

    # --------------------------------------------
    # Create DataFrame
    # --------------------------------------------

    input_data = pd.DataFrame(
        [
            {
                "Age": age,
                "HeightCM": height_cm,
                "CaloriesConsumed": calories_consumed,
                "CaloriesBurned": calories_burned,
                "WorkoutMinutes": workout_minutes,
                "SleepHours": sleep_hours,
                "ProteinG": protein,
                "CarbsG": carbs,
                "FatG": fat
            }
        ]
    )

    # --------------------------------------------
    # Match Training Features
    # --------------------------------------------

    input_data = input_data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # --------------------------------------------
    # Prediction
    # --------------------------------------------

    prediction = model.predict(input_data)[0]

    prediction = round(float(prediction), 2)

    logger.info(
        f"Weight Prediction Successful : {prediction} KG"
    )

    return prediction


# ======================================================
# Testing
# ======================================================

if __name__ == "__main__":

    try:

        predicted_weight = predict_weight(

            age=25,
            height_cm=175,

            calories_consumed=2300,
            calories_burned=500,

            workout_minutes=60,

            sleep_hours=8,

            protein=140,
            carbs=250,
            fat=60
        )

        print("=" * 60)
        print(f"Predicted Weight : {predicted_weight} KG")
        print("=" * 60)

    except Exception as e:

        print("=" * 60)
        print("Prediction Failed")
        print(e)
        print("=" * 60)