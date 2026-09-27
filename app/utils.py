import joblib
import pandas as pd

model = joblib.load(
    "artifacts/models/weight_prediction_model.pkl"
)

feature_columns = joblib.load(
    "artifacts/models/feature_columns.pkl"
)


def predict_weight(
    age,
    height,
    calories,
    calories_burned,
    workout_minutes,
    sleep_hours,
    protein,
    carbs,
    fat
):

    data = pd.DataFrame([{

        "Age": age,
        "HeightCM": height,
        "CaloriesConsumed": calories,
        "CaloriesBurned": calories_burned,
        "WorkoutMinutes": workout_minutes,
        "SleepHours": sleep_hours,
        "ProteinG": protein,
        "CarbsG": carbs,
        "FatG": fat

    }])

    data = data[feature_columns]

    prediction = model.predict(data)[0]

    return prediction