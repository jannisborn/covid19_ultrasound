# pocovidnet
[![Build Status](https://travis-ci.com/jannisborn/covid19_pocus_ultrasound.svg?branch=master)](https://travis-ci.com/jannisborn/covid19_pocus_ultrasound)
A simple package to train deep learning models on ultrasound data for COVID19.

## Installation

The library itself has few dependencies (see [setup.py](setup.py)) with loose requirements. 

To run the code, just install the package `pocovidnet` in editable mode:

```sh
git clone https://github.com/jannisborn/covid19_pocus_ultrasound.git
cd covid19_pocus_ultrasound/pocovidnet/
pip install -e .
```

## Training the model

*NOTE*: The repository is constantly updated with new data. If you want to
reproduce the results of our paper, use the repo's state of the `arxiv` tag:
```sh
git checkout tags/arxiv
```
Then, please follow the instructions of the `README.md` *at that state* (see
[here](https://github.com/jannisborn/covid19_pocus_ultrasound/tree/6c74e05b5f4ccdf96485eb5030035775d5f5c895/pocovidnet)).

If you want to use the latest version of the database, read below:

### Videos to images

First, we have to merge the videos and images to create an image dataset. 
You can use the script `cross_val_splitter.py` to copy from [pocus images](../data/pocus_images) and [pocus videos](../data/pocus_videos). It will cope the images automatically and process all videos (read the frames and save every x-th frame dependent on the framerate supplied in args).

Note: In the script, it is hard-coded that only convex POCUS data is taken, and only the classes `covid`, `pneumonia`, `regular` (there is not enough data for `viral`yet). You can change this selection in the script.

From the directory of this README, execute:
```sh
python3 scripts/build_image_dataset.py
```

Now, your [data folder](../data) should contain a new folder `image_dataset`
with folders `covid`, `pneumonia`, `regular` and `viral` or a subset of those dependent on your selection.

### Add butterfly data

*NOTE*: The vast majority of data we gathered thus far is available in the 
[data folder](../data).
But unfortunately, not all data used to train/evaluate the model is in this repo
as we do not have the right to host/distribute the data from
[Butterfly](https://butterflynetwork.com).

However, we provide a script that automatically processes the data. To reproduce
the experiments from the paper, please first complete the following steps:

1. Visit the [COVID-19 ultrasound_gallery](https://butterflynetwork.com/covid19/covid-19-ultrasound-gallery)
   of Butterfly, scroll to the bottom and download the videos (we accessed this
   source on 17.04.2020 for training our models. Please note that it is not
   under control whether Butterfly will keep this data online. Feel free to
   notify us if you observe any changes).
2. Place the `.zip` folder into the [data folder](../data).
3. `cd` into the [data folder](../data).
3. Run:
    ```sh
    sh parse_butterfly.sh
    ```
    *NOTE*: This step requires that you installed the `pocovidnet` package
    before (see "Installation").
    
The butterfly images should now be added to `data/image_dataset`.


### Cross validation splitting
The next step is to perform the datat split. You can use the script
`cross_val_splitter.py` to perform a 5-fold cross validation (it will use the data from `data/image_dataset` by default):

From the directory of this README, execute:
```sh
python3 scripts/cross_val_splitter.py --splits 5
```
Now, your [data folder](../data) should contain a new folder `cross_validation`
with folders `fold_1`, `fold_2`. Each folder contains only the test data for
that specific fold.

#### Uninformative data
If you want to add data from an *uninformative* class, see [here](https://github.com/jannisborn/covid19_pocus_ultrasound/tree/master/data#add-class-uninformative).

### Add Butterfly data

As described above, the data from butterfly must be downloaded manually. We provide an automatic script to add the videos to the `data/pocus_videos/convex` folder:

Assuming that you have already downloaded and unzipped the butterfly folder and renamed it to `butterfly`, `cd` into the [data folder](../data).
Then run:
```sh
python ../pocovidnet/scripts/process_butterfly_videos.py  
```
Now all usable butterfly videos should be added to `data/pocus_videos/convex`.

### Train the model

Afterwards you can train the model by:
```sh
python3 scripts/train_covid19.py --data_dir ../data/cross_validation/ --fold 0 --epochs 2
```
*NOTE*: `train_covid19.py` will automatically utilize the data from all other
folds for training.

### Test the model

Given a pre-trained model, it can be evaluated on a cross validations split (`--data`) with the following command:

```sh
python scripts/test.py [-h] [--data DATA] [--weights WEIGHTS] [--m_id M_ID] [--classes CLASSES] [--folds FOLDS] [--save_path SAVE_PATH]
```

## Video classification

We have explored method for video classification to exploit temporal information in the videos. With the following instructions one can train a video classifier based on 3D convolutions.

```sh
python scripts/eval_vid_classifier.py [-h] [--json ../data/video_input_data/cross_val.json] [--genesis_weights GENESIS_WEIGHTS][--cam_weights CAM_WEIGHTS] [--videos ../data/pocus_videos/convex]
```

A [json file](../data/video_input_data/cross_val.json) is provided that corresponds to the cross validation split in `data/cross_validation`. To train a 3D CNN on a split, `cd` into the folder of this README and run
```sh
python scripts/video_classification.py --output models --fold 0 --epoch 40  
```

The models will be saved to the directory specified in the `output` flag.

## Our results (`POCOVID-Net`)

Current results (5-fold CV) are

| Model                  | Accuracy  |      Balanced | 
| ------------------ |---------------- | -------------- |
| VGG  |     89.7%  +- 5%       |      89.6% +- 5%
| VGG-CAM  |     89.5% +-2%     |      88.1%  +- 3% 
| NASNetMobile  |     75.7% +-9%     |      71.1%  +- 7% 

![alt text](https://github.com/jannisborn/covid19_pocus_ultrasound/blob/master/pocovidnet/plots/confusion_matrix.png "Confusion matrix")

Detailed performances:
![alt text](https://github.com/jannisborn/covid19_pocus_ultrasound/blob/master/pocovidnet/plots/result_table.png "Result table")

### Pretrained models
To access the pre-trained models, have a look [here](https://drive.google.com/drive/folders/1c_B4V-Ejs45pVyl1QNPEXgT4_Kg0o-Lt). The default configuration in the evaluation class `Evaluator` in `evaluate_covid19.py` uses the `vgg_base` model which is stored in the Google Drive folder `trained_models_vgg`. You can place the 5 folders named `fold_1` ... `fold_5` into `pocovidnet/trained_models` and should be ready to go to use the `Evaluator` class.


# Contact 
- If you experience problems with the code, please open an
[issue](https://github.com/jannisborn/covid19_pocus_ultrasound/issues).
- If you have questions about the project, please reach out: `jborn@ethz.ch`.


# Citation

The paper is available [here](https://arxiv.org/abs/2004.12084).

If you build upon our work or find it useful, please cite our paper:
```bib
@article{born2020pocovid,
  title={POCOVID-Net: Automatic Detection of COVID-19 From a New Lung Ultrasound Imaging Dataset (POCUS)},
  author={Born, Jannis and Br{\"a}ndle, Gabriel and Cossio, Manuel and Disdier, Marion and Goulet, Julie and Roulin, J{\'e}r{\'e}mie and Wiedemann, Nina},
  journal={arXiv preprint arXiv:2004.12084},
  year={2020}
}
```