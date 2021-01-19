# **Automatic Detection of COVID-19 from Ultrasound Data**
![Node.js CI](https://github.com/jannisborn/covid19_pocus_ultrasound/workflows/Node.js%20CI/badge.svg)
[![Build Status](https://travis-ci.com/BorgwardtLab/covid19_ultrasound.svg?branch=master)](https://travis-ci.com/BorgwardtLab/covid19_ultrasound)

## Summary

### News
This repo contains the code for the paper `Accelerating Detection of Lung Pathologies with Explainable Ultrasound Image Analysis` which is now [available](https://www.mdpi.com/2076-3417/11/2/672). Please [cite](#Citation) that one instead of our preprint.

### Goal
This is an ongoing ultrasound data collection initiative for COVID-19. Please help growing the [database](data/README.md).

### Dataset
Feel free to use (and cite) our dataset. We currently have >200 LUS videos. For details see [data/README.md](data/README.md).


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
- If you have questions about the project, please reach out: `jborn@ethz.ch`.

# Citation
The paper is available in [Applied Sciences](https://www.mdpi.com/2076-3417/11/2/672).
Please cite this one in favor of our deprecated [POCOVID-Net preprint](https://arxiv.org/abs/2004.12084).

Please use the following bibtex entry:
```bib
@article{born2021accelerating,
   title={Accelerating Detection of Lung Pathologies with Explainable Ultrasound Image Analysis},
   author={Born, Jannis and Wiedemann, Nina and Cossio, Manuel and Buhre, Charlotte and Brändle, Gabriel and Leidermann, Konstantin and Aujayeb, Avinash and Moor, Michael and Rieck, Bastian and Borgwardt, Karsten},  
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
