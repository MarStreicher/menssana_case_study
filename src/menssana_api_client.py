import pandas as pd
from typing import List
import requests
import time
import json
import os


class MenssanaApiClient:
    def __init__(
        self,
        api_endpoint: str = "https://idalab-icu.ew.r.appspot.com/history_vital_signs",
        headers: dict = {"accept": "application/json"},
        entries: int = 600,
        file_name: str = "menssana.csv",
        id_column: bool = False,
    ) -> None:
        self.api_endpoint = api_endpoint
        self.headers = headers
        self.entries = entries
        self.file_name = file_name
        self.id_column = id_column
        self.raw_data = []
        self.prepared_data = List[dict[str, dict]]
        self.pandas_data = pd.DataFrame()

    ######################## API interaction #######################################

    def _filter_unique_entries(self) -> List[dict]:
        seen = set()
        unique_entries = []

        for entry in self.raw_data:
            json_entry = json.dumps(entry, sort_keys=True)
            if json_entry not in seen:
                seen.add(json_entry)
                unique_entries.append(entry)
        return unique_entries

    def _connect(self) -> bool:
        try:
            response = requests.get(self.api_endpoint, headers=self.headers)
            if response.status_code == 200:
                dictionary = response.json()
                self.raw_data = self.raw_data + dictionary["patient_list"]
                return True
            else:
                print(f"ERROR - Response code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"ERROR - Request error: {e}")
            return False

    def fetch_data(self) -> List[dict]:
        patience = 0
        while len(self.raw_data) < self.entries:
            connection = self._connect()
            if connection == False:
                patience += 1
                if patience > 3:
                    print(f"ERROR - Stopped data fetch. Too many failed attempts.")
                    break
                continue

            self._filter_unique_entries()
            time.sleep(2)
        self.raw_data = self.raw_data[0 : self.entries]
        return self.raw_data

    ######################## Data preperation #######################################

    def _parse_vital_signs(self) -> List[dict[str, dict]]:
        self.prepared_data = self.raw_data
        for entry in self.prepared_data:
            vital_signs = {}
            vital_signs_list = entry["vital_signs"].split(";")
            for pair in vital_signs_list:
                key, value = pair.split("->")
                vital_signs[key.strip()] = value.strip()

            entry["vital_signs"] = vital_signs
        return self.prepared_data

    def _convert_into_frame(self) -> pd.DataFrame:
        frame = {"patient_id": []}
        for entry in self.prepared_data:
            frame["patient_id"].append(entry["patient_id"])
            for key, value in entry["vital_signs"].items():
                if key not in frame:
                    frame[key] = []
                frame[key].append(value)
        self.pandas_data = pd.DataFrame(frame)
        return self.pandas_data

    def _store_data(self) -> None:
        if self.id_column == False:
            self.pandas_data = self.pandas_data.drop("patient_id", axis=1)

        if os.path.exists(self.file_name):
            print(
                f"WARNING - File '{self.file_name}' already exitsts and will be overwritten."
            )

        self.pandas_data.to_csv(self.file_name, index=False)
        return

    def prepare_data(self) -> None:
        self._parse_vital_signs()
        self._convert_into_frame()
        return self._store_data()


if __name__ == "__main__":
    client = MenssanaApiClient()
    client.fetch_data()
    client.prepare_data()
