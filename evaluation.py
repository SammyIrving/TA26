import pandas as pd
from datetime import datetime

def classify_flow(flow_acc):
    if flow_acc == 100:
        return "F1"
    elif 90 <= flow_acc < 100:
        return "F2"
    else:
        return "F3"

def classify_suture(suture_acc):
    if suture_acc == 100:
        return "S1"
    elif 90 <= suture_acc < 100:
        return "S2"
    else:
        return "S3"

def classify_duration(duration_str):
    try:
        duration = datetime.strptime(duration_str, "%H:%M:%S")
        total_minutes = duration.minute + duration.hour * 60
        if total_minutes < 20:
            return "D1"
        elif total_minutes == 20:
            return "D2"
        else:
            return "D3"
    except Exception as e:
        print("Invalid duration format. Use HH:MM:SS.")
        raise e

def evaluate_performance(flow_acc, suture_acc, duration_str, csv_path="dataset.csv"):
    # Convert raw values to class codes
    flow_code = classify_flow(flow_acc)
    suture_code = classify_suture(suture_acc)
    duration_code = classify_duration(duration_str)

    # Load dataset
    df = pd.read_csv(csv_path)

    # Match row
    match = df[
        (df["Flow"] == flow_code) &
        (df["Suture"] == suture_code) &
        (df["Duration"] == duration_code)
    ]

    # Display result
    if not match.empty:
        print("\nEvaluation:")
        print(match["Evaluation"].values[0])
    else:
        print("No matching evaluation found for the given conditions.")

# 🧪 Example usage
#flow_accuracy = 97.5       # percentage
#suture_accuracy = 88.0     # percentage
#duration_string = "00:21:10"  # HH:MM:SS format


flow_accuracy = float(input("Enter flow accuracy (%) : "))
suture_accuracy = float(input("Enter suture accuracy (%) : "))
duration_string = input("Enter duration (HH:MM:SS) : ")

evaluate_performance(flow_accuracy, suture_accuracy, duration_string)
