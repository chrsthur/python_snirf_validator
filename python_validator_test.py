import h5py as h5py
import numpy as np
import re
import colorama
from colorama import Fore, Style
import sys

def hdfgetdata(gID, field):
    val = gID.get(field)
    if val is None:
        return val
    if h5py.check_string_dtype(val.dtype):
        # string
        if val.len() == 1:
            val = val[0].decode('ascii')
            return val
        else:
            val2 = []
            for x in val:
                val2.append(x.decode('ascii'))
            val2 = np.array(val2)
            return val2
    val = np.array(val)
    if (val.ndim == 1 and len(val) == 1):
        val = val[0]
    return val

def validate(filename, fileOut=None):
    fileID = h5py.File(filename, 'r')

    def getallnames(gID, completeList, missingList):
        if isinstance(gID, h5py.File):
            required = ["formatVersion", "nirs"]
            requiredIndex = [0] * len(required)
            for child in gID:
                if child in required: # if child in RequiredField, change RequiredIndex
                    requiredIndex[required.index(child)] = 1
                else:
                    print(Fore.RED + "\tInvalid Group: " + str(child))
                getallnames(gID[child], completeList, missingList)
            if 0 in requiredIndex: # check if requiredIndex has 0, if so, append the name
                missingList.append(required[requiredIndex.index(0)])
        elif isinstance(gID, h5py.Group):
            if 'nirs' in gID.name:
                required = ["metaDataTag", "data", "probe"]
            elif 'data' in gID.name:
                required = ["dataTimeSeries", "time", "measurementList"]
            else:
                print(Fore.RED + "\tInvalid Group: " + str(gID.name))

            # if gID is /nirs, requiredfield = ["metaDataTag","data","probe"]
            # if gID is /data, requireField = ["dataTimeSeries","time","measurementList"]
            # if gID is /measurementList, requiredField = [sourceIndex,detectorIndex,wavelengthIndex,dataType,dataTypeIndex]
            # if gID is /stim, requiredField = [name,data]
            # if gID is /aux, requiredField = [name,data,time]
            for child in gID:
                # if child in the Required, change requirefield index
                getallnames(gID[child], completeList, missingList)
            # check if requiredFieldIndex has 0, if not, no missing field
        elif isinstance(gID, h5py.Dataset):
            completeList.append(gID.name)
            # required/optional check
            # datatype check
            # dimension check
        else:
            return 0

    completeList = []
    missingList = []
    getallnames(fileID, completeList,missingList)

def main():
    filename=sys.argv[1]
    print(filename)
    validate(filename)

if __name__ == "__main__":
    main()