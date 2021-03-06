import os
import sys
sys.path.append(os.path.join(".."))
import cv2
from pathlib import Path
import csv


#specifying data path 
data_path = os.path.join("..", "jpg", "*.jpg")

#specyfying the out directory - where the data is saved
outpath = os.path.join("..", "distance12.csv")


#Empty lists for results
results = []
new_results = ["filename", "distance"]


# target image path
target_image = os.path.join("..","jpg", "image_0006.jpg")

#Creating a histogram from the picture
target_image_hist = cv2.calcHist([target_image], [0,1,2], None, [8,8,8], [0,256, 0,256, 0,256])

#Normalizing the histogram
normalized_target_hist = cv2.normalize(target_image_hist, target_image_hist, 0,255, cv2.NORM_MINMAX)


#Loop that runs through the folder with all pictures and calculates t.
for image in Path(data_path).glob("*.jpg"):
    
    #OPening each image
    image_o = cv2.imread(str(image))
    
    #Creating histograms
    extract_hist = cv2.calcHist([image_o], [0,1,2], None, [8,8,8], [0,256, 0,256, 0,256])
    
    #Normalizing the histograms.
    normalize_hist = cv2.normalize(extract_hist, extract_hist, 0,255, cv2.NORM_MINMAX)
    
    #Coputing distances between every image and the target image.
    result = (round(cv2.compareHist(normalized_target_hist, normalize_hist, cv2.HISTCMP_CHISQR), 2))
    
    #Making sure identical pictures are not compared.
    if result > 0:
        results.append(f"{image}, {result}") #appending the result into the results list.
    



#writing a csv-file with columns: filename and distance
with open(outpath, "w", encoding="utf-8") as distance_file:
    writer = csv.writer(distance_file)    
    writer.writerow(["filename", "distance"])
    

#A loop that runs through the results.
for result in results:
    
    #Making sure the name only contains the image name - slicing the path
    sliced_names = result[22:36]
    
    #Slicing the result from the rest so only the difference is left.
    sliced_result = result[38:len(result)]
    
    #Now writing the sliced names and sliced results to the csv-file deffined in the outpath and appending each image and its distance.
    # 'a' is used instead of 'w' because we are appending and don't want to overwrite the Filename and Distance written in earlier.
    with open(outpath, 'a', newline='') as distance_file:
        writer = csv.writer(distance_file)
        writer.writerow([sliced_names, sliced_result])
    
    
    #appending to the list new_results above
    new_results.append(result[22:len(result)])
    