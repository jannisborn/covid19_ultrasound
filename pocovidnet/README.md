# pocovidnet
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![build](https://github.com/jannisborn/covid19_ultrasound/actions/workflows/build.yml/badge.svg)](https://github.com/jannisborn/covid19_ultrasound/actions/workflows/build.yml)

A simple package to train deep learning models on ultrasound data for COVID19.

## Train/test split
**Due to multiple papers that used our dataset incorrectly, we are adding the following disclaimer: Please make sure to create a meaningful train/test data split. Do not split the data on a frame-level, but on a video/patient-level. The task becomes trivial otherwise because consecutive LUS frames are extremely correlated. We provide scripts to create a cross-validation split for you. See the instructions [here](#cross-validation-splitting).**

## Installation

The library itself has few dependencies (see [setup.py](setup.py)) with loose requirements. 

To run the code, just install the package `pocovidnet` in editable mode:

```sh
git clone https://github.com/BorgwardtLab/covid19_ultrasound.git
cd covid19_ultrasound/pocovidnet/
pip install -e .
```

## Training the model
### Set up database
A lot of data is directly provided in this repository in the [data folder](../data).

#### Web data
Parts of our database are videos/images from online sources that are not licensed for redistribution. This includes publications with restrictive licenses (e.g. from Elsevier) or data from commercial websites. These samples are not provided within our repo but we provide a script to download and preprocess this data automatically:
```sh
cd ../data
sh get_and_process_web_data.sh
```
This will take a while, but afterwards more data will be in the [data folder](../data).

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

## Our results 
To see our results, please have a look at our [paper](https://www.mdpi.com/2076-3417/11/2/672).

### Pretrained models
To access the pre-trained models, have a look [here](https://drive.google.com/drive/folders/1c_B4V-Ejs45pVyl1QNPEXgT4_Kg0o-Lt). The default configuration in the evaluation class `Evaluator` in `evaluate_covid19.py` uses the `vgg_base` model which is stored in the Google Drive folder `trained_models_vgg`. You can place the 5 folders named `fold_1` ... `fold_5` into `pocovidnet/trained_models` and should be ready to go to use the `Evaluator` class.


# Contact 
- If you experience problems with the code, please open an
[issue](https://github.com/jannisborn/covid19_pocus_ultrasound/issues).
- If you have questions about the project, please reach out: `jannis.born@gmx.de`.


# Citation
An [abstract of our work was published](https://thorax.bmj.com/content/76/Suppl_1/A230.2) in *Thorax* as part of the BTS Winter Meeting 2021. 
The full paper is available via the COVID-19 special issue of [Applied Sciences](https://www.mdpi.com/2076-3417/11/2/672).
Please cite these in favor of our deprecated [POCOVID-Net preprint](https://arxiv.org/abs/2004.12084).

Please use the following bibtex entries:
```bib
@article{born2021accelerating,
  title={Accelerating Detection of Lung Pathologies with Explainable Ultrasound Image Analysis}, 
  author={Born, Jannis and Wiedemann, Nina and Cossio, Manuel and Buhre, Charlotte and Brändle, Gabriel and Leidermann, Konstantin and      Aujayeb, Avinash and Moor, Michael and Rieck, Bastian and Borgwardt, Karsten}, 
  volume={11}, ISSN={2076-3417}, 
  url={http://dx.doi.org/10.3390/app11020672}, 
  DOI={10.3390/app11020672}, 
  number={2}, 
  journal={Applied Sciences}, 
  publisher={MDPI AG}, 
  year={2021}, 
  month={Jan}, 
  pages={672}
}

@article {born2021l2,
  author = {Born, J and Wiedemann, N and Cossio, M and Buhre, C and Br{\"a}ndle, G and Leidermann, K and Aujayeb, A and Rieck, B and Borgwardt, K},
  title = {L2 Accelerating COVID-19 differential diagnosis with explainable ultrasound image analysis: an AI tool},
  volume = {76},
  number = {Suppl 1},
  pages = {A230--A231},
  year = {2021},
  doi = {10.1136/thorax-2020-BTSabstracts.404},
  publisher = {BMJ Publishing Group Ltd},
  issn = {0040-6376},
  URL = {https://thorax.bmj.com/content/76/Suppl_1/A230.2},
  eprint = {https://thorax.bmj.com/content/76/Suppl_1/A230.2.full.pdf},
  journal = {Thorax}
}
```
