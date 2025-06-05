import numpy as np
import pandas as pd
from typing import List, Optional


class EvaluationData:
    def __init__(
        self,
        file_path: str = "../data/solutions_case_study_task2_data.csv",
        columns: Optional[List[str]] = None,
    ) -> None:
        self.file_path = file_path
        self.columns = columns

        self.raw_data = pd.read_csv(file_path)
        self.data = self._add_bool_label()
        self.data = self._add_alarm_category()
        if columns:
            self.data = self._filter_columns()

    def _add_bool_label(self):
        prob_columns = {
            "ai_model1_alarm_probability": "ai_model1_alarm",
            "ai_model2_alarm_probability": "ai_model2_alarm",
            "ai_model3_alarm_probability": "ai_model3_alarm",
        }

        for prob_col, bool_col in prob_columns.items():
            if prob_col in self.raw_data.columns:
                self.raw_data[bool_col] = self.raw_data[prob_col] >= 0.5
        return self.raw_data

    def _add_alarm_category(self):
        def _compute_category(row):
            if row["medical_emergency"] == True and row["monitor_alarm"] == True:
                return "true positive"
            elif row["medical_emergency"] == False and row["monitor_alarm"] == False:
                return "true negative"
            elif row["medical_emergency"] == True and row["monitor_alarm"] == False:
                return "false negative"
            elif row["medical_emergency"] == False and row["monitor_alarm"] == True:
                return "false positive"
            else:
                return np.nan

        self.data["category"] = self.data.apply(_compute_category, axis=1)
        return self.data

    def _filter_columns(self):
        return self.raw_data[self.columns]

    def filter_monitor_false_negative(self) -> "EvaluationData":
        self.data = self.data[self.data["category"] != "false negative"]
        return self
