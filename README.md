# covid_detector
Detecting COVID-19 from medical images


## Installation

The library itself has few dependencies (see [setup.py](setup.py)) with loose requirements. 

To run the code, just install the package `covid_detector` in editable mode for development:

```sh
pip install -e .
```

To run the model on CT data just to:

```sh
python3 covid_detector/train_covid19.py --dataset data_ct
```


## Current performance (POCUS-splitted data):

```
[INFO] evaluating network...
              precision    recall  f1-score   support

       covid       0.98      0.84      0.90        55
   pneunomia       0.90      0.82      0.86        11
     regular       0.57      0.93      0.70        14

    accuracy                           0.85        80
   macro avg       0.81      0.86      0.82        80
weighted avg       0.90      0.85      0.86        80

[[46  1  8]
 [ 0  9  2]
 [ 1  0 13]]
acc: 0.6875
sensitivity: 0.9787
specificity: 1.0000

```


## Current performance (XRAY data):

```
[INFO] evaluating network...
              precision    recall  f1-score   support

       covid       1.00      0.80      0.89         5
      normal       0.83      1.00      0.91         5

    accuracy                           0.90        10
   macro avg       0.92      0.90      0.90        10
weighted avg       0.92      0.90      0.90        10
```