from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from React (port 3000)

# Load model and scaler
model = joblib.load("ai-model/model.pkl")
scaler = joblib.load("ai-model/scaler.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        temperature = float(data.get("suhu", 0))
        humidity = float(data.get("kelembaban", 0))
        co2 = float(data.get("co2", 0))

        # Preprocessing
        X = np.array([[temperature, humidity, co2]])
        X_scaled = scaler.transform(X)

        # Model prediction
        pred = model.predict(X_scaled)[0]

        # Interpretation and AI explanation
        if pred.lower() == "normal":
            recommendation = (
                "Storage conditions are stable. Keep monitoring temperature and humidity "
                "every 12 hours and maintain proper ventilation."
            )
            condition_status = "Storage is safe, no immediate action required."
        elif pred.lower() == "almost rotten" or pred.lower() == "near rotten":
            recommendation = (
                "Start physical inspection at several sample points. "
                "Consider lowering humidity or improving air circulation."
            )
            condition_status = "Potential quality degradation detected. Extra monitoring recommended."
        elif pred.lower() == "rotten" or pred.lower() == "rotten":
            recommendation = (
                "Immediately separate spoiled materials, improve ventilation, "
                "and check the drying or dehumidification system."
            )
            condition_status = "Critical condition! Spoilage process detected."
        else:
            recommendation = "Unable to determine the condition. Please check sensor input."
            condition_status = "Unidentified data."

        # Current condition information
        current_condition = f"Temperature: {temperature}°C | Humidity: {humidity}% | CO₂: {co2} ppm"

        return jsonify({
            "prediction": pred,
            "recommendation": recommendation,
            "current_condition": current_condition,
            "condition_status": condition_status
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
