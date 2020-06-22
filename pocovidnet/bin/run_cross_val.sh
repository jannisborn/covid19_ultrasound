#!/bin/bash
python3 scripts/train_covid19.py -t 3 -id 'vgg_cam' -lr 1e-3 -d '../data/cross_validation' -f 0
python3 scripts/train_covid19.py -t 3 -id 'vgg_cam' -lr 1e-3 -d '../data/cross_validation' -f 1
python3 scripts/train_covid19.py -t 3 -id 'vgg_cam' -lr 1e-3 -d '../data/cross_validation' -f 2
python3 scripts/train_covid19.py -t 3 -id 'vgg_cam' -lr 1e-3 -d '../data/cross_validation' -f 3
python3 scripts/train_covid19.py -t 3 -id 'vgg_cam' -lr 1e-3 -d '../data/cross_validation' -f 4

