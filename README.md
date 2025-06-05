# MensSana Case Study

Aim: Reducing the false positives device alarms in ICUs.

- ICUs == Intensive Care Unit
- Average ICU takes care of 18 patients
- For every ICU patient, about 100 alarms are raised per day


## Menssana API Client

### Menssana REST API

**REST API:**
Representational state Transfer, communication over the web using standard HTTP methods (GET, POST, PUT/PATCH (Update data), DELETE)

- Api documentation done with FastAPI
- Language is most likely python
- Appspot == Google App Engine (supports python apps), API is running on Google servers

Get request:
```
curl -X 'GET' \
  'https://idalab-icu.ew.r.appspot.com/history_vital_signs' \
  -H 'accept: application/json'
```

**curl:**
Tool for making HTTP requests from the command line

**-X 'GET':**
Request type

**'http: ....':**
URL of the API endpoint

**-H 'accept: application/json':**
Please send the response in json format


- Library for python: requests
- Headers == is a label or tag added to an HTTP request or response (metadata)
- Pooling == Repeatedly sending GET requests every few seconds to check if new data is available

### Task:

1. Connect to API of the hospital
2. Fetch the raw real-time vital signs continuosly coming from the API
3. Transform the data
4. Store data in appropriate format


### Custom 

Environment:
```
conda activate env_menssana
```

## Evaluation of the models

| medical_emergency | monitor_alarm  | Expected result | category |
|------------|------------|------------|---------|
| F| F| low probability | true negative |
| F| T| low probability | false positive |
| T| F| high probability (Aim?)| false negative|
| T| T| high probability| true positive |

- Special case: There is a medical emergency but no monitore alarm.
- Problem here: 12 cases - but not really the aim
- The aim is to detect false positive ones but not to be better than the monitor, right?
- Should be a criterion in the evaluation


