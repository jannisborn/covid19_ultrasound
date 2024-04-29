# PULSE Lab Repository Containing Simulated and Labeled In Vivo COVID-19 Dataset

Repository link: https://gitlab.com/pulselab/covid19

This external repository link provides public access to the datasets and code described in the paper “Detection of COVID-19 features in lung ultrasound images using deep neural networks.” Communications Medicine, 2024. https://www.nature.com/articles/s43856-024-00463-5.

Access includes 40,000 carefully simulated lung ultrasound B-mode images containing A-line, B-line, and consolidation features with paired ground truth segmentations. The simulation code can be accessed via the repository. 

Access also includes segmentation annotations of the following publicly available POCUS datasets (available in https://github.com/jannisborn/covid19_ultrasound):

| File name                              | Source link                                                                                          | Feature       | File name prefix in the data folder |
|----------------------------------------|------------------------------------------------------------------------------------------------------|---------------|-------------------------------------|
| Reg-Atlas-alines                       | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_034                             |
| Reg_Avi_normal-A-lines-pleural-line    | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_133                             |
| Reg_Avi_lung-sliding                   | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_134                             |
| Reg_Avi_lung-sliding-3                 | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_135                             |
| Reg_Avi_lung-sliding-2                 | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_137                             |
| Reg_Avi_normal-A-lines                 | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_139                             |
| Reg_Avi_pleural-line-normal            | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_151                             |
| Reg_Avi_Image002                       | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_157                             |
| Reg_Avi_Image003                       | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_159                             |
| Reg_northumbria_0409_set3_vid1         | Data contributed by Northumbria Specialist Emergency Care Hospital                                   | Aline         | Reg_200                             |
| Cov-Atlas-Day+2                        | http://www.thepocusatlas.com/covid19 (Day2)                                                          | Bline         | Cov_025                             |
| Cov-Atlas-+(43)                        | http://www.thepocusatlas.com/covid19-1/ru6w5sgjyu1zn21jraypm2pfm0h6uf                                | Bline         | Cov_030                             |
| Cov-Atlas-suspectedCovid               | http://www.thepocusatlas.com/covid19-1/lung-us-findings-in-hypoxic-patient-with-suspected-covid19    | Bline         | Cov_036                             |
| Cov_denault_proposedUS_vid1            | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7241588/                                                | Bline         | Cov_293                             |
| Cov_denault_proposedUS_vid2            | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7241588/                                                | Bline         | Cov_294                             |
| Cov_denault_proposedUS_vid13           | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7241588/                                                | Bline         | Cov_299                             |
| Cov_denault_proposedUS_vid14           | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7241588/                                                | Bline         | Cov_300                             |
| Cov_combatting_Image1                  | https://www.stemlynsblog.org/combatting-covid19-is-lung-ultrasound-an-option/ - third video          | Bline         | Cov_126                             |
| Cov_combatting_Image2                  | https://www.stemlynsblog.org/combatting-covid19-is-lung-ultrasound-an-option/ - fourth video         | Bline         | Cov_127                             |
| Cov_combatting_Image3                  | https://www.stemlynsblog.org/combatting-covid19-is-lung-ultrasound-an-option/ - fifth video          | Bline         | Cov_129                             |
| Cov_combatting_image4                  | https://www.stemlynsblog.org/combatting-covid19-is-lung-ultrasound-an-option/ - sixth video          | Bline         | Cov_130                             |
| Cov_combatting_Image5                  | https://www.stemlynsblog.org/combatting-covid19-is-lung-ultrasound-an-option/ - seventh video        | Consolidation | Cov_131                             |
| Reg_recommendations_alines_mov1        | https://theultrasoundjournal.springeropen.com/articles/10.1186/s13089-020-00177-4#author-information | Aline         | Reg_255                             |
| Cov_recommendations_likebutterfly_mov5 | https://theultrasoundjournal.springeropen.com/articles/10.1186/s13089-020-00177-4#author-information | Consolidation | Cov_259                             |
| Cov_recommendations_lightbeam_mov6     | https://theultrasoundjournal.springeropen.com/articles/10.1186/s13089-020-00177-4#author-information | Bline         | Cov_260                             |
| Cov_convex_volpecelli_sonographic_v1   | https://theultrasoundjournal.springeropen.com/articles/10.1186/s13089-020-00171-w                    | Bline         | Cov_288                             |
| Cov_convex_volpecelli_sonographic_v2   | https://theultrasoundjournal.springeropen.com/articles/10.1186/s13089-020-00171-w                    | Bline         | Cov_289                             |
| Cov_convex_volpecelli_sonographic_v3   | https://theultrasoundjournal.springeropen.com/articles/10.1186/s13089-020-00171-w                    | Bline         | Cov_290                             |
| Cov_convex_volpecelli_sonographic_v4   | https://theultrasoundjournal.springeropen.com/articles/10.1186/s13089-020-00171-w                    | Bline         | Cov_291                             |
| Cov_convex_volpecelli_sonographic_v5   | https://theultrasoundjournal.springeropen.com/articles/10.1186/s13089-020-00171-w                    | Bline         | Cov_292                             |
| Cov_Oliviera_2020_Fig5A                | https://www.scielo.br/img/revistas/rb/v53n4//0100-3984-rb-20200051-gf05.jpg                          | Bline         | Cov_364                             |
| Cov_Oliviera_2020_Fig15A               | https://www.scielo.br/img/revistas/rb/v53n4//0100-3984-rb-20200051-gf15.jpg                          | Bline         | Cov_366                             |
| Cov_emdocs_vid1                        | http://www.emdocs.net/wp-content/uploads/2020/04/R-apex-1.gif                                        | Bline         | Cov_373                             |
| Cov_emdocs_vid3                        | http://www.emdocs.net/wp-content/uploads/2020/04/unnamed.gif                                         | Bline         | Cov_375                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_003                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Aline         | Reg_004                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_006                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_007                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_008                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Consolidation | Cov_009                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Consolidation | Cov_010                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Consolidation | Cov_011                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Consolidation | Cov_013                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_014                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_015                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_016                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_018                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_019                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_020                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_021                             |
| Butterfly                              | https://www.butterflynetwork.com/covid19/covid-19-ultrasound-gallery                                 | Bline         | Cov_022                             |

If you use the simulated datasets, labels, and/or code in this external repository, cite the following references:

1. L. Zhao, T.C. Fong, M.A.L. Bell, “Detection of COVID-19 features in lung ultrasound images using deep neural networks”, Communications Medicine, 2024. https://www.nature.com/articles/s43856-024-00463-5

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

2. L. Zhao, M.A.L. Bell (2023). Code for the paper “Detection of COVID-19 features in lung ultrasound images using deep neural networks”. Zenodo. https://doi.org/10.5281/zenodo.10324042

```bib
@misc{zenodo,
  title={Code for the paper “Detection of COVID-19 features in lung ultrasound images using deep neural networks"},
  author={Zhao, Lingyi and Bell, Muyinatu A Lediju},
  year={2024},  
  publisher={Zenodo}
  url={https://doi.org/10.5281/zenodo.10324042}
}
```