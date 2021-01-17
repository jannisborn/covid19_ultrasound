# Keys are filnames, values are tuples, first for cropping size, second for triming
# CROPPING_DICT={
#     'pocus_videos/convex/Cov-clarius.gif':
#     'pocus_videos/convex/Cov-clarius3.gif': # Was formerly MP$
#     'pocus_images/convex/Pneu_clarius.jpg':
#     'pocus_images/convex/Pneu_clarius2.png':
#     'pocus_videos/convex/pneu-everyday.gif':
#     'pocus_videos/convex/Reg-nephropocus.gif': # Formerly mp4
#     'pocus_videos/convex/Reg-bcpocus.gif': # Remove last frame
#     'pocus_videos/convex/Reg-Youtube.mp4': # Needs some trimming, this comes from youtube. Our video is a concatenation of TWO short seconds of this vid.
#     'pocus_videos/linear/Reg-Youtube-start20sec.mp4': # Needs triming and cropping left part, since right and left part of smae vid aare used
#     'pocus_videos/linear/Pneu-Youtube-start20sec.mp4': # Same vid as above, cropped differently
#     'pocus_videos/linear/Reg-Youtube-Video_902_Lung_POCUS-left.mp4': # Croping to left but no triming needed
#     'pocus_videos/linear/Reg-nephropocus.gif':
#     'pocus_videos/linear/Reg-NormalLung.gif': # Formerly mp4, maybe no cropping
#     'pocus_videos/linear/Reg-minimalmovement.gif': # Formerly mp4, maybe no cropping
#     'pocus_videos/convex/Reg_Alines-1-90.mov':
#     'pocus_videos/convex/Pneu_AIR BRONC2.mov':
#     'pocus_videos/convex/Cov-grepmed-blines-pocus-.mp4':
#     'pocus_videos/convex/Cov-grepmed2.mp4':
#     'pocus_videos/convex/pneu-gred-6.gif':
#     'pocus_videos/convex/Pneu-grep-pneumonia1.mp4':
#     'pocus_videos/convex/Pneu-grep-pneumonia2_1.mp4': # Needs triming (last 3 sec show XRay)
#     'pocus_videos/convex/Pneu-grep-pneumonia4.mp4':
#     'pocus_videos/convex/pneu-gred-7.gif':
#     'pocus_videos/convex/Pneu-grep-pneumonia3.mp4':
#     'pocus_videos/convex/Reg-Grep-Alines.mp4':
#     'pocus_videos/convex/Reg-Grep-Normal.gif':
#     'pocus_videos/convex/Pneu-grep-shredsign-consolidation.mp4':
#     'pocus_videos/convex/Pneu-grep-bacterial-hepatization-clinical.mp4':
#     'pocus_videos/convex/Pneu-grep-pulmonary-pneumonia.mp4':
#     'pocus_videos/convex/Cov-grep-7543.mp4':
#     'pocus_videos/convex/Cov-grep-7525.mp4':
#     'pocus_videos/convex/Cov-grep-7511.mp4':
#     'pocus_videos/convex/Cov-grep-7510.mp4':
#     'pocus_videos/convex/Cov-grep-7507.mp4':
#     'pocus_videos/convex/Cov-grep-7505.mp4':
#     'pocus_videos/convex/Cov-grep-7453.mp4':
#     'pocus_videos/linear/Reg-grep-normal-alines-original.mp4':
#     'pocus_videos/linear/Cov-grep-7500.mp4':
#     'pocus_videos/linear/Cov-grep-7432.mp4': # Have to cut end off. Also a sec in the middle with black screen
#     'pocus_videos/linear/Cov-grep-7431.mp4':
#     'pocus_videos/convex/Reg_alines_advancesVid4.mp4':
#     'pocus_videos/convex/Vir_blines_advancesVid9.mp4':
#     'pocus_videos/convex/Pneu_consol_advancesVid10.mp4':
#     'pocus_videos/convex/Reg_clinicalreview_mov1.mp4':
#     'pocus_videos/convex/Pneu_clinicalreview_MOV4.mp4':
#     'pocus_images/convex/Cov_ablines_covidmanifestations_paper1.png':
#     'pocus_images/convex/Cov_blines_covidmanifestation_paper2.png':
#     'pocus_images/linear/Cov_irregularpleural_covidmanifestations_paper3.png':
#     'pocus_videos/convex/Cov_new_pregnant_vid1.avi':
#     'pocus_videos/convex/Cov_new_pregnant_vid2.avi':
#     'pocus_videos/convex/Cov_new_pregnant_vid3.avi':
#     'pocus_videos/convex/Cov_new_pregnant_vid4.avi':
#     'pocus_videos/convex/Cov_new_pregnant_vid5.avi':
#     'pocus_videos/convex/Cov_new_pregnant_vid6.avi':
#     'pocus_videos/convex/Cov_new_pregnant_vid7.avi':
#     'pocus_videos/convex/Cov_new_pregnant_vid8.avi':
#     'pocus_images/convex/Reg_com_acquired_paper.png': # Subfigure c
#     'pocus_images/convex/Pneu_air_bronchogram_com_acquired_paper.png': # subfigure a
#     'pocus_images/linear/Pneu_leftbasal_pedriatic_pneumonia.png':
#     'pocus_images/linear/Pneu_consol_pedriatic_pneumonia.png':
#     'pocus_images/convex/Cov_pregnantPublication1.png': # subfigure D
#     'pocus_images/convex/Cov_pregnantPublication2.png': # subfigure B
#     'pocus_images/convex/Cov_blines_thoraric_paperfig1.png':
#     'pocus_images/convex/Cov_blines_thoraric_paperfig2.png':
#     'pocus_images/convex/Cov_blines_thoraric_paperfig3.png': # Keep the subfigure at the top
#     'pocus_images/convex/Cov_pleuralthickening_thoraric_paperfig8.png':
#     'pocus_images/convex/Cov_whitelungs_thoraric_paperfig5.png':
#     'pocus_images/convex/Cov_pleuraleffusion_thoraric_paperfig9.png':
#     'pocus_images/convex/Cov_subpleuralthickening_thoraric_paperfig6.png': # Keep top figure
#     'pocus_images/convex/Cov_efsumb1.png': # Keep left
#     'pocus_images/convex/Cov_efsumb1_2.png': # Keep right
#     'pocus_images/convex/Cov_efsumb3.png':
#     'pocus_images/convex/Reg_efsumb2.png':
#     ### The next three images were cropped from a multi-page PDF. in wget the pdf is downlaoded 3x and saved as '.pdf'.
#     ### Script should ideally save the extracted imgs as .png and delete the respective .pdf
#     'pocus_images/convex/Pneu_bikus2.pdf': # Page 21
#     'pocus_images/convex/Pneu_bikus3.pdf': # Page 22
#     'pocus_images/convex/Reg_bikus.pdf': # Page 7 (links)
#     ###
#     'pocus_images/convex/Pneu_sonographiebilder1.jpg':
#     'pocus_images/convex/Pneu_sonographiebilder2.jpg':
#     ## Next 3 are also from PDF. Again, cropped imgs should be saved as filename.png and .pdf should be deleted
#     'pocus_images/convex/Reg_acutemedicine.pdf': # Figure at top left
#     'pocus_images/convex/Cov_severe_acutemedicine.pdf': # Second last row, leftmost column
#     'pocus_images/linear/Cov_blines_acutemedicine.pdf': #  Third row, leftmost column
#     # ##
#     'pocus_videos/linear/Cov_linear_abrams_2020_v1.mp4':

import cv2
import os
import json
import numpy as np
import matplotlib.pyplot as plt

DISPLAY_IMG = False

# input path with uncropped videos
path = "../../data_pocovid/DATASET/"

# path where to output the final videos
final_path = "../../data_pocovid/DATASET/test_videos"
if not os.path.exists(final_path):
    os.makedirs(final_path)
    os.makedirs(os.path.join(final_path, "pocus_videos/convex"))
    os.makedirs(os.path.join(final_path, "pocus_videos/linear"))
    os.makedirs(os.path.join(final_path, "pocus_images/convex"))
    os.makedirs(os.path.join(final_path, "pocus_images/linear"))

# load json with crop
with open("crop.json", "r") as infile:
    crop_dir = json.load(infile)

for key in crop_dir.keys():
    save_video_path = os.path.join(final_path, key)

    # get crop and trimming
    start, end = crop_dir[key][1]
    bottom, left, size = crop_dir[key][0]

    print(key, crop_dir[key])

    # read video
    cap = cv2.VideoCapture(os.path.join(path, key))

    # Image processing
    if cap.get(7) < 2:
        ret, frame = cap.read()
        frame = frame[bottom:bottom + size, left:left + size]
        cv2.imwrite(save_video_path, frame)
        continue

    video_array = []
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    for i in range(int(end - start)):
        ret, frame = cap.read()
        cropped = frame[bottom:bottom + size, left:left + size]
        if i == 0 and DISPLAY_IMG:
            plt.imshow(cropped)
            plt.show()
        video_array.append(cropped)

    # write video
    print(np.array(video_array).shape)
    video_path = ".".join(save_video_path.split(".")[:-1])
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # XVID
    writer = cv2.VideoWriter(
        video_path + '.mp4', fourcc, cap.get(5), cropped.shape[:2]
    )
    for x in video_array:
        writer.write(x.astype("uint8"))
    writer.release()
