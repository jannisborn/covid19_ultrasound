# Accelerating COVID-19 Detection with ExplainableUltrasound Image Analysis

This codebase is the official implementation of our submission **Accelerating COVID-19 Detection with ExplainableUltrasound Image Analysis**.

## Requirements

The library itself has few dependencies (see [setup.py](setup.py)) with loose requirements. 

To run the code, just install the package `pocovidnet` in editable mode:

```sh
git clone https://github.com/jannisborn/covid19_pocus_ultrasound.git
cd covid19_pocus_ultrasound/pocovidnet/
pip install -e .
```

Packages that will be installed include OpenCV, Tensorflow, Scikit-learn and Matplotlib.

## Dataset

We provide the largest dataset of lung POCUS videos and images. It contains samples from convex and linear probes:

- Convex:
  - 86 videos (40x COVID, 23x bacterial pneumonia, 20x healthy, 3x viral pneumonia)
  - 28 images (16x COVID, 7x bacterial pneumonia, 5x healthy)
- Linear: 
  - 20 videos (4x COVID, 2x bacterial pneumonia, 10x healthy, 4x viral pneumonia)
  - 5 images (3x COVID, 2x bacterial pneumonia)


In order to train the model on this data, a folder containing our cross validation split can be downloaded [here](https://drive.google.com/file/d/1E9Cih7QdZNhaD7ns9sPcx7zOCBTYF-Wb/view?usp=sharing). Download the directory into the [data folder](../data) and unzip it. **Note: In this case, all further steps until the train-section can be skipped**

Otherwise, the data can be collected, pre-processed and split with the steps explained in the following. Note that in this case the split will be different,
since the splitting procedure is non-deterministic, and thus the results might vary.

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

In order to detect out of distribution samples we decided to include a fourth class called "uninformative", where we add Imagenet images and neck-ultrasound data from the Kaggle Nerve Segmentation Challenge.

Download the data [here](https://drive.google.com/open?id=1bAbCJCq-U5vIxbG0ySUKanAW_pW_z2O4) from google drive. It contains a folder *uniform_class_nerves* and one *uniform_class_imagenet*. These two folders need to be downloaded into the [data folder](../data), and can be directly used for training there.

If you want to add them to an existing cross validation split (e.g after executing [cross_val_splitter](../pocovidnet/scripts/cross_val_splitter.py)), we also provide a script:

Run (from the directory of this README):
```
cd ../data
python ../pocovidnet/scripts/add_uninformative_class.py -i uniform_class_imagenet -u uniform_class_nerves -o cross_validation -s 5
```

This script will split the data in the *uniform_class_nerves* and *uniform_class_imagenet* folders and add them in a folder *uninformative* to each fold.

## Train the model

Given an existing cross validation folder, train the model on fold 0 by running:
```sh
python3 scripts/train_covid19.py --data_dir ../data/cross_validation/ --fold 0 --epochs 20
```
*NOTE*: `train_covid19.py` will automatically utilize the data from all other
folds for training.

To reproduce the results reported in our submission, run the script with the following parameters:

```sh
python scripts/train_covid19.py -d ../data/cross_validation/ -t 0
    -m models/ -id 'vgg_base' -lr 1e-3 -e 40 -bs 8 -ls True
```

## Video classification

We have explored method for video classification to exploit temporal information in the videos. With the following instructions one can train a video classifier based on 3D convolutions.

#### Add Butterfly data

As described above, the data from butterfly must be downloaded manually. We provide an automatic script to add the videos to the `data/pocus_videos/convex` folder:

Assuming that you have already downloaded and unzipped the butterfly folder and renamed it to `butterfly`, `cd` into the [data folder](../data).
Then run:
```sh
python ../pocovidnet/scripts/process_butterfly_videos.py  
```
Now all usable butterfly videos should be added to `data/pocus_videos/convex`.

#### Train video classifier

A [json file](../data/video_input_data/cross_val.json) is provided that corresponds to the cross validation split in `data/cross_validation`. The followings script will automatically process the data listed in this json file. There are two video classification model: A simple 3D CNN that is trained from scratch (--model_id base) or a pre-trained 3D CNN provided by Models Genesis (--model_id genesis). For the latter, the pre-trained model needs to be requested [here](https://www.wjx.top/jq/46747127.aspx).

To reproduce the reported video classification results with model genesis, `cd` into the folder of this README and run
```sh
python scripts/video_classification.py --model_id genesis
```

The models will be saved to the directory specified in the `output` flag.

## Evaluation

#### Pre-trained models and input data

**All models and data can be downloaded [here](https://drive.google.com/drive/folders/1c_B4V-Ejs45pVyl1QNPEXgT4_Kg0o-Lt?usp=sharing)**
To reproduce our results, download the trained models, as well as our cross validation split.

#### Test

General usage of test script:

```sh
python scripts/test.py [-h] [--data DATA] [--weights WEIGHTS] [--m_id M_ID] [--classes CLASSES] [--folds FOLDS] [--save_path SAVE_PATH]
```

To reproduce our evaluation, download the trained_models folder from Drive and put them into the directory of this README (pocovidnet). Also, download the cross validation split folder and unzip it in the [data](../data) folder (see paths in commands below).

The first three models use the raw data as input, which is in the [cross_validation](../data/cross_validation) folder

VGG-model:
```sh
python scripts/test.py --data ../data/cross_validation --weights trained_models_vgg --m_id vgg_base --save_path results_VGG
```
VGG-CAM-model:
```sh
python scripts/test.py --data ../data/cross_validation --weights trained_models_cam --m_id vgg_cam --save_path results_VGG_CAM
```
NASNet-model:
```sh
python scripts/test.py --data ../data/cross_validation --weights trained_models_NAS --m_id nasnet --save_path results_NAS
```

The other two models are trained on segmented images or encoding layers, which are provided in the [cross_validation_segmented](../data/cross_validation_segmented) folder.

VGG-Segment:
```sh
python scripts/test.py --data ../data/cross_validation_segmented --weights trained_models_vgg_segment --m_id vgg_base --save_path results_segment
```
Segment-Enc:
```sh
python scripts/test.py --data ../data/cross_validation_segmented --weights trained_models_encoding --m_id dense --save_path results_encode
```

All results will be dumped as .dat files containing the raw logits, as well as csv files with tables containing the results in the specified save_path location (in this case, in the files results_encode.dat, results_encode_mean.csv and results_encode_std.csv etc). Both results with and without the uninformative class will be produced (indicated by _3 added to the file name).

## Results

Frame-based classification results obtained in 5-fold cross validation:

| Model                  | Accuracy  |      Balanced | 
| ------------------ |---------------- | -------------- |
| VGG  |     89.7%  +- 5%       |      89.6% +- 5%
| VGG-CAM  |     89.5% +-2%     |      88.1%  +- 3% 
| NASNetMobile  |     75.7% +-9%     |      71.1%  +- 7% 

When averaging the frame-wise probabilities to obtain a video classification, VGG-CAM achieves 94% accuracy (93% balanced).

The video classification model using 3D convolutions described above, Model Genesis, meanwhile exhibits 87% accuracy.