#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, "..")
from collections import Counter

from joblib import load
from sklearn.metrics import (
    confusion_matrix,
)

from ml_detector.utils import load_data

flood_attack_csv_filenames = [
    "SYN.csv",
    "udp_flood.csv",
]

methods = [
    "RF",
    "SVM",
    "LR",
    "KNN",
]


label_to_num = {
    "Normal": "Normal",
    "UDP Flood": "DoS",
    "ICMP Flood": "DoS",
    "SYN Flood": "DoS",
}


def format_y(y: list) -> list:
    y = [label_to_num[label] for label in y]
    return y


def count_y(y):
    print("Analyzing...")
    packet_counts = Counter(y)
    print("Summary of packets:")
    for packet_type, count in packet_counts.items():
        print(f"Total number of '{packet_type}' packets: {count}")


def main():
    for filename in flood_attack_csv_filenames:
        print("=====================================")
        print(f"Reading flooding attack {filename}...")
        print("=====================================")
        X, y, _ = load_data(filename)
        y = format_y(y)
        count_y(y)
        for method in methods:
            print(f"Using method: {method}")
            model = load(f"../ml_detector/trained_model_{method}.joblib")
            print("Making predictions on Wireshark data...")
            y_pred = model.predict(X)
            y_pred = format_y(y_pred)
            count_y(y_pred)

            # Evaluating the model's performance
            print("Evaluating model performance...")

            # Postive: DoS Negative: Normal
            cm = confusion_matrix(y, y_pred)
            tp, fn = cm[0]
            fp, tn = cm[1]
            accuracy = (tp + tn) / (tp + fp + tn + fn)
            tpr = tp / (tp + fn)
            fpr = fp / (fp + tn)
            fnr = fn / (tp + fn)
            print(f"Accuracy: {accuracy}")
            print(f"True Positive Rate: {tpr}")
            print(f"False Positive Rate: {fpr}")
            print(f"False Negative Rate: {fnr}")


if __name__ == "__main__":
    main()
