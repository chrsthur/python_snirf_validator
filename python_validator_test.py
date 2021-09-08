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

    def CheckRequiredIndex(Name,required,requiredIndex):
        if 0 in requiredIndex:  # check if requiredIndex has 0, if so, append the name
            for i in range(len(required)):
                if requiredIndex[i] == 0:
                    missingList.append(Name + '/' + required[i])

    def getallnames(gID, completeList, missingList):
        if isinstance(gID, h5py.File):
            required = ["formatVersion", "nirs"]
            requiredIndex = [0] * len(required)
            for child in gID:
                childNoNum = ''.join(i for i in child if not i.isdigit())
                if childNoNum in required:  # if child in RequiredField, change RequiredIndex
                    requiredIndex[required.index(childNoNum)] = 1
                else:
                    print(Fore.RED + "\tInvalid Indexed Group: " + str(child))
                getallnames(gID[child], completeList, missingList)
            CheckRequiredIndex(gID.name, required, requiredIndex)
        elif isinstance(gID, h5py.Group):
            print(gID.name)
            if 'measurementList' in gID.name:
                required = ["sourceIndex", "detectorIndex", "wavelengthIndex", "dataType", "dataTypeIndex"]
            elif 'data' in gID.name:
                required = ["dataTimeSeries", "time", "measurementList"]
            elif 'stim' in gID.name:
                required = ["name", "data"]
            elif 'aux' in gID.name:
                required = ["name", "dataTimeSeries", "time"]
            elif 'metaDataTags' in gID.name:
                required = ["SubjectID", "MeasurementDate", "MeasurementTime", "LengthUnit", "TimeUnit", "FrequencyUnit"]
            elif 'probe' in gID.name:
                required = ["wavelengths"]
            elif 'nirs' in gID.name:
                required = ["metaDataTags", "data", "probe"]
            else:
                print(Fore.RED + "\tInvalid Group: " + str(gID.name))
                return 0
            requiredIndex = [0] * len(required)

            for child in gID:
                if 'sourcePos2D' in child or 'detectorPos2D' in child:
                    if 'sourcePos2D' not in required and 'detectPos2D' not in required:
                        required.append("sourcePos2D")
                        requiredIndex.append(0)
                        required.append("detectorPos2D")
                        requiredIndex.append(0)
                    if child in required:
                        requiredIndex[required.index(child)] = 1
                elif 'sourcePos3D' in child or 'detectorPos3D' in child:
                    if 'sourcePos3D' not in required and 'detectPos3D' not in required:
                        required.append("sourcePos3D")
                        requiredIndex.append(0)
                        required.append("detectorPos3D")
                        requiredIndex.append(0)
                    if child in required:
                        requiredIndex[required.index(child)] = 1
                else:
                    childNoNum = ''.join(i for i in child if not i.isdigit())
                    if childNoNum in required:  # if child in RequiredField, change RequiredIndex
                        requiredIndex[required.index(childNoNum)] = 1
                    else: # check if optional


                getallnames(gID[child], completeList, missingList)
            CheckRequiredIndex(gID.name, required, requiredIndex)
        elif isinstance(gID, h5py.Dataset):
            completeList.append(gID.name)
            # datatype check
            # dimension check
        else:
            return 0

    completeList = []
    missingList = []
    getallnames(fileID, completeList, missingList)
    print(missingList)

def main():
    filename=sys.argv[1]
    print(filename)
    validate(filename)

if __name__ == "__main__":
    main()