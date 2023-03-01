import os
import cv2
import numpy
from PIL import Image
import wsq
import shutil
import sys

class FingerData:

  def __init__(self, sample, file):
    self.main = file
    self.sample = sample
    # self.home = homeDir
    

  # Compares sample file with fingerprint entries
  def match(self):

    # sampleFile = os.listdir(self.destination)   # assigning sample file a variable
    sampleFile = numpy.array(Image.open("Temp/"+self.sample))
    best_score = 0.0

    # # Group finger data into an array
    # self.fileCount = len(os.listdir(self.dir))

    # if (self.fileCount%self.modulo):
    #     splitNum = self.fileCount%self.modulo
    # else:
    #     splitNum = (self.fileCount)/self.modulo 

    # self.dataList = numpy.array_split(os.listdir(self.dir), splitNum)

    # for i in range(len(self.dataList)):
    #   # print("Scanning Array: "+str(i))
    #   if (os.path.exists(self.home+"Temp")):
    #     shutil.rmtree(self.home+"Temp")

    #   for file in self.dataList[i]:
    #     filePath = self.dir+file
    #     self.sample_conversion(filePath, "Temp")

    #     filePath = self.home+"Temp/"+file+".png"
    dataFile = numpy.array(Image.open("Temp/"+self.main))

    # Matching Algorithm
    sift = cv2.SIFT_create()
    
    keypoints_1, descriptors_1 = sift.detectAndCompute(sampleFile, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(dataFile, None)

    matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10},
                                            {}).knnMatch(descriptors_1, descriptors_2, k=2)

    match_points = []
    for p, q in matches:
        if p.distance < 0.1 * q. distance:
            match_points.append(p)

    keypoints = 0
    if len (keypoints_1) < len (keypoints_2):
        keypoints = len(keypoints_1)
    else:
        keypoints = len(keypoints_2)

    if len (match_points) / keypoints * 100 > best_score:
        best_score = len(match_points) / keypoints * 100

    if best_score > 80.0:
      return {"response": 200, "score": best_score, "Name": self.main}
    
    return {"response": 404, "score": best_score, "Name": self.main}


  def clean(self):
    shutil.rmtree("Temp")



class FingerConversion:
  def __init__(self, file):
    self.file = file
    self.destination = "Temp"

  def sample_conversion(self):
    finger_image = Image.open(self.file)
    finger_image = finger_image.convert('L')

    try:
        os.mkdir(self.destination)
    except:
        print(self.destination+" folder exists.")

    name, ext = os.path.splitext(self.file)
    newName = name+".png"
    finger_image.save(newName)

    try:
      shutil.move(newName, self.destination)
      return str(newName)
    except:
      os.remove(newName)
      sys.exit(name+" is already in "+ self.destination + " folder, delete and restart process")  