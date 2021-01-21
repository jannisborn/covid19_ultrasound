import cv2
import os
import json
import matplotlib.pylab as plt


def read_first_frame(fp):
    cap = cv2.VideoCapture(fp)
    ret, cropped = cap.read()
    if cropped is None:
        cap = cv2.VideoCapture(".".join(fp.split(".")[:-1]) + ".mp4")
        ret, cropped = cap.read()
        print("changed to mp4")
    return cropped, cap


path = "../../../data_pocovid/DATASET"

with open("../../data/crop.json", "r") as infile:
    crop_dir = json.load(infile)

path_cropped = "../../../covid19_pocus_ultrasound/data/"
for folder in [
    "pocus_videos/convex", "pocus_videos/linear", "pocus_images/convex",
    "pocus_images/linear"
]:
    for filename in os.listdir(os.path.join(path, folder)):
        print(filename)
        if os.path.join(folder, filename) in crop_dir.keys():
            print("already done")
            continue
        if filename[0] == ".":
            continue
        # cropped, _ = read_first_frame(os.path.join(path_cropped, folder, filename))
        # normal, cap = read_first_frame(os.path.join(path, folder, filename))
        print(os.path.exists(os.path.join(path, folder, filename)))
        cap = cv2.VideoCapture(os.path.join(path, folder, filename))
        ret, frame = cap.read()
        print(ret)
        # x,y, _ = cropped.shape
        # for i in range(normal.shape[0]-x):
        #     for j in range(normal.shape[1]-y):
        #         patch = normal[i:i+x, j:j+y]
        #         if np.all(patch == cropped):
        #             print("FOUND")
        # crop

        x, y, _ = frame.shape
        min_shape = min([x, y])
        # crop = [int(0.1*x), int(y/2-0.9*min_shape/2), int(0.9 * min_shape)]
        crop = [0, 0, min_shape]
        while True:
            bottom, left, size = crop
            # count = 0
            # while cap.isOpened() and count< 1:
            plt.imshow(frame[bottom:bottom + size, left:left + size])
            plt.show()
            crop_in = input("okay?")
            if crop_in == 1 or crop_in == "1":
                crop_dir[os.path.join(folder,
                                      filename)] = [crop, [0, cap.get(7)]]
                break
            if crop_in == "0":
                ret, frame = cap.read()
            else:
                crop_in = input("input list " + str(crop))
                crop = eval(crop_in)
                print(crop)

with open("../../data/crop.json", "w") as infile:
    json.dump(crop_dir, infile)
