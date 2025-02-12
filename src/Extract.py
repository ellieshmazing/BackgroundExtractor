'''Program to extract image of setting from video'''
import os
import sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st

#Function to save output images
#Input: Output path, array of images, array of image names
#Output: None
def saveImages(outPath, imgOutputs, imgNames):
    #Create output directory if nonexistent
    if (not os.path.exists(outPath)):
        os.mkdir(outPath)
        
    #Iterate through imgOutputs and save images by corresponding title in imgNames
    for index, img in enumerate(imgOutputs):
        cv.imwrite(outPath + imgNames[index] + ".jpg", img)
        
        
#Function to extract setting from video
#Input: Video
#Output: Frame of setting void of moving objects
def extractBackground(vid):
    print("Initializing extraction process...")
    #Read first frame and frame count
    ret, frame = vid.read()
    frameTot = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
    frameCount = 0
    
    #Declare array to hold video frames set to size of initial frame
    vidFramesShape = [frameTot]
    vidFramesShape += frame.shape
    vidFrames = np.zeros((vidFramesShape), dtype=np.uint8)
    vidFrames[frameCount] = frame
    
    print("Separating video frames...")
    #Iterate through video while frames remain
    while(vid.isOpened() and ret):
        #Read next frame
        ret, frame = vid.read()
        frameCount += 1
        
        #Check that frame exists
        if (ret):
            #Add frame to array
            vidFrames[frameCount] = frame
            
    #Declare NumPy array to hold output frame
    bgImg = np.zeros((vidFrames[0].shape), np.uint8)
    bgHeight, bgWidth = bgImg.shape[:2]
    
    print("Calculating mode of each pixel...")
    #Set bgImg to mode of each pixel in video frames
    bgImg[:,:,:] = st.mode(vidFrames[:,:,:,:]).mode

    print("Success!")
    #Return extracted frame
    return bgImg
        
        
#Get paths for input images, output directory, and small/large-scale sigma values
srcDir = os.path.dirname(os.path.abspath(__file__))
inPath = str(srcDir + '\\' + sys.argv[1])
outPath = str(srcDir + '\\' + sys.argv[2])


#Read in input video
vid = cv.VideoCapture(inPath)

#Extract background
bgImg = extractBackground(vid)


#Create arrays to hold output images and their filenames, and add result
imgOutputs = []
imgNames = []

imgOutputs.append(bgImg)
imgNames.append("Result")

#Save images
saveImages(outPath, imgOutputs, imgNames)