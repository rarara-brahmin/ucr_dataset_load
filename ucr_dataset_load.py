### Download UCR dataset

import os
import urllib.request
import pyzipper
import numpy as np

datasetURL = "https://www.cs.ucr.edu/~eamonn/time_series_data_2018/UCRArchive_2018.zip"
datasetPath = "./UCRArchive_2018.zip"
datasetTitle = "UCRArchive_2018.zip"

datalistURL = "https://www.cs.ucr.edu/~eamonn/time_series_data_2018/DataSummary.csv"
datalistPath = "./DataSummary.csv"
datalistTitle = "DataSummary.csv"

# Constant Variable
_ID = 0
_Type = 1
_Train = 2
_Test = 3
_Class = 4
_Length = 5
_ED = 6
_DTW_learned_w = 7
_DTW_w_100 = 8
_Default_rate = 9
_Data_donor_editor = 10

def download():
    if( os.path.isfile(datasetPath) ):
        print("UCR Archive is already downloaded.")
    else:
        print("Datasets Downloading...")
        urllib.request.urlretrieve(datasetURL, "{0}".format(datasetTitle))
        print("Complete!")
    
    if( os.path.isfile(datalistTitle) == False):
        print("Datalist Downloading...")
        urllib.request.urlretrieve(datalistURL, "{0}".format(datalistTitle))
        print("Complete!")
    
    return

def extract( password ):
    bytePwd = password.encode('utf-8')
    print("Extracting...")

    with pyzipper.AESZipFile(datasetPath) as f:
        f.extractall(pwd=bytePwd)

    print("Complete!")

    return

def download_and_extract( password ):
    download()
    extract(password)

    return

def get_datalist():
    print(datalistPath)
    dataname = np.loadtxt(datalistPath, dtype="unicode", delimiter=",", skiprows=1, usecols=(2))
    datalist = np.loadtxt(datalistPath, dtype="unicode", delimiter=",", skiprows=1, usecols=(0,1,3,4,5,6,7,8,9,10,11))

    return( dict(zip(dataname, datalist)) )

    
def get_data( datasetName ):
    traindataPath = "./UCRArchive_2018/" + datasetName + "/" + datasetName + "_TRAIN.tsv"
    testdataPath = "./UCRArchive_2018/" + datasetName + "/" + datasetName + "_TEST.tsv"

    datalist_dict = get_datalist()

    if(datalist_dict[datasetName][_Length] != "Vary"):
        # Get data length from DataSummary file.
        dataLength = int(datalist_dict[datasetName][_Length])

        # Get train data
        train_data = np.loadtxt(traindataPath, dtype="float", delimiter= "\t", skiprows=0, usecols=(tuple(np.arange(1,dataLength))))
        
        # Get train label
        train_label = np.loadtxt(traindataPath, dtype="int", delimiter= "\t", skiprows=0, usecols=(0))
        
        # Get test data
        test_data = np.loadtxt(testdataPath, dtype="float", delimiter= "\t", skiprows=0, usecols=(tuple(np.arange(1,dataLength))))
        
        # Get train label
        test_label = np.loadtxt(testdataPath, dtype="int", delimiter= "\t", skiprows=0, usecols=(0))

        # print(train_data)
        # print(train_label)
        # print(test_data)
        # print(test_label)


    else:
        print("'Vary' length dataset is not supported.")
        train_data = np.arange(0)
        train_label = np.arange(0)
        test_data = np.arange(0)
        test_label = np.arange(0)

    return(train_data, train_label, test_data, test_label)

    

