# **Automatic Detection of COVID-19 from Ultrasound Data**
![Node.js CI](https://github.com/jannisborn/covid19_pocus_ultrasound/workflows/Node.js%20CI/badge.svg)
[![Build Status](https://github.com/jannisborn/covid19_ultrasound/actions/workflows/build.yml/badge.svg)](https://github.com/jannisborn/covid19_ultrasound/actions/workflows/build.yml)

## Summary

### News
This repo contains the code for the paper `Accelerating Detection of Lung Pathologies with Explainable Ultrasound Image Analysis` which is now [available](https://www.mdpi.com/2076-3417/11/2/672). Please [cite](#Citation) that one instead of our preprint.

### Dataset
Feel free to use (and cite) our dataset. We currently have >200 LUS videos labelled with a diagnostic outcome. Moreover, lung severity scores for 136 videos are made available in the [dataset_metadata.csv](./data/dataset_metadata.csv) under the column **"Lung Severity Score"** from [Gare et al., 2022](https://arxiv.org/abs/2201.07357). Further clinical information (symptoms, visible LUS patterns etc) are provided for some videos. For details see [data/README.md](data/README.md).

If you are looking for more data, please consider using the 40,000 [carefully simulated LUS images](https://gitlab.com/pulselab/covid19) from the paper by [Zhao et al. (2024, *Communications Medicine*)](https://www.nature.com/articles/s43856-024-00463-5) that were partially derived from the data in this repo. For details see [PULSE Lab Repository/README.md](PULSE%20Lab%20Repository/README.md).

**NOTE: Please make sure to create a meaningful train/test data split. Do not split the data on a frame-level, but on a video/patient-level. The task becomes trivial otherwise. See the instructions [here](pocovidnet/#cross-validation-splitting).**

Please note: The founders/authors of the repository take no responsibility or liability for the data contributed to this archive. The contributing sites have to ensure that the collection and use of the data fulfills all applicable legal and ethical requirements.


## Contribution
<p align="center">
	<img src="pocovidnet/plots/overview.png" alt="photo not available" width="100%" height="100%">
	<br>
   <em>Overview figure about current efforts. Public dataset consists of >200 LUS videos.</em>
</p>

### Motivation:
From the ML community, ultrasound has gained much less attention than CT and X-Ray in the context of COVID-19.
But many voices from the medical community have advocated for a more prominent role of ultrasound in the current pandemic.

### Summary
We developed methods for the automatic detection of **COVID-19** 
from **Lung Ultrasound** (LUS) recordings. Our results show that one can accurately distinguish LUS samples from COVID-19 patients from healthy controls and bacterial pneumonia. Our model is validated on an external dataset (ICLUS) where we achieve promising performance. The CAMs of the model were validated in a blinded study by US experts and found to highlight relevant pulmonary biomarkers.
Using model uncertainty techniques, we can further boost model performance and find samples which are likely to be incorrectly classified.
Our dataset complements the current data collection initiaves that only focus
on CT or X-Ray data. 

#### Evidence for ultrasound
Ultrasound is **non-invasive**, **cheap**, **portable** (bedside execution),
**repeatable** and **available in almost all medical facilities**. But even for
trained doctors detecting patterns of COVID-19 from ultrasound data is challenging and
time-consuming. Since their time is scarce, there is an urgent need to simplify,
fasten & automatize the detection of COVID-19.
   - [LUS is more sensitive than X-Ray in diagnosing COVID-19](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7390587/) 
   - [COVID-19 outbreak: less stethoscope, more ultrasound](https://www.thelancet.com/journals/lanres/article/PIIS2213-2600(20)30120-X/fulltext?fbclid=IwAR2kDbxpYTSjoj3Nl_B-nOhLZL66mQLUBVBCdzn6zEG5ObLKq9oXhPZDXHQ)
   - Ultrasound can evidence the same symptoms as CT: ([Point-by-point correspondance of CT
     and ultrasound findings through COVID-19 disease process](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7165267/)) 

#### Learn more about the project
- [**Read our manuscript**](https://www.mdpi.com/2076-3417/11/2/672)
- Read our [blogpost](https://towardsdatascience.com/ultrasound-for-covid-19-a-deep-learning-approach-f7906002892a)
  
## Installation 

### Ultrasound data
Find all details on the current state of the database in the [data](data)
folder.

### Deep learning model (`pocovidnet`)
Find all details on how to reproduce our experiments and train your models on
ultrasound data in the [pocovidnet](pocovidnet) folder.

### Web interface (`pocovidscreen`)
Find all details on how to get started in the [pocovidscreen](pocovidscreen)
folder.

## Contact 
- If you experience problems with the code, please open an
[issue](https://github.com/jannisborn/covid19_pocus_ultrasound/issues).
- If you have questions about the project, please reach out: `jannis.born@gmx.de`.

# Citation
An [abstract of our work was published](https://thorax.bmj.com/content/76/Suppl_1/A230.2) in *Thorax* as part of the BTS Winter Meeting 2021. 
The full paper is available via the COVID-19 special issue of [Applied Sciences](https://www.mdpi.com/2076-3417/11/2/672).
Please cite these in favor of our deprecated [POCOVID-Net preprint](https://arxiv.org/abs/2004.12084).

**Please use the following bibtex entry to cite this dataset:**
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
```

If you use the severity scores, please cite the [Gare et al., 2022](https://arxiv.org/abs/2201.07357) paper using the following bibtex entry:
```bib
@article{Gare2022WeaklyUltrasound,
    author = {Gare, Gautam Rajendrakumar and Tran, Hai V. and deBoisblanc, Bennett P and Rodriguez, Ricardo Luis and Galeotti, John Michael},
    title = {{Weakly Supervised Contrastive Learning for Better Severity Scoring of Lung Ultrasound}},
    year = {2022},
    month = {1},
    publisher = {arXiv},
    url = {https://arxiv.org/abs/2201.07357},
    doi = {10.48550/ARXIV.2201.07357},
    arxivId = {2201.07357}
}
```

If you use the 40,000 synthetic images from [Zhao et al., 2024](https://www.nature.com/articles/s43856-024-00463-5), please cite their paper with the following bibtex entry:
```bib
@article{zhao2024detection,
  title={Detection of COVID-19 features in lung ultrasound images using deep neural networks},
  author={Zhao, Lingyi and Fong, Tiffany Clair and Bell, Muyinatu A Lediju},
  journal={Communications Medicine},
  volume={4},
  number={1},
  pages={41},
  year={2024},
  publisher={Nature Publishing Group UK London}
}
```