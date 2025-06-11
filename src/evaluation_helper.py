from turtle import color
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve
from evaluation_data import EvaluationData
from typing import List, Optional
import numpy as np
import matplotlib.pyplot as plt


class EvaluationHelper:
    def __init__(self, data: pd.DataFrame, models: Optional[List[str]] = None):
        self.data = data
        self.models = (
            ["ai_model1_alarm", "ai_model2_alarm", "ai_model3_alarm", "monitor_alarm"]
            if models is None
            else models
        )
        self.probability_models = [
            col for col in data.columns if col.endswith("_alarm_probability")
        ]

    def get_false_positive_rate(self):
        fprs = {}
        for model in self.models:
            fp = len(
                self.data[
                    (self.data["medical_emergency"] == False)
                    & (self.data[model] == True)
                ]
            )
            tn = len(
                self.data[
                    (self.data["medical_emergency"] == False)
                    & (self.data[model] == False)
                ]
            )

            if (fp + tn) == 0:
                fprs[model] = np.nan
            else:
                fprs[model] = round(fp / (fp + tn), 2)
        return fprs

    def get_true_positive_rate(self):
        tprs = {}
        for model in self.models:
            tp = len(
                self.data[
                    (self.data["medical_emergency"] == True)
                    & (self.data[model] == True)
                ]
            )
            fn = len(
                self.data[
                    (self.data["medical_emergency"] == True)
                    & (self.data[model] == False)
                ]
            )

            if (tp + fn) == 0:
                tprs[model] = np.nan
            else:
                tprs[model] = round(tp / (tp + fn), 2)
        return tprs

    def get_true_negative_rate(self):
        tnrs = {}
        for model in self.models:
            tn = len(
                self.data[
                    (self.data["medical_emergency"] == False)
                    & (self.data[model] == False)
                ]
            )
            fp = len(
                self.data[
                    (self.data["medical_emergency"] == False)
                    & (self.data[model] == True)
                ]
            )

            if (tn + fp) == 0:
                tnrs[model] = np.nan
            else:
                tnrs[model] = round(tn / (tn + fp), 2)
        return tnrs

    def get_accuracy(self):
        accuracies = {}
        for model in self.models:
            accuracies[model] = round(
                sum(self.data["medical_emergency"] == self.data[model])
                / len(self.data),
                2,
            )

        return accuracies

    def plot_roc_auc_curve(self, best_threshold: bool = False):
        def _get_best_threshold(thresholds, trp):
            return np.where(trp >= 0.89)[0][0]

        plt.figure(figsize=(8, 6))
        for model in self.probability_models:
            auc = roc_auc_score(
                self.data["medical_emergency"].astype(int), self.data[model]
            )
            fpr, trp, thresholds = roc_curve(
                self.data["medical_emergency"].astype(int), self.data[model]
            )

            if best_threshold:
                index = _get_best_threshold(thresholds, trp)
                print(f"{model}: {thresholds[index]}")
            else:
                index = np.argmin(np.abs(thresholds - 0.5))

            names = model.split("_")
            plt.plot(fpr, trp, label=f"{names[1]} (AUC = {round(auc,2)})")
            plt.scatter(fpr[index], trp[index], color="red")

        plt.plot([0, 1], [0, 1], "k--", label="Chance")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.show()
        return
