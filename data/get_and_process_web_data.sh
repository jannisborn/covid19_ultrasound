# Install youtube downloader if applicable
if ! command -v youtube-dl &> /dev/null
then
    echo "youtube-dl could not be found, installing now.."
    sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl
    sudo chmod a+rx /usr/local/bin/youtube-dl
else
    echo "Found existing youtube-dl version."
fi

echo "Grabbing data now.."

mkdir tmp 
mkdir tmp/pocus_videos tmp/pocus_videos/convex tmp/pocus_videos/linear
mkdir tmp/pocus_images tmp/pocus_images/convex tmp/pocus_images/linear

wget -O tmp/pocus_videos/convex/Cov-clarius.gif https://clarius.com/wp-content/uploads/2020/03/1-blines.gif
wget -O tmp/pocus_videos/convex/Cov-clarius3.gif https://clarius.com/wp-content/uploads/2020/03/3-large-consolidation.gif # Former file type is mp4
wget -O tmp/pocus_images/convex/Pneu_clarius.jpg https://cloud.clarius.com/cases/img/85166/
wget -O tmp/pocus_images/convex/Pneu_clarius2.png https://cloud.clarius.com/cases/img/85168/
wget -O tmp/pocus_videos/convex/pneu-everyday.gif https://bit.ly/39wgXfk
wget -O tmp/pocus_videos/convex/Reg-nephropocus.gif https://nephropocushome.files.wordpress.com/2019/07/a-lines-titled.gif # Former file type is mp4
wget -O tmp/pocus_videos/convex/Reg-bcpocus.gif https://www.bcpocus.ca/wp-content/uploads/2018/07/A-lines.gif
youtube-dl -f 134 -o "tmp/pocus_videos/convex/Reg-Youtube.mp4" https://www.youtube.com/watch\?v\=VzgX9ihnmec\&ab_channel\=EM:RAPProductions
youtube-dl -f 136 -o "tmp/pocus_videos/linear/Reg-Youtube-start20sec.mp4" https://www.youtube.com/watch?v=Qd-26HdJP6I&ab
youtube-dl -f 136 -o "tmp/pocus_videos/linear/Pneu-Youtube-start20sec.mp4" https://www.youtube.com/watch?v=Qd-26HdJP6I&ab
youtube-dl -f 18 -o "tmp/pocus_videos/linear/Reg-Youtube-Video_902_Lung_POCUS-left.mp4" https://www.youtube.com/watch?v=HqPXJ0A0HCU&ab
wget -O "tmp/pocus_videos/linear/Reg-nephropocus.gif" https://images.squarespace-cdn.com/content/v1/5c69e7d7b91449698da66e65/1590627160853-3ULNVXBBJD5LVR930CU1/ke17ZwdGBToddI8pDm48kI8YiP-OhoX1jaED3zwYDitZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpw0zQBx-_xluAT7IF9HiONY7KDc7zDddqX0ywCRyjQsO3pixv1ek7N_oX80uiIUqvU/LungPoint.ezgif.gif?format=750w # Formerly MP4
wget -O "tmp/pocus_videos/linear/Reg-NormalLung.gif" https://i0.wp.com/criticalcarenorthampton.com/wp-content/uploads/2016/11/normal-lung.gif?resize=480,360&ssl=1 # Formerly mp4
wget -O "tmp/pocus_videos/linear/Reg-minimalmovement.gif" https://i0.wp.com/criticalcarenorthampton.com/wp-content/uploads/2016/11/pneumothorax-case-3-litfl-ultrasound-clinical-cases.gif?resize=480,360&ssl=1
wget -O "tmp/pocus_videos/convex/Reg_Alines-1-90.mov" https://hls.cf.brightcove.com/1611106596001/4304256093001/1611106596001_4304256093001_s-1.ts\?pubId\=1611106596001\&videoId\=4304084884001
wget -O "tmp/pocus_videos/convex/Pneu_AIR BRONC2.mov" https://f1.media.brightcove.com/3/1611106596001/4304256034001/1611106596001_4304256034001_s-1.ts\?pubId\=1611106596001\&videoId\=4304052567001
wget -O "tmp/pocus_videos/convex/Cov-grepmed-blines-pocus-.mp4" https://img.grepmed.com/uploads/7415/blines-pocus-pulmonary-lung-covid19-original.mp4
wget -O "tmp/pocus_videos/convex/Cov-grepmed2.mp4" https://img.grepmed.com/uploads/7410/sparing-lung-ultrasound-subpleural-blines-original.mp4
wget -O "tmp/pocus_videos/convex/pneu-gred-6.gif" https://img.grepmed.com/uploads/5721/airbronchogram-pulmonary-pocus-pneumonia-lung-original.gif
wget -O "tmp/pocus_videos/convex/Pneu-grep-pneumonia1.mp4" https://img.grepmed.com/uploads/6903/ultrasound-pocus-bronchograms-lung-pulmonary-original.mp4
wget -O "tmp/pocus_videos/convex/Pneu-grep-pneumonia2_1.mp4" https://img.grepmed.com/uploads/6876/bronchograms-air-pulmonary-pocus-ultrasound-original.mp4
wget -O tmp/pocus_videos/convex/Pneu-grep-pneumonia4.mp4 https://img.grepmed.com/uploads/6431/ultrasound-lung-pneumonia-shredsign-clinical-original.mp4
wget -O tmp/pocus_videos/convex/pneu-gred-7.gif https://img.grepmed.com/uploads/1304/airbronchograms-pneumonia-sonostuff-effusion-clinical-original.gif
wget -O tmp/pocus_videos/convex/Pneu-grep-pneumonia3.mp4 https://img.grepmed.com/uploads/6439/pulmonary-ultrasound-pocus-clinical-lung-original.mp4
wget -O tmp/pocus_videos/convex/Reg-Grep-Alines.mp4 https://img.grepmed.com/uploads/7408/pocus-alines-lung-normal-ultrasound-original.mp4
wget -O tmp/pocus_videos/convex/Reg-Grep-Normal.gif https://img.grepmed.com/uploads/5325/clinical-pulmonary-lung-normal-artifact-original.gif
wget -O tmp/pocus_videos/convex/Pneu-grep-shredsign-consolidation.mp4 https://img.grepmed.com/uploads/7583/lung-pocus-ultrasound-shredsign-consolidation-original.mp4
wget -O tmp/pocus_videos/convex/Pneu-grep-bacterial-hepatization-clinical.mp4 https://img.grepmed.com/uploads/7582/pocus-pneumonia-bacterial-hepatization-clinical-original.mp4
wget -O tmp/pocus_videos/convex/Pneu-grep-pulmonary-pneumonia.mp4 https://img.grepmed.com/uploads/6952/pocus-clinical-lung-pulmonary-pneumonia-original.mp4
wget -O tmp/pocus_videos/convex/Cov-grep-7543.mp4 https://img.grepmed.com/uploads/7543/clinical-covid19-pocus-sarscov2-lung-original.mp4
wget -O tmp/pocus_videos/convex/Cov-grep-7525.mp4 https://img.grepmed.com/uploads/7525/lung-ultrasound-pocus-coronavirus-covid19-original.mp4
wget -O tmp/pocus_videos/convex/Cov-grep-7511.mp4 https://img.grepmed.com/uploads/7511/ultrasound-covid19-pocus-sarscov2-coronavirus-original.mp4
wget -O tmp/pocus_videos/convex/Cov-grep-7510.mp4 https://img.grepmed.com/uploads/7510/clinical-blines-covid19-pocus-lung-original.mp4
wget -O tmp/pocus_videos/convex/Cov-grep-7507.mp4 https://img.grepmed.com/uploads/7507/ultrasound-sarscov2-pocus-clinical-lung-original.mp4
wget -O tmp/pocus_videos/convex/Cov-grep-7505.mp4 https://img.grepmed.com/uploads/7505/covid19-pocus-ultrasound-sarscov2-clinical-original.mp4
wget -O tmp/pocus_videos/convex/Cov-grep-7453.mp4 https://img.grepmed.com/uploads/7453/covid19-lung-sarscov2-coronavirus-skiplesions-original.mp4
wget -O tmp/pocus_videos/linear/Reg-grep-normal-alines-original.mp4 https://img.grepmed.com/uploads/7578/ultrasound-sliding-pulmonary-normal-alines-original.mp4
wget -O tmp/pocus_videos/linear/Cov-grep-7500.mp4 https://img.grepmed.com/uploads/7500/clinical-subpleural-coronavirus-covid19-pocus-original.mp4
wget -O tmp/pocus_videos/linear/Cov-grep-7432.mp4 https://img.grepmed.com/uploads/7432/ultrasound-sarscov2-lung-covid19-pocus-original.mp4
wget -O tmp/pocus_videos/linear/Cov-grep-7431.mp4 https://img.grepmed.com/uploads/7431/lung-pocus-coronavirus-ultrasound-clinical-original.mp4
wget -O tmp/pocus_videos/convex/Reg_alines_advancesVid4.mp4 https://ars.els-cdn.com/content/image/1-s2.0-S0733862715000772-mmc4.mp4
wget -O tmp/pocus_videos/convex/Vir_blines_advancesVid9.mp4 https://ars.els-cdn.com/content/image/1-s2.0-S0733862715000772-mmc9.mp4
wget -O tmp/pocus_videos/convex/Pneu_consol_advancesVid10.mp4 https://ars.els-cdn.com/content/image/1-s2.0-S0733862715000772-mmc10.mp4
wget -O tmp/pocus_videos/convex/Reg_clinicalreview_mov1.mp4 https://static-content.springer.com/esm/art%3A10.1186%2Fcc5668/MediaObjects/13054_2007_5188_MOESM1_ESM.avi
wget -O tmp/pocus_videos/convex/Pneu_clinicalreview_MOV4.mp4 https://static-content.springer.com/esm/art%3A10.1186%2Fcc5668/MediaObjects/13054_2007_5188_MOESM4_ESM.avi
wget -O tmp/pocus_images/convex/Cov_ablines_covidmanifestations_paper1.png https://ars.els-cdn.com/content/image/1-s2.0-S2352047720300204-gr1_lrg.jpg
wget -O tmp/pocus_images/convex/Cov_blines_covidmanifestation_paper2.png https://ars.els-cdn.com/content/image/1-s2.0-S2352047720300204-gr2_lrg.jpg
wget -O tmp/pocus_images/linear/Cov_irregularpleural_covidmanifestations_paper3.png https://ars.els-cdn.com/content/image/1-s2.0-S2352047720300204-gr3_lrg.jpg
wget -O tmp/pocus_videos/convex/Cov_new_pregnant_vid1.avi "https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjum.15367&file=jum15367-sup-0001-VideoS1.avi"
wget -O tmp/pocus_videos/convex/Cov_new_pregnant_vid2.avi "https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjum.15367&file=jum15367-sup-0002-VideoS2.avi"
wget -O tmp/pocus_videos/convex/Cov_new_pregnant_vid3.avi "https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjum.15367&file=jum15367-sup-0003-VideoS3.avi"
wget -O tmp/pocus_videos/convex/Cov_new_pregnant_vid4.avi "https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjum.15367&file=jum15367-sup-0004-VideoS4.avi"
wget -O tmp/pocus_videos/convex/Cov_new_pregnant_vid5.avi "https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjum.15367&file=jum15367-sup-0005-VideoS5.avi"
wget -O tmp/pocus_videos/convex/Cov_new_pregnant_vid6.avi "https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjum.15367&file=jum15367-sup-0006-VideoS6.avi"
wget -O tmp/pocus_videos/convex/Cov_new_pregnant_vid7.avi "https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjum.15367&file=jum15367-sup-0007-VideoS7.avi"
wget -O tmp/pocus_videos/convex/Cov_new_pregnant_vid8.avi "https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fjum.15367&file=jum15367-sup-0008-VideoS8.avi"
wget -O tmp/pocus_images/convex/Reg_com_acquired_paper.png https://www.karger.com/WebMaterial/ShowPic/150968
wget -O tmp/pocus_images/convex/Pneu_air_bronchogram_com_acquired_paper.png https://www.karger.com/WebMaterial/ShowPic/150968
wget -O tmp/pocus_images/linear/Pneu_leftbasal_pedriatic_pneumonia.png https://ars.els-cdn.com/content/image/1-s2.0-S0720048X16304260-gr5.jpg 
wget -O tmp/pocus_images/linear/Pneu_consol_pedriatic_pneumonia.png https://ars.els-cdn.com/content/image/1-s2.0-S0720048X16304260-gr6.jpg
wget -O tmp/pocus_images/convex/Cov_pregnantPublication1.png https://ars.els-cdn.com/content/image/1-s2.0-S0002937820304683-gr1.jpg
wget -O tmp/pocus_images/convex/Cov_pregnantPublication2.png https://ars.els-cdn.com/content/image/1-s2.0-S0002937820304683-gr1.jpg
wget -O tmp/pocus_images/convex/Cov_blines_thoraric_paperfig1.png https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs40477-020-00458-7/MediaObjects/40477_2020_458_Fig1_HTML.jpg
wget -O tmp/pocus_images/convex/Cov_blines_thoraric_paperfig2.png https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs40477-020-00458-7/MediaObjects/40477_2020_458_Fig2_HTML.jpg
wget -O tmp/pocus_images/convex/Cov_blines_thoraric_paperfig3.png https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs40477-020-00458-7/MediaObjects/40477_2020_458_Fig3_HTML.jpg
wget -O tmp/pocus_images/convex/Cov_pleuralthickening_thoraric_paperfig8.png https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs40477-020-00458-7/MediaObjects/40477_2020_458_Fig7_HTML.jpg
wget -O tmp/pocus_images/convex/Cov_whitelungs_thoraric_paperfig5.png https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs40477-020-00458-7/MediaObjects/40477_2020_458_Fig4_HTML.jpg
wget -O tmp/pocus_images/convex/Cov_pleuraleffusion_thoraric_paperfig9.png https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs40477-020-00458-7/MediaObjects/40477_2020_458_Fig8_HTML.jpg
wget -O tmp/pocus_images/convex/Cov_subpleuralthickening_thoraric_paperfig6.png https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs40477-020-00458-7/MediaObjects/40477_2020_458_Fig5_HTML.jpg
wget -O tmp/pocus_images/convex/Reg_publication1.png https://journals.viamedica.pl/advances_in_respiratory_medicine/article/viewFile/41845/36561/110994
wget -O tmp/pocus_images/convex/Cov_efsumb1.png https://wfumb.info/wp-content/uploads/2020/04/wfumb_april_fig03.png 
wget -O tmp/pocus_images/convex/Cov_efsumb1_2.png https://wfumb.info/wp-content/uploads/2020/04/wfumb_april_fig03.png
wget -O tmp/pocus_images/convex/Cov_efsumb3.png https://wfumb.info/wp-content/uploads/2020/04/wfumb_april_fig06-1-1024x682.png 
wget -O tmp/pocus_images/convex/Reg_efsumb2.png https://wfumb.info/wp-content/uploads/2020/04/wfumb_april_fig01.png
wget -O tmp/pocus_images/convex/Pneu_sonographiebilder1.jpg https://sonographiebilder.de/fileadmin/_processed_/c/b/csm_Pneumonie_li_canifizierend_24ebb9e166.jpg
wget -O tmp/pocus_images/convex/Pneu_sonographiebilder2.jpg https://sonographiebilder.de/fileadmin/_migrated/pics/Pneumonie__3_.jpg
wget -O tmp/pocus_videos/linear/Cov_linear_abrams_2020_v1.mp4 https://www.jem-journal.com/cms/10.1016/j.jemermed.2020.06.032/attachment/69e81993-824e-4a79-9b61-8683b242a328/mmc1.mp4
wget -O tmp/pocus_images/convex/Cov_siemens_1.png https://static.healthcare.siemens.com/siemens_hwem-hwem_ssxa_websites-context-root/wcm/idc/groups/public/@global/documents/image/mda5/nzg3/~edisp/jun-5c1-lung-hepatization-07275343/~renditions/jun-5c1-lung-hepatization-07275343~8.jpg
wget -O tmp/pocus_images/convex/Cov_siemens_2.png https://static.healthcare.siemens.com/siemens_hwem-hwem_ssxa_websites-context-root/wcm/idc/groups/public/@global/documents/image/mda5/nzg3/~edisp/jun-5c1-lung-4-b-lines-07275344/~renditions/jun-5c1-lung-4-b-lines-07275344~8.jpg 
wget -O tmp/pocus_images/linear/Cov_siemens_3.png https://static.healthcare.siemens.com/siemens_hwem-hwem_ssxa_websites-context-root/wcm/idc/groups/public/@global/documents/image/mda5/nzg3/~edisp/seq-10l4-lung-b-lines-pleuritis-07275337/~renditions/seq-10l4-lung-b-lines-pleuritis-07275337~8.jpg
wget -O tmp/pocus_videos/linear/Reg_siemens_vid_3.mp4 "https://house-fastly-signed-eu-west-1-prod.brightcovecdn.com/media/v1/hls/v4/clear/2744552178001/5ef91327-742a-48cb-9ade-d04374e5dcac/49587bc4-0dac-48b4-ba3a-93d41d44cbf0/5x/segment0.ts?fastly_token=NjAwNGU4ZjNfMTQxNWMwMjBlNjI0NTEwMTBhNzE3OTBiYTY2M2Q3NWNmZTdkMDM4NDIwNzhjNDVhNmVhOWM0YzMzZTY4ZGMxN18vL2hvdXNlLWZhc3RseS1zaWduZWQtZXUtd2VzdC0xLXByb2QuYnJpZ2h0Y292ZWNkbi5jb20vbWVkaWEvdjEvaGxzL3Y0L2NsZWFyLzI3NDQ1NTIxNzgwMDEvNWVmOTEzMjctNzQyYS00OGNiLTlhZGUtZDA0Mzc0ZTVkY2FjLzQ5NTg3YmM0LTBkYWMtNDhiNC1iYTNhLTkzZDQxZDQ0Y2JmMC8%3D"
wget -O tmp/pocus_images/convex/Reg_Chen_2020_3A.png https://cdn.amegroups.cn/journals/amepc/files/journals/8/articles/46675/public/46675-PB8-6552-R1.png 
wget -O tmp/pocus_images/convex/Reg_Chen_2020_6A.png https://cdn.amegroups.cn/journals/amepc/files/journals/8/articles/46675/public/46675-PB8-6552-R1.png
wget -O tmp/pocus_images/convex/Pneu_Reissig_2012_fig2A.jpg https://ars.els-cdn.com/content/image/1-s2.0-S0012369212605662-gr2.jpg 
wget -O tmp/pocus_images/convex/Pneu_Reissig_2012_fig2B.jpg https://ars.els-cdn.com/content/image/1-s2.0-S0012369212605662-gr2.jpg 
youtube-dl -f 134 -o "tmp/pocus_videos/convex/Pneu_Youtube_case.mp4" https://www.youtube.com/watch?v=UnMeUrakOmc&feature=emb_logo
wget -O tmp/pocus_images/convex/Cov_wfumb_case_dez_a.jpg https://wfumb.info/wp-content/uploads/2020/12/wfumb-dec2pics.png
wget -O tmp/pocus_images/convex/Cov_wfumb_case_dez_b.jpg https://wfumb.info/wp-content/uploads/2020/12/wfumb-dec2pics.png
wget -O tmp/pocus_images/convex/Cov_wfumb_case_dez_c.jpg https://wfumb.info/wp-content/uploads/2020/12/wfumb-dec2pics.png
youtube-dl -f 134 -o "tmp/pocus_videos/convex/Cov_wfumb_case_dez.mp4" "https://www.youtube.com/watch?v=CpXPimphNSM&feature=youtu.be"
wget -O tmp/pocus_videos/convex/Cov_Arnthfield_2020_Vid3.mp4 https://www.medrxiv.org/content/medrxiv/early/2020/10/22/2020.10.13.20212258/DC3/embed/media-3.mp4

echo "Data fetched. Postprocessing..."

python3 crop_processed_data.py

rm -rf tmp
echo "Done, shutting down."
