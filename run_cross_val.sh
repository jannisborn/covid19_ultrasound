#!/bin/bash

python3 covid_detector/train_covid19.py --dataset "data_pocus/cross_validation_data" --split 0
python3 covid_detector/train_covid19.py --dataset "data_pocus/cross_validation_data" --split 1
python3 covid_detector/train_covid19.py --dataset "data_pocus/cross_validation_data" --split 2
python3 covid_detector/train_covid19.py --dataset "data_pocus/cross_validation_data" --split 3
python3 covid_detector/train_covid19.py --dataset "data_pocus/cross_validation_data" --split 4