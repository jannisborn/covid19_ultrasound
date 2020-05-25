# pocovidnet

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

### Train the model

Afterwards you can train the model by:
```sh
python3 scripts/train_covid19.py --data_dir ../data/cross_validation/ --fold 0 --epochs 2
```
*NOTE*: `train_covid19.py` will automatically utilize the data from all other
folds for training.

## Our results (`POCOVID-Net`)

Current results (5-fold CV) are an accuracy of 0.89 (balanced accuracy 0.82) across all 3
classes. For COVID-19, we achieve a sensitivity of 96%.

![alt text](https://github.com/jannisborn/covid19_pocus_ultrasound/blob/master/pocovidnet/plots/confusion_matrix.png "Confusion matrix")

Detailed performances:
![alt text](https://github.com/jannisborn/covid19_pocus_ultrasound/blob/master/pocovidnet/plots/result_table.png "Result table")

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