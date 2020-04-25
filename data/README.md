# COVID-19 Ultrasound data

We build a dataset of lung ultrasound images and videos. The dataset is
assembled from publicly available resources in the web as well as from publications.


## Contribute!
- Donate your lung ultrasound recordings directly on our website:
  [https://pocovidscreen.org](https://pocovidscreen.org)
    - *Note:* We will manually process the data (crop it, remove artifacts etc.)
      and get it approved from medical doctors before it will be added to the
      dataset.

- Please help us to find more data! Open an
  [issue](https://github.com/jannisborn/covid19_pocus_ultrasound/issues) if you
  identified a promising data source. Please check before [here](https://docs.google.com/spreadsheets/d/1t-tLMjMod6W-nAjkuxmO0CLsiyalFIOp92k_XD_yeo8/edit#gid=1181682638) whether the
  data is already included. Useful contributions could include:
   - Publications with ultrasound images/videos
   - Images/Videos that are available via Creative Commens license (e.g. CC
     BY-NC-SA) in the web or on YouTube.
   - Possible sources are:
      - https://thepocusatlas.com
      - https://radiopaedia.org/
      - https://grepmed.com 

   
- *Note*: We are mostly looking for *healthy* lung recordings (at the moment we have *more* data for COVID than for healthy
  lungs)
- Open issues in this repository and paste links to publications (please
     check [here TODO]() before whether the data is already in the dataset)



## Collect Data from Butterfly
Unfortunately, not all data used to train/evaluate the model is in this repo
as we do not have the right to host/distribute the data from
[Butterfly](https://butterflynetwork.com).

However, we provide a script that automatically processes the data. To reproduce
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
    
All current images should now be in `data/pocus_images`.
