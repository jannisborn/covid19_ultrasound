import os
import pandas as pd


def get_paths(data_table_path):
    """
    Get the filenames of our data from csv file
    """
    data_table = pd.read_csv(data_table_path)
    butterfly = data_table["Filename"].values
    butterfly = [b for b in butterfly if "utterfly" in b]
    actual_names = [b.split("Butterfly-")[-1] for b in butterfly]
    labels = [b[:3] for b in butterfly]
    return actual_names, labels


def get_processing_info(data_path, actual_names, labels):
    """
    Iterates over the downloaded data and checks which one is in our database
    Returns:
        files_to_process: List of file paths to videos
        labs_to_process: list of same length with corresponding labels
    """
    files_to_process = []
    labs_to_process = []
    for img_type in os.listdir(data_path):
        if img_type[0] == ".":
            continue
        # img_type is B-lines, cardiac etc
        for vid in os.listdir(os.path.join(data_path, img_type)):
            # print(vid)
            if vid in actual_names:
                full_path = os.path.join(data_path, img_type, vid)
                files_to_process.append(full_path)
                ind = actual_names.index(vid)
                labs_to_process.append(labels[ind])
    return files_to_process, labs_to_process


def makedirs(out_dir):
    for mod in ["covid", "pneumonia", "regular"]:
        if not os.path.exists(os.path.join(out_dir, mod)):
            os.makedirs(os.path.join(out_dir, mod))


def label_to_dir(lab):
    if lab == "Cov":
        label = "covid"
    elif lab == "Pne" or lab == "pne":
        label = "pneumonia"
    elif lab == "Reg":
        label = "regular"
    else:
        raise ValueError("Wrong label! " + lab)
    return os.path.join(label, lab + "-")
