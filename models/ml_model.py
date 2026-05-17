import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

def train_models():

    data = pd.read_csv("student_stress.csv")

    X = data.drop("stress", axis=1)

    y = data["stress"]

    rf = RandomForestClassifier(
        n_estimators=100
    )

    svm = SVC(
        probability=True
    )

    rf.fit(X, y)

    svm.fit(X, y)

    return rf, svm