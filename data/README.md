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
  
## Current dataset size (July 2020)
- Convex:
  - 109 videos (33x  COVID, 23x bacterial pneumonia, 50x healthy, 3x viral pneumonia)
  - 45 images (16x COVID, 7x bacterial pneumonia, 22x healthy)
  - 21 videos from the Butterfly dataset (19 COVID, 2 healthy, see below how to use the provided scripts to process the data)
- Linear: 
  - 20 videos (4x COVID, 2x bacterial pneumonia, 10x healthy, 4x viral pneumonia)
  - 5 images (3x COVID, 2x bacterial pneumonia)

- We are constantly updating the dataset with new data - any contributions are appreciated!

## Updates
- **11.7.2020**: Database update - We added an up to date csv file with all metadata, and new videos that were contributed from the Northumbria Specialist Emergency Care Hospital (17 images and 4 videos of healthy patients)
- **22.6.2020**: Database update - We added 46 new videos (18x COVID, 1x bacterial pneumonia, 27x healthy).
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

We are deeply thankful to the authors and contributors to our datset, in particular
* Dr Avinash Aujayeb (MBBS MRCP (Edin 2008) PgCert ClinEd FHEA), Pleural Medicine Lead and Consultant in Respiratory and Acute Medicine for the Trustee for Mesothelioma UK and Northumbria Specialist Emergency Care Hospital, who contributes regularly to our database with clinical data. We greatly appreciate their efforts for open-access data.
* The maintainers of https://thepocusatlas.com, https://radiopaedia.org/, https://grepmed.com and https://litfl.com/ultrasound-library/ (thanks for Dr. Rippey in particular who gave interesting advice)
* Charlotte Buhre for recording data herself just for our dataset.
* The contributers to [Stemlyn's blog](https://www.stemlynsblog.org/combatting-covid19-is-lung-ultrasound-an-option/).

Also, we obtained videos and images from publications on ultrasound, and we appreciate very much that we could include data from the following publications in our database:

* 3 COVID-19 images from [@inchingolo2020diagnosis] - [The Diagnosis of Pneumonia in a Pregnant Woman with COVID-19 Using Maternal Lung Ultrasound](https://www.ajog.org/action/showPdf?pii=S0002-9378%2820%2930468-3)
* 8 COVID-19 images from [@huang2020preliminary] - [A Preliminary Study on the Ultrasonic Manifestations of Peripulmonary Lesions of Non-Critical Novel Coronavirus Pneumonia (COVID-19)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3544750)
* 4 videos (healthy and pneumonia) from [@irwin2016advances] - [Advances in Point-of-Care Thoracic Ultrasound](https://www.sciencedirect.com/science/article/pii/S0733862715000772#appsec2)
* 2 videos (healthy and pneumonia) from [@bouhemad2007clinical] - [Clinical review: Bedside lung ultrasound in critical care practice](https://link.springer.com/article/10.1186/cc5668#Abs1)
* 3 COVID-19 images from [@lomoro2020covid] - [COVID-19 pneumonia manifestations at the admission on chest ultrasound, radiographs, and CT: single-center study and comprehensive radiologic literature review](https://www.sciencedirect.com/science/article/pii/S2352047720300204)
* 2 viral pneumonia videos (H1N1) from [@testa2012early] - [Early recognition of the 2009 pandemic influenza A (H1N1) pneumonia by chest ultrasound](https://link.springer.com/article/10.1186/cc11201)
* 1 healthy and 7 COVID-19 videos from [@yassa2020lung] - [Lung Ultrasound Can Influence the Clinical Treatment of Pregnant Women With COVID ‐19](https://onlinelibrary.wiley.com/doi/full/10.1002/jum.15367#jum15367-fig-0001)
* 2 healthy and 1 viral image from [@stadler2017lung] - [Lung ultrasound for the diagnosis of community-acquired pneumonia in children](https://link.springer.com/content/pdf/10.1007/s00247-017-3910-1.pdf)
* 1 healthy and 2 regular images from [@reissig2014lung] - [Lung Ultrasound in Community-Acquired Pneumonia and in Interstitial Lung Diseases](https://www.karger.com/Article/Pdf/357449)
* 4 pneumonia images from [@claes2017performance] - [Performance of chest ultrasound in pediatric pneumonia](https://www.sciencedirect.com/science/article/pii/S0720048X16304260?casa_token=W82e3087RfcAAAAA:plbCnRIJAeD9tj369F72kUDp0vChQMU9CwO0pBJvd6_RKsTSozgLFdPijaG4sFM7m5Auov988b4)
* 4 videos (viral and bacterial pneumonia) from [@tsung2012prospective] - [Prospective application of clinician-performed lung ultrasonography during the 2009 H1N1 influenza A pandemic: distinguishing viral from bacterial pneumonia](https://theultrasoundjournal.springeropen.com/articles/10.1186/2036-7902-4-16)
* 6 videos (COVID-19, healthy, bacterial pneumonia) from [@vieira2020role] - [Role of point-of-care ultrasound during the COVID-19 pandemic: our recommendations in the management of dialytic patients](https://theultrasoundjournal.springeropen.com/articles/10.1186/s13089-020-00177-4)
* 9 COVID-19 images from [@sofia2020thoracic] - [Thoracic ultrasound and SARS-COVID-19: a pictorial essay](https://link.springer.com/content/pdf/10.1007/s40477-020-00458-7.pdf)

```bib
@article{inchingolo2020diagnosis,
  title={The Diagnosis of Pneumonia in a Pregnant Woman with COVID-19 Using Maternal Lung Ultrasound},
  author={Inchingolo, Riccardo and Smargiassi, Andrea and Moro, Francesca and Buonsenso, Danilo and Salvi, Silvia and Del Giacomo, Paola and Scoppettuolo, Giancarlo and Demi, Libertario and Soldati, Gino and Testa, Antonia Carla},
  journal={American Journal of Obstetrics and Gynecology},
  year={2020},
  publisher={Elsevier}
}
@article{huang2020preliminary,
  title={A preliminary study on the ultrasonic manifestations of peripulmonary lesions of non-critical novel coronavirus pneumonia (COVID-19)},
  author={Huang, Yi and Wang, Sihan and Liu, Yue and Zhang, Yaohui and Zheng, Chuyun and Zheng, Yu and Zhang, Chaoyang and Min, Weili and Zhou, Huihui and Yu, Ming and others},
  journal={Available at SSRN 3544750},
  year={2020}
}
@article{irwin2016advances,
  title={Advances in point-of-care thoracic ultrasound},
  author={Irwin, Zareth and Cook, Justin O},
  journal={Emerg Med Clin North Am},
  volume={34},
  number={1},
  pages={151--7},
  year={2016}
}
@article{bouhemad2007clinical,
  title={Clinical review: bedside lung ultrasound in critical care practice},
  author={Bouhemad, B{\'e}la{\"\i}d and Zhang, Mao and Lu, Qin and Rouby, Jean-Jacques},
  journal={Critical care},
  volume={11},
  number={1},
  pages={205},
  year={2007},
  publisher={Springer}
}
@article{lomoro2020covid,
  title={COVID-19 pneumonia manifestations at the admission on chest ultrasound, radiographs, and CT: single-center study and comprehensive radiologic literature review},
  author={Lomoro, Pascal and Verde, Francesco and Zerboni, Filippo and Simonetti, Igino and Borghi, Claudia and Fachinetti, Camilla and Natalizi, Anna and Martegani, Alberto},
  journal={European journal of radiology open},
  pages={100231},
  year={2020},
  publisher={Elsevier}
}
@article{testa2012early,
  title={Early recognition of the 2009 pandemic influenza A (H1N1) pneumonia by chest ultrasound},
  author={Testa, Americo and Soldati, Gino and Copetti, Roberto and Giannuzzi, Rosangela and Portale, Grazia and Gentiloni-Silveri, Nicol{\`o}},
  journal={Critical Care},
  volume={16},
  number={1},
  pages={R30},
  year={2012},
  publisher={Springer}
}
@article{yassa2020lung,
  title={Lung Ultrasound Can Influence the Clinical Treatment of Pregnant Women With COVID-19},
  author={Yassa, Murat and Birol, Pinar and Mutlu, Ali Memis and Tekin, Arzu Bilge and Sandal, Kemal and Tug, Niyazi},
  journal={Journal of Ultrasound in Medicine},
  year={2020},
  publisher={Wiley Online Library}
}
@article{stadler2017lung,
  title={Lung ultrasound for the diagnosis of community-acquired pneumonia in children},
  author={Stadler, Jacob AM and Andronikou, Savvas and Zar, Heather J},
  journal={Pediatric radiology},
  volume={47},
  number={11},
  pages={1412--1419},
  year={2017},
  publisher={Springer}
}
@article{reissig2014lung,
  title={Lung ultrasound in community-acquired pneumonia and in interstitial lung diseases},
  author={Reissig, Angelika and Copetti, Roberto},
  journal={Respiration},
  volume={87},
  number={3},
  pages={179--189},
  year={2014},
  publisher={Karger Publishers}
}
@article{claes2017performance,
  title={Performance of chest ultrasound in pediatric pneumonia},
  author={Claes, Anne-Sophie and Clapuyt, Philippe and Menten, Renaud and Michoux, Nicolas and Dumitriu, Dana},
  journal={European journal of radiology},
  volume={88},
  pages={82--87},
  year={2017},
  publisher={Elsevier}
}
@article{tsung2012prospective,
  title={Prospective application of clinician-performed lung ultrasonography during the 2009 H1N1 influenza A pandemic: distinguishing viral from bacterial pneumonia},
  author={Tsung, James W and Kessler, David O and Shah, Vaishali P},
  journal={Critical ultrasound journal},
  volume={4},
  number={1},
  pages={1--10},
  year={2012},
  publisher={SpringerOpen}
}
@article{vieira2020role,
  title={Role of point-of-care ultrasound during the COVID-19 pandemic: our recommendations in the management of dialytic patients},
  author={Vieira, Ana Luisa Silveira and J{\'u}nior, Jos{\'e} Muniz Pazeli and Bastos, Marcus Gomes},
  journal={The Ultrasound Journal},
  volume={12},
  number={1},
  pages={1--9},
  year={2020},
  publisher={SpringerOpen}
}
@article{sofia2020thoracic,
  title={Thoracic ultrasound and SARS-COVID-19: a pictorial essay},
  author={Sofia, Soccorsa and Boccatonda, Andrea and Montanari, Marco and Spampinato, Michele and D’ardes, Damiano and Cocco, Giulio and Accogli, Esterita and Cipollone, Francesco and Schiavone, Cosima},
  journal={Journal of ultrasound},
  pages={1--5},
  year={2020},
  publisher={Springer}
}
```

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
