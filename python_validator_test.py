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

    def getallnames(gID, completeList,missingList):
        if isinstance(gID, h5py.File):
            Required = ["formatVersion", "nirs"]
            RequiredIndex = [0, 0]
            for child in gID:
                if child in Required: # if nirs/formatversion in RequiredField, change RequiredField Index
                    RequiredIndex[Required.index(child)] = 1
                else:
                    print(Fore.RED + "\tInvalid Group: " + str(child))
                getallnames(gID[child], completeList,missingList)
            missingList.append(Required[RequiredIndex.index(0)])
            # check if requiredFieldIndex has 0, if not, no missing field
        elif isinstance(gID, h5py.Group):
            # if gID is /nirs, requiredfield = ["metaDataTag","data","probe"]
            # if gID is /data, requireField = ["dataTimeSeries","time","measurementList"]
            # if gID is /measurementList, requiredField = [sourceIndex,detectorIndex,wavelengthIndex,dataType,dataTypeIndex]
            # if gID is /stim, requiredField = [name,data]
            # if gID is /aux, requiredField = [name,data,time]
            for child in gID:
                # if y in the requireField, change requirefield index
                getallnames(gID[child], completeList,missingList)
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