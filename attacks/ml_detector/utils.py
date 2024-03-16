import pandas as pd
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from joblib import dump
import pandas as pd
from datetime import datetime
from joblib import load
from collections import Counter
import os


def load_data(path):
    # Load the dataset
    print("Loading data...")
    df = pd.read_csv(path)
    print("Data loaded successfully.")

    # Feature engineering
    print("Starting feature engineering...")
    df["Time"] = pd.to_timedelta(df["Time"], unit="s")
    df["Time"] = pd.to_datetime("today").normalize() + df["Time"]
    df["Packets_Per_Second"] = df.groupby("Source")["Time"].transform(
        lambda x: 1 / x.diff().dt.total_seconds().fillna(0.1)
    )
    df["Packets_Per_Second"] = df["Packets_Per_Second"].clip(upper=1000)

    # Labeling the data
    print("Labeling the data...")

    def label_row(row):
        if "UDP" in row["Protocol"]:
            return "UDP Flood" if row["Packets_Per_Second"] > 10 else "Normal"
        elif "ICMP" in row["Protocol"]:
            return "ICMP Flood" if row["Packets_Per_Second"] > 10 else "Normal"
        elif "TCP" in row["Protocol"]:
            # Check for a pattern of SYN packets without corresponding ACKs to indicate a SYN Flood
            if "[SYN]" in row["Info"] and not "[ACK]" in row["Info"]:
                return "SYN Flood" if row["Packets_Per_Second"] > 10 else "Normal"
            else:
                return "Normal"
        else:
            return "Normal"

    df["Label"] = df.apply(label_row, axis=1)

    # Preprocessing data
    print("Preprocessing data...")
    X = df[["Length", "Packets_Per_Second"]]
    y = df["Label"]

    numeric_features = ["Length", "Packets_Per_Second"]
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[("num", numeric_transformer, numeric_features)]
    )

    return X, y, preprocessor


# Function to parse a single line of Wireshark output
def parse_wireshark_line(line):
    parts = line.strip().split(",")
    if len(parts) < 5 or not parts[0].startswith('"'):
        return None  # Skip lines that are not properly formatted

    timestamp = datetime.fromtimestamp(float(parts[0].strip('"')))
    src_ip = parts[1].strip('"') if parts[1] else "UNKNOWN"
    length = int(parts[2]) if parts[2].isdigit() else 0
    protocol = parts[3].strip('"') if parts[3] else "UNKNOWN"
    info = parts[4].strip('"') if parts[4] else ""

    return {
        "Timestamp": timestamp,
        "Source": src_ip,
        "Length": length,
        "Protocol": protocol,
        "Info": info,
    }


# Function to process the Wireshark output and calculate packets per second
def process_wireshark(file_path):
    data = []
    with open(file_path, "r") as file:
        next(file)  # Skip the header line
        for line in file:
            parsed_line = parse_wireshark_line(line)
            if parsed_line:
                data.append(parsed_line)

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df.sort_values("Timestamp", inplace=True)
    df["Packets_Per_Second"] = df.groupby("Source")["Timestamp"].transform(
        lambda x: 1 / x.diff().dt.total_seconds().fillna(0.1)
    )

    return df[["Length", "Packets_Per_Second"]]
