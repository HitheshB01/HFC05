from sklearn.ensemble import IsolationForest
import numpy as np

def detect_anomalies(data):
    try:
        clf = IsolationForest(contamination=0.1)
        clf.fit(data.reshape(-1, 1))

        anomalies = clf.predict(data.reshape(-1, 1))
        return anomalies
    except Exception as e:
        print("Error in detecting anomalies:")
        print(e)
        return None