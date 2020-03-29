# Automatic detection of COVID-19 from POCUS ultrasound images

### Here, we gather ultrasound data (POCUS) from human lungs, especially from COVID 19 patients. Detecting COVID-19 from POCUS is challenging and time-consuming, even for trained medical doctors. Since the time of doctors is scarce, there is an urgent need to simplify, fasten & automatize the detection of COVID-19, especially non-invasively.  

## Please contribute your own images here or tell us directly where to find them. 

## Here is the current performance of our model (POCUS-splitted data):
*Disclaimer: The model is in a very preliminary stage and was not trained in a scientifically rigorous way.*

Recall = Sensitivity 

Precision = Specificity

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


### COVID
![COVID](data_pocus-splitted/train/covid/Cov-Atlas+(44).gif_frame4.jpg)  
### Pneunomia
![Pneunomia](data_pocus-splitted/train/pneunomia/Pneu-Atlas-pneumonia.gif_frame0.jpg)
### Sane
![Sane](data_pocus-splitted/train/regular/Reg-Atlas.gif_frame0.jpg)




## Installation

The library itself has few dependencies (see [setup.py](setup.py)) with loose requirements. 

To run the code, just install the package `covid_detector` in editable mode for development:

```sh
pip install -e .
```

To run the model on CT data just to:

```sh
python3 covid_detector/train_covid19.py --dataset data_pocus-splitted
```
