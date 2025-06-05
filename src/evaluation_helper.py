import pandas as pd


class EvaluationHelper:
    def __init__(self):
        pass

    @classmethod
    def get_false_positive_rate(cls, data: pd.DataFrame, model_column: str):
        fp = len(
            data[(data["medical_emergency"] == False) & (data[model_column] == True)]
        )
        tn = len(
            data[(data["medical_emergency"] == False) & (data[model_column] == False)]
        )

        if (fp + tn) == 0:
            return 0.0

        fpr = fp / (fp + tn)
        return fpr
