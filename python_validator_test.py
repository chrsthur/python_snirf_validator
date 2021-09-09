import h5py as h5py
import numpy as np
import re
import colorama
from colorama import Fore, Style
import sys

def validate(filename, optionalList):
    fileID = h5py.File(filename, 'r')

    def checkSpecialCase(required, requiredIndex, child):
        if 'sourcePos2D' in child or 'detectorPos2D' in child:
            if 'sourcePos2D' not in required and 'detectPos2D' not in required:
                required.append("sourcePos2D")
                requiredIndex.append(0)
                required.append("detectorPos2D")
                requiredIndex.append(0)
            childForCheck = child
        elif 'sourcePos3D' in child or 'detectorPos3D' in child:
            if 'sourcePos3D' not in required and 'detectPos3D' not in required:
                required.append("sourcePos3D")
                requiredIndex.append(0)
                required.append("detectorPos3D")
                requiredIndex.append(0)
            childForCheck = child
        elif 'landmarkPos' in child:
            childForCheck = child
        else:
            childForCheck = ''.join(i for i in child if not i.isdigit())
        return required, requiredIndex, childForCheck

    def printEverything(gID, child, optionalList, requireFlag):
        if requireFlag == True:
            if isinstance(gID[child], h5py.Dataset):
                if "stim" in gID.name or "aux" in gID.name:
                    print(Fore.WHITE + '\t' + gID.name + '/' + child)
                    print(Fore.GREEN + '\t\tRequired Dataset When Parent Group ' + gID.name + ' Presents')
                else:
                    print(Fore.WHITE + '\t' + gID.name + '/' + child)
                    print(Fore.GREEN + '\t\tRequired Dataset')
            if isinstance(gID[child], h5py.Group):
                print(Fore.MAGENTA + gID[child].name)
                print(Fore.GREEN + '\tRequired Indexed Group')
        else:
            OptionalFlag = False
            for x in optionalList:
                if re.match(x, gID[child].name):
                    if isinstance(gID[child], h5py.Dataset):
                        print(Fore.WHITE + '\t' + gID.name + '/' + child)
                        print(Fore.BLUE + '\t\tOptional Dataset')
                        OptionalFlag = True
                        break
                    if isinstance(gID[child], h5py.Group):
                        print(Fore.MAGENTA + gID[child].name)
                        print(Fore.BLUE + '\tOptional Indexed Group')
                        OptionalFlag = True
                        break
            if OptionalFlag == False:
                if isinstance(gID[child], h5py.Dataset):
                    if 'metaDataTags' in gID.name:
                        print(Fore.WHITE + '\t' + gID.name + '/' + child)
                        print(Fore.YELLOW + '\t\tUser Defined optional Dataset')
                    else:
                        print(Fore.WHITE + '\t' + gID.name + '/' + child)
                        print(Fore.RED + '\t\tInvalid Dataset')
                        invalidDatasetList.append(gID.name)
                if isinstance(gID[child], h5py.Group):
                    print(gID.name)
                    print(Fore.RED + '\tInvalid Indexed Group')
                    invalidGroupList.append(gID.name)

    def getRequiredDataset(gID):
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
            return 0
        return required

    def checkGroupChild(gID, required):
        requiredIndex = [0] * len(required)
        for child in gID:
            requireFlag = False
            if any(chr.isdigit() for chr in child):
                [required, requiredIndex, childForCheck] = checkSpecialCase(required, requiredIndex, child)
            else:
                childForCheck = child
            if childForCheck in required:  # if child in RequiredField, change RequiredIndex
                requiredIndex[required.index(childForCheck)] = 1
                requireFlag = True
            printEverything(gID, child, optionalList, requireFlag)
            getAllNames(gID[child])
        if 0 in requiredIndex:  # check if requiredIndex has 0, if so, append the name
            for i in range(len(required)):
                if requiredIndex[i] == 0:
                    missingList.append(Name + '/' + required[i])

    def CheckDataset(gID):

        def checkSpecDim(gID):
            if "Pos2D" in gID.name or "Pos3D" in gID.name:
                dim = 2
            elif "dataTimeSeries" in gID.name:
                if "aux" in gID.name:
                    dim = 1
                else:
                    dim = 2
            elif "measurementList" in gID.name:
                if "dataTypeLabel" in gID.name:
                    dim = 1
                else:
                    dim = 0
            elif "stim" in gID.name and "data" in gID.name:
                if "dataLabels" in gID.name:
                    dim = 1
                else:
                    dim = 2
            else:
                dim = 1
            if dim != len(gID.dims):
                return False, dim
            else:
                return True, dim

        def reCheck(gID):
            if gID.shape == (1,):
                return True
            else:
                return False

        dimCheck, actualDim = checkSpecDim(gID)
        if h5py.check_string_dtype(gID.dtype): # string
            if gID.len() == 1:
                val = gID[0].decode('ascii')
                print(Fore.CYAN + '\t\tHDF5-STRING: {0}'.format(val))
            else:
                val2 = []
                for y in gID:
                    val2.append(y.decode('ascii'))
                val2 = np.array(val2)
                print(Fore.CYAN + '\t\tHDF5-STRING 1D-Vector: <{0}x1>'.format(len(val2)))
        else:
            val = np.array(gID)
            if val.ndim == 1:
                if len(val) == 1:
                    val = val[0]
                    print(Fore.CYAN + '\t\tHDF5-FLOAT: {0}'.format(val))
                    if not dimCheck:
                        dimCheck = reCheck(gID)
                else:
                    print(Fore.CYAN + '\t\tHDF5-FLOAT 1D-Vector: <{0}x1>'.format(len(val)))
            elif val.ndim == 0:
                print(Fore.CYAN + '\t\tHDF5-Integer 0D-Scalar <0x0>')
            else:
                print(Fore.CYAN + '\t\tHDF5-FLOAT 2D-Array: <{0}x{1}>'.format(len(val), int(val.size / len(val))))

        if not dimCheck:
            print(Fore.RED + '\t\tINVALID dimensions(Expected Number of Dimensions: ' + str(actualDim) + ')')
            invalidDatasetList.append(gID.name)

    def getAllNames(gID):
        if isinstance(gID, h5py.File):
            required = ["formatVersion", "nirs"]
            checkGroupChild(gID, required)
        elif isinstance(gID, h5py.Group):
            required = getRequiredDataset(gID)
            checkGroupChild(gID, required)
        elif isinstance(gID, h5py.Dataset):
            completeList.append(gID.name)
            CheckDataset(gID)
        else:
            return 0

    completeList = []
    missingList = []
    invalidGroupList = []
    invalidDatasetList = []

    getAllNames(fileID)

    print(missingList)
    print(invalidGroupList)
    print(invalidDatasetList)

def main():
    optionalList = ["/nirs\d*/data\w*/measurementList\d*/wavelengthActual",
                "/nirs\d*/data\w*/measurementList\d*/wavelengthEmissionActual",
                "/nirs\d*/data\d*/measurementList\d*/dataTypeLabel",
                "/nirs\d*/data\w*/measurementList\d*/sourcePower",
                "/nirs\d*/data\w*/measurementList\d*/detectorGain",
                "/nirs\d*/data\w*/measurementList\d*/moduleIndex",
                "/nirs\d*/data\w*/measurementList\d*/sourceModuleIndex",
                "/nirs\d*/data\w*/measurementList\d*/detectorModuleIndex", 
                "/nirs\d*/probe/wavelengthsEmission","/nirs\d*/probe/frequencies",
                "/nirs\d*/probe/timeDelays", "/nirs\d*/probe/timeDelayWidths", "/nirs\d*/probe/momentOrders",
                "/nirs\d*/probe/correlationTimeDelays", "/nirs\d*/probe/correlationTimeDelayWidths",
                "/nirs\d*/probe/sourceLabels", "/nirs\d*/probe/detectorLabels", "/nirs\d*/probe/landmarkPos2D",
                "/nirs\d*/probe/landmarkPos3D", "/nirs\d*/probe/landmarkLabels", "/nirs\d*/probe/useLocalIndex",
                "/nirs\d*/aux\d*/timeOffset", "/nirs\d*/stim\d*/dataLabels","/nirs\d*/stim\d*","/nirs\d*/aux\d*"]

    filename=sys.argv[1]
    print(Fore.MAGENTA + filename)
    validate(filename, optionalList)

if __name__ == "__main__":
    main()