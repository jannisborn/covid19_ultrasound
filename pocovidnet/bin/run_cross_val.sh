#!/bin/bash
python3 pocovidnet/train_covid19.py --dataset '../data/pocus/cross_validation' --split 0
python3 pocovidnet/train_covid19.py --dataset '../data/pocus/cross_validation' --split 1
python3 pocovidnet/train_covid19.py --dataset '../data/pocus/cross_validation' --split 2
python3 pocovidnet/train_covid19.py --dataset '../data/pocus/cross_validation' --split 3
python3 pocovidnet/train_covid19.py --dataset '../data/pocus/cross_validation' --split 4

