import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
    accuracy_score,
    confusion_matrix,
)
from joblib import dump
import pandas as pd
from datetime import datetime
from joblib import load
from collections import Counter
import os
import matplotlib.pyplot as plt


class AttackDetector:
    def train(self, X, y, preprocessor):
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=100, random_state=42, class_weight="balanced"
                    ),
                ),
            ]
        )

        # Splitting data into training and testing sets
        print("Splitting data into training and testing sets...")
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )

        # Training the model
        print("Training the model...")
        pipeline.fit(X_train, y_train)

        # Saving the model to disk
        model_filename = "attacks/ml_detector/trained_model.joblib"
        dump(pipeline, model_filename)
        print(f"Model saved to {model_filename}.")

        # Making predictions on the test set
        print("Making predictions on the test set...")
        y_pred = pipeline.predict(X_val)

        # Evaluating the model's performance
        print("Evaluating model performance...")
        print(classification_report(y_val, y_pred))
        print(f"Model accuracy: {accuracy_score(y_val, y_pred)}")
        fig, axes = plt.subplots(1, 1, figsize=(8, 5), sharey="row")
        cm = confusion_matrix(y_val, y_pred, labels=pipeline.classes_)
        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=pipeline.classes_
        )
        disp.plot(ax=axes)
        fig.savefig("attacks/ml_detector/cm.png")
        plt.close()
        print("Model training and evaluation complete.")

    def test(self, data):
        model = load("attacks/ml_detector/trained_model.joblib")
        if data.empty:
            print("No valid data found in Wireshark output.")
        else:
            print("Making predictions on Wireshark data...")
            predictions = model.predict(data)

            print("Analyzing predictions...")
            packet_counts = Counter(predictions)

            print("Summary of packets:")
            for packet_type, count in packet_counts.items():
                print(f"Total number of '{packet_type}' packets: {count}")

            # Define thresholds for each attack type
            attack_thresholds = {
                "UDP Flood": 100,
                "ICMP Flood": 100,
                "TCP Flood": 100,  # Example threshold, adjust based on your criteria
            }

            # Alert for each attack type based on its threshold
            for attack_type, threshold in attack_thresholds.items():
                if packet_counts[attack_type] > threshold:
                    print(
                        f"ALERT: Possible {attack_type} detected with {packet_counts[attack_type]} packets!"
                    )
