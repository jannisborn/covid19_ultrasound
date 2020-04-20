# pocovidnet

A simple package to train deep learning models on POCUS data for COVID19.

## Installation

The library itself has few dependencies (see [setup.py](setup.py)) with loose requirements. 

To run the code, just install the package `covid_detector` in editable mode for development:

```sh
pip install -e .
```

To run the model you should split the data first. You can use the script `cross_val_splitter.py` like this:

```sh
python3 covid_detector/train_covid19.py --dataset data_pocus-splitted
```

Afterwards you can train the model by:
```sh
python3 covid_detector/train_covid19.py --dataset data_pocus-splitted
```
