import h5py as h5py
import numpy as np
import re
import colorama
from colorama import Fore
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
                    print(Fore.MAGENTA + '\t' + gID.name + '/' + child)
                    print(Fore.GREEN + '\t\tRequired Dataset When Parent Group ' + gID.name + ' Presents')
                else:
                    print(Fore.MAGENTA + '\t' + gID.name + '/' + child)
                    print(Fore.GREEN + '\t\tRequired Dataset')
            if isinstance(gID[child], h5py.Group):
                print(Fore.MAGENTA + gID[child].name)
                print(Fore.GREEN + '\tRequired Indexed Group')
        else:
            OptionalFlag = False
            for x in optionalList:
                if re.match(x, gID[child].name):
                    if isinstance(gID[child], h5py.Dataset):
                        print(Fore.MAGENTA + '\t' + gID.name + '/' + child)
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
                        print(Fore.MAGENTA + '\t' + gID.name + '/' + child)
                        print(Fore.YELLOW + '\t\tUser Defined optional Dataset')
                    else:
                        print(Fore.MAGENTA + '\t' + gID.name + '/' + child)
                        print(Fore.RED + '\t\tInvalid Dataset')
                        invalidDatasetNameList.append(gID.name)
                if isinstance(gID[child], h5py.Group):
                    print(Fore.MAGENTA + gID.name)
                    print(Fore.RED + '\tInvalid Indexed Group')
                    invalidGroupNameList.append(gID.name)

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
                    missingList.append(gID.name + '/' + required[i])

    def CheckDataset(gID):

        def GetSpec(gID):
            # check spec dimension
            if "Pos2D" in gID.name or "Pos3D" in gID.name:
                specDim = 2
            elif "dataTimeSeries" in gID.name:
                if "aux" in gID.name:
                    specDim = 1
                else:
                    specDim = 2
            elif "measurementList" in gID.name:
                if "dataTypeLabel" in gID.name:
                    specDim = 1
                else:
                    specDim = 0
            elif "stim" in gID.name and "data" in gID.name:
                if "dataLabels" in gID.name:
                    specDim = 1
                else:
                    specDim = 2
            else:
                specDim = 1

            # check spec data type
            if "metaDataTags" in gID.name or 'formatVersion' in gID.name:
                specType = str
            elif "name" in gID.name or "Label" in gID.name:
                specType = str
            elif "Index" in gID.name:
                specType = int
            elif "dataType" in gID.name:
                specType = int
            else:
                specType = float

            return specType, specDim

        # check spec datatype and dimension
        specType, specDim = GetSpec(gID)

        # check actual data type and dimension
        if h5py.check_string_dtype(gID.dtype):  # string
            actualDim = 1
            if gID.len() == 1:
                data = gID[0].decode('ascii')
                print(Fore.CYAN + '\t\tHDF5-STRING')
            else:
                data = []
                for y in gID:
                    data.append(y.decode('ascii'))
                data = np.array(data)
                print(Fore.CYAN + '\t\tHDF5-STRING 1D-Array')
        else:
            data = gID[()]
            if gID.ndim == 2:
                print(Fore.CYAN + '\t\tHDF5-FLOAT 2D-Array')
                actualDim = gID.ndim
            elif gID.ndim == 1:
                dimensions = gID.shape
                if dimensions[0] == 1:
                    print(Fore.CYAN + '\t\tHDF5-FLOAT Point')
                    actualDim = 0
                else:
                    print(Fore.CYAN + '\t\tHDF5-FLOAT 1D-Array')
                    actualDim = gID.ndim
            elif gID.ndim == 0:
                print(Fore.CYAN + '\t\tHDF5-Integer')
                actualDim = gID.ndim
            else:
                return

        if isinstance(data, (int, np.integer)):
            actualType = int
        elif gID.dtype == 'int64' or gID.dtype == 'int32':
            actualType = int
        elif isinstance(data, str) or h5py.check_string_dtype(gID.dtype):
            actualType = str
        else:
            actualType = float

        if "metaDataTags" in gID.name and not h5py.check_string_dtype(gID.dtype):
            # implies an user defined field since all required datasets are string
            actualType = specType
            actualDim = specDim

        # compare actual and spec, and print out correct statement
        if actualType.__name__ != specType.__name__:
            print(Fore.RED + '\t\tINVALID Data Type! Expecting: ' + str(specType.__name__) +
                  '! But ' + str(np.dtype(gID.dtype.type)) + ' was given.')
            invalidDatasetTypeList.append(gID.name)
        if actualDim != specDim:
            print(Fore.RED + '\t\tINVALID Data Dimension! Expecting: ' + str(specDim) +
                  '! But ' + str(gID.ndim) + ' was given.')
            invalidDatasetDimList.append(gID.name)

    def getAllNames(gID):
        if isinstance(gID, h5py.File):
            required = ["formatVersion", "nirs"]
            checkGroupChild(gID, required)
        elif isinstance(gID, h5py.Group):
            required = getRequiredDataset(gID)
            checkGroupChild(gID, required)
        elif isinstance(gID, h5py.Dataset):
            completeDatasetList.append(gID.name)
            CheckDataset(gID)
        else:
            return 0

    completeDatasetList = []
    missingList = []
    invalidGroupNameList = []
    invalidDatasetNameList = []
    invalidDatasetDimList = []
    invalidDatasetTypeList = []

    getAllNames(fileID)

    Decision = True
    if np.size(invalidGroupNameList) > 0:
        print(Fore.RED + "Invalid Group Detected: ")
        print(Fore.RED + str(invalidGroupNameList) + '\n')
        Decision = False
    if np.size(missingList) > 0:
        print(Fore.RED + "Missing Dataset/Group Detected: ")
        print(Fore.RED + str(missingList) + '\n')
        Decision = False
    if np.size(invalidDatasetNameList) > 0:
        print(Fore.RED + "Invalid Dateset Detected: " )
        print(Fore.RED + str(invalidDatasetNameList) + '\n')
        Decision = False
    if np.size(invalidDatasetTypeList) > 0:
        print(Fore.RED + "Invalid Dataset Data Type Detected: ")
        print(Fore.RED + str(invalidDatasetTypeList) + '\n')
        Decision = False
    if np.size(invalidDatasetDimList) > 0:
        print(Fore.RED + "Invalid Dataset Dimension Detected: " )
        print(Fore.RED + str(invalidDatasetDimList) + '\n')
        Decision = False


    return completeDatasetList, Decision

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

    fileName=sys.argv[1]
    print(Fore.MAGENTA + fileName)

    [CompleteDatasetList,Decision] = validate(fileName, optionalList)
    print(Fore.WHITE + '----------------------------------')
    if Decision == True:
        print(Fore.GREEN + fileName +  " is valid!")
    else:
        print(Fore.RED + fileName + " is invalid!")

if __name__ == "__main__":
    main()
