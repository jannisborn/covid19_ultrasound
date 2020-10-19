import os
import pandas as pd 


# Define paths to results files
base_dir = "../results_oct/"
models_to_evaluate = ["base_new", "cam_new", "nasnet_new", "encoding", "segmented"]
vid_models_to_evaluate = ["frame_based_video_evaluation", "vid_based_video_evaluation"]

print()
print("---------------------------------")
print("FRAME BASED EVALUATION")
print("---------------------------------")

class_map2 = {0:"COVID-19", 1:"Pneumonia", 2: "Healthy",3:"Uninformative"}
for model in models_to_evaluate:
    mean_table = pd.read_csv(os.path.join(base_dir, model+"_mean.csv"))
    std_table = pd.read_csv(os.path.join(base_dir, model+"_std.csv"))
    print("----------", model, " ---------------")
    for i, row in mean_table.iterrows():
        std_row = std_table.loc[i] # std_table[std_table["Unnamed: 0"]=="covid"]
        # if i==1:
            # "& $", row["Accuracy"],"\\pm",std_row["Accuracy"],"$ &", 
        if i ==0:
            print(round(row["Accuracy"],2), std_row["Accuracy"], row["Balanced"], std_row["Balanced"])
        print("&", class_map2[i],
              "& $", round(row["Recall"], 2), "\\pm {\scriptstyle",std_row["Recall"],
              "}$ & $", round(row["Precision"],2), "\\pm {\scriptstyle",std_row["Precision"],
              "}$ & $", round(row["F1-score"], 2), "\\pm {\scriptstyle",std_row["F1-score"], 
              "}$ & $", round(row["Specificity"], 2), "\\pm {\scriptstyle",std_row["Specificity"],
              "}$ & $",round(row["MCC"], 2), "\\pm {\scriptstyle",std_row["MCC"], "} $ \\\\")      

print()
print("---------------------------------")
print("VIDEO EVALUATION")
print("---------------------------------")

class_map2 = {0:"COVID-19", 1:"Pneumonia", 2: "Healthy"}
for model in vid_models_to_evaluate:
    mean_table = pd.read_csv(os.path.join(base_dir, model+".csv"))
    print("----------", model)
    for i, row in mean_table.iterrows():
        std_row = std_table.loc[i] # std_table[std_table["Unnamed: 0"]=="covid"]
        # if i==1:
            # "& $", row["Accuracy"],"\\pm",std_row["Accuracy"],"$ &", 
        print(row["Accuracy"], row["Balanced"])
        
        # WO standard deviation
        print("&", class_map2[i],"&", row["recall"], 
                "&", row["precision"], "&", row["f1-score"], "&", row["Specificity"], "&", row["MCC"], "\\\\")
        