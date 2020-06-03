# COVID-19 Ultrasound data

We build a dataset of lung ultrasound images and videos. The dataset is
assembled from publicly available resources in the web as well as from publications.


## Contribute!
- You can donate your lung ultrasound recordings directly on our website: [](https://pocovidscreen.org)
- Please help us to find more data! Open an
  [issue](https://github.com/jannisborn/covid19_pocus_ultrasound/issues) if you
  identified a promising data source. Please check [here](https://docs.google.com/spreadsheets/d/1t-tLMjMod6W-nAjkuxmO0CLsiyalFIOp92k_XD_yeo8/edit#gid=1181682638) in our Google sheet whether the data is already included. Useful contributions are:
   - Publications with ultrasound images/videos
      - check sheet *image_data_publications* in the goole sheet linked above to see whether a publication was already added
   - Images/Videos that are available via Creative Commens license (e.g. CC
     BY-NC-SA) in the web or on YouTube.
   - Possible sources are:
      - https://thepocusatlas.com
      - https://radiopaedia.org/
      - https://grepmed.com
      - https://litfl.com/ultrasound-library/
  
## Current dataset size (May 2020)
- Convex:
  - 86 videos (40x COVID, 23x bacterial pneumonia, 20x healthy, 3x viral pneumonia)
  - 28 images (16x COVID, 7x bacterial pneumonia, 5x healthy)
- Linear: 
  - 20 videos (4x COVID, 2x bacterial pneumonia, 10x healthy, 4x viral pneumonia)
  - 5 images (3x COVID, 2x bacterial pneumonia)

- Soon more will be added!

## Updates
- **16.5.2020**: The [ICLUS
  project](https://www.disi.unitn.it/iclus) released ~60 videos
  from COVID-patients (register [here](https://covid19.disi.unitn.it/iclusdb/login)). 
  

## Collect Data from sources without CC license (Butterfly & ICLUS)

Unfortunately, not all data used to train/evaluate the model is in this repo
as we do not have the right to host/distribute the data from
[Butterfly](https://butterflynetwork.com) and [ICLUS](https://iclus-web.bluetensor.ai/login/?next=/).

However, we **provide a script that automatically processes the data from Butterfly**. To reproduce
the experiments from the paper, please first complete the following steps:

1. Visit the [COVID-19 ultrasound_gallery](https://butterflynetwork.com/covid19/covid-19-ultrasound-gallery)
   of Butterfly, scroll to the bottom and download the videos (we accessed this
   source on 17.04.2020 for training our models. Please note that it is not
   under control whether Butterfly will keep this data online. Feel free to
   notify us if you observe any changes).
2. Place the `.zip` folder into the this folder (`data`)
3. `cd` into the `data` folder.
3. Run:
    ```sh
    sh parse_butterfly.sh
    ```
    *NOTE*: This step requires that you installed the `pocovidnet` package
    before (see the [pocovidnet](../pocovidnet/) README how to do that).
    
All current images should now be in `data/image_dataset`.


## Add class "uninformative"
In the current state, a user could input any image, e.g. of a house, and still receive a classification result as covid / pneumonia / healthy.
In order to prevent this, we decided to include a fourth class called "uninformative", where we add Imagenet images and neck-ultrasound data from the Kaggle Nerve Segmentation Challenge.

Download the data [here](https://drive.google.com/open?id=1bAbCJCq-U5vIxbG0ySUKanAW_pW_z2O4) from google drive. It contains a folder *uniform_class_nerves* and one *uniform_class_imagenet*.

The data can be immediately used for training, simply combine it in a folder *uninformative* next to the *covid*, *pneumonia* and *regular* folders.

If you want to add them to an existing cross validation split (e.g after executing [cross_val_splitter](../pocovidnet/scripts/cross_val_splitter.py)), we also provide a script:

Run:
```
cd ..
python ../pocovidnet/scripts/add_uninformative_class.py -i uniform_class_imagenet -u uniform_class_nerves -o cross_validation -s 5
```

This script will split the data in the *uniform_class_nerves* and *uniform_class_imagenet* folders and add them in a folder *uninformative* to each fold.

## License Note:
Most data here is available under [Creative Commons
License](https://creativecommons.org/licenses/by-nc/4.0/).
The following modifcations to videos/images were done:
- Cropped to the center to remove measuring bars, text etc.
- Removal of artifcats on the sample (few cases only)


We are deeply thankful to the authors and contributors to our datset, in particular to the maintainers of https://thepocusatlas.com, https://radiopaedia.org/, https://grepmed.com and https://litfl.com/ultrasound-library/ (thanks for Dr. Rippey who helped us personally), and to Charlotte Buhre for recording data herself just for our dataset.

## Citation
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
