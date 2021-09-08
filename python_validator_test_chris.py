#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 3 13:28 2020
Updated on Tue Sep 7 21:48 2021

Original Author: theodorehuppert
Updated by Team Lemon
"""

import h5py as h5py
import numpy as np
import re
from colorama import Fore, Style
import sys


class measurementList:
    sourceIndex = None
    detectorIndex = None
    wavelengthIndex = None
    wavelengthActual = None
    wavelengthEmissionsActual = None
    dataType = None
    dataTypeLabel = None
    dataTypeIndex = None
    sourcePower = None
    detectorGain = None
    moduleIndex = None
    sourceModuleIndex = None
    detectorModuleIndex = None
    validFlag = 0
    missField = []


class data:
    dataTimeSeries = None
    time = None
    measurementList = measurementList()
    validFlag = 0
    missField = []


class probe:
    wavelengths = None
    wavelengthsEmission = None
    sourcePos2D = None
    sourcePos3D = None
    detectorPos2D = None
    detectorPos3D = None
    frequencies = None
    timeDelays = None
    timeDelayWidths = None
    momentOrder = None
    correlationTimeDelays = None
    correlationTimeDelayWidths = None
    sourceLabels = None
    detectorLabels = None
    landmarkPos2D = None
    landmarkPos3D = None
    landmarkLabels = None
    useLocalIndex = None
    validFlag = 0
    missField = []


class aux:
    name = None
    dataTimeSeries = None
    time = None
    timeOffSet = None
    validFlag = 0
    missField = []


class stim:
    name = None
    data = None
    dataLabels = None
    validFlag = 0
    missField = []


class metaDataTags:
    SubjectID = None
    MeasurementDate = None
    MeasurementTime = None
    LengthUnit = None
    TimeUnit = None
    FrequencyUnit = None
    validFlag = 0
    missField = []


class nirs:
    data = []
    stim = []
    probe = probe()
    aux = []
    metaDataTags = metaDataTags()
    validFlag = 0
    missField = []


class snirf:
    filename = None
    formatVersion = None
    nirs = []


def read_measurementList(gID):
    m = measurementList

    m.sourceIndex = hdfgetdata(gID, 'sourceIndex')
    m.detectorIndex = hdfgetdata(gID, 'detectorIndex')
    m.wavelengthIndex = hdfgetdata(gID, 'wavelengthIndex')
    m.wavelengthActual = hdfgetdata(gID, 'wavelengthActual')
    m.wavelengthEmissionsActual = hdfgetdata(gID, 'wavelengthEmissionsActual')
    m.dataType = hdfgetdata(gID, 'dataType')
    m.dataTypeLabel = hdfgetdata(gID, 'dataTypeLabel')
    m.dataTypeIndex = hdfgetdata(gID, 'dataTypeIndex')
    m.sourcePower = hdfgetdata(gID, 'sourcePower')
    m.detectorGain = hdfgetdata(gID, 'detectorGain')
    m.moduleIndex = hdfgetdata(gID, 'moduleIndex')
    m.sourceModuleIndex = hdfgetdata(gID, 'sourceModuleIndex')
    m.detectorModuleIndex = hdfgetdata(gID, 'detectorModuleIndex')

    reqField = [m.sourceIndex, m.detectorIndex, m.wavelengthIndex, m.dataType, m.dataTypeIndex]
    reqFieldName = ['sourceIndex', 'detectorIndex', 'wavelengthIndex', 'dataType', 'dataTypeIndex']

    if any(elem is None or (isinstance(elem, list) and len(elem) == 0) for elem in reqField):
        pass
    else:
        m.validFlag = 1

    for j in (i for i in range(len(reqField)) if reqField[i] is None):
        m.missField.append(reqFieldName[j])

    return m


def read_data(gID):
    d = data

    d.dataTimeSeries = hdfgetdata(gID, 'dataTimeSeries')
    d.time = hdfgetdata(gID, 'time')
    d.measurementList = []
    for fld in gID:
        if 'measurementList' in fld:
            d.measurementList.append(read_measurementList(gID[fld]))

    reqField = [d.dataTimeSeries, d.time, d.measurementList]

    if any(elem is None or (isinstance(elem, list) and len(elem) == 0) for elem in reqField):
        pass
    else:
        d.validFlag = 1

    return d


def read_probe(gID):
    p = probe

    p.wavelengths = hdfgetdata(gID, 'wavelengths')
    p.wavelengthsEmission = hdfgetdata(gID, 'wavelengthsEmission')
    p.sourcePos2D = hdfgetdata(gID, 'sourcePos2D')
    p.sourcePos3D = hdfgetdata(gID, 'sourcePos3D')
    p.detectorPos2D = hdfgetdata(gID, 'detectorPos2D')
    p.detectorPos3D = hdfgetdata(gID, 'detectorPos3D')
    p.frequencies = hdfgetdata(gID, 'frequencies')
    p.timeDelays = hdfgetdata(gID, 'timeDelays')
    p.timeDelayWidths = hdfgetdata(gID, 'timeDelayWidths')
    p.momentOrder = hdfgetdata(gID, 'momentOrder')
    p.correlationTimeDelays = hdfgetdata(gID, 'correlationTimeDelays')
    p.correlationTimeDelayWidths = hdfgetdata(gID, 'correlationTimeDelayWidths')
    p.sourceLabels = hdfgetdata(gID, 'sourceLabels')
    p.detectorLabels = hdfgetdata(gID, 'detectorLabels')
    p.landmarkPos2D = hdfgetdata(gID, 'landmarkPos2D')
    p.landmarkPos3D = hdfgetdata(gID, 'landmarkPos3D')
    p.landmarkLabels = hdfgetdata(gID, 'landmarkLabels')
    p.useLocalIndex = hdfgetdata(gID, 'useLocalIndex')

    if any(elem is not None for elem in [p.sourcePos2D, p.sourcePos3D]):
        sourcepos = 1
    else:
        sourcepos = None
    if any(elem is not None for elem in [p.detectorPos2D, p.detectorPos3D]):
        detectorpos = 1
    else:
        detectorpos = None
    reqField = [p.wavelengths, sourcepos, detectorpos]

    if any(elem is None or (isinstance(elem, list) and len(elem) == 0) for elem in reqField):
        pass
    else:
        p.validFlag = 1

    return p


def read_aux(gID):
    a = aux
    a.name = hdfgetdata(gID, 'name')
    a.dataTimeSeries = hdfgetdata(gID, 'dataTimeSeries')
    a.time = hdfgetdata(gID, 'time')
    a.timeOffSet = hdfgetdata(gID, 'timeOffSet')

    reqField = [a.name, a.dataTimeSeries, a.time]

    if any(elem is None or (isinstance(elem, list) and len(elem) == 0) for elem in reqField):
        pass
    else:
        a.validFlag = 1

    return a


def read_stim(gID):
    s = stim
    s.name = hdfgetdata(gID, 'name')
    s.data = hdfgetdata(gID, 'data')
    s.dataLabels = hdfgetdata(gID, 'dataLabels')

    reqField = [s.name, s.data]
    reqFieldName = ['name', 'data']

    if any(elem is None or (isinstance(elem, list) and len(elem) == 0) for elem in reqField):
        pass
    else:
        s.validFlag = 1

    for j in (i for i in range(len(reqField)) if reqField[i] is None):
        s.missField.append(reqFieldName[j])

    return s


def read_meta(gID):
    md = metaDataTags
    md.SubjectID = hdfgetdata(gID, 'SubjectID')
    md.MeasurementDate = hdfgetdata(gID, 'MeasurementDate')
    md.MeasurementTime = hdfgetdata(gID, 'MeasurementTime')
    md.LengthUnit = hdfgetdata(gID, 'LengthUnit')
    md.TimeUnit = hdfgetdata(gID, 'TimeUnit')
    md.FrequencyUnit = hdfgetdata(gID, 'FrequencyUnit')

    reqField = [md.SubjectID, md.MeasurementDate, md.MeasurementTime, md.LengthUnit, md.TimeUnit, md.FrequencyUnit]

    if any(elem is None or (isinstance(elem, list) and len(elem) == 0) for elem in reqField):
        pass
    else:
        md.validFlag = 1

    return md


def read_nirs(gID):
    n = nirs
    for fld in gID:
        if 'metaDataTags' in fld:
            n.metaDataTags = read_meta(gID[fld])
        elif 'data' in fld:
            n.data.append(read_data(gID[fld]))
        elif 'stim' in fld:
            n.stim.append(read_stim(gID[fld]))
        elif 'probe' in fld:
            n.probe = read_probe(gID[fld])
        elif 'aux' in fld:
            n.aux.append(read_aux(gID[fld]))

    reqField = [n.metaDataTags, n.data, n.probe]

    if any(elem is None or (isinstance(elem, list) and len(elem) == 0) for elem in reqField):
        pass
    else:
        n.validFlag = 1

    return n


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

    if val.ndim != 1 or len(val) != 1:
        pass
    else:
        val = val[0]

    return val


def getrequiredfieldsLst():
    Required = ["/formatVersion", "/nirs\d*/metaDataTags/SubjectID", "/nirs\d*/metaDataTags/MeasurementDate",
                "/nirs\d*/metaDataTags/MeasurementTime", "/nirs\d*/metaDataTags/LengthUnit",
                "/nirs\d*/metaDataTags/TimeUnit", "/nirs\d*/metaDataTags/FrequencyUnit",
                "/nirs\d*/data\d*/dataTimeSeries", "/nirs\d*/data\d*/time",
                "/nirs\d*/data\d*/measurementList\d*/sourceIndex", "/nirs\d*/data\d*/measurementList\d*/detectorIndex",
                "/nirs\d*/data\d*/measurementList\d*/wavelengthIndex", "/nirs\d*/data\d*/measurementList\d*/dataType",
                "/nirs\d*/data\d*/measurementList\d*/dataTypeIndex", "/nirs\d*/probe/wavelengths",
                "/nirs\d*/probe/sourcePos2D", "/nirs\d*/probe/detectorPos2D", "/nirs\d*/stim\d*/name",
                "/nirs\d*/stim\d*/data", "/nirs\d*/aux\d*/name", "/nirs\d*/aux\d*/dataTimeSeries",
                "/nirs\d*/aux\d*/time"]
    return Required


def getoptionalfieldsLst():
    Optional = ["/nirs\d*/data\w*/measurementList\d*/wavelengthActual",
                "/nirs\d*/data\w*/measurementList\d*/wavelengthEmissionActual",
                "/nirs\d*/data\d*/measurementList\d*/dataTypeLabel", "/nirs\d*/data\w*/measurementList\d*/sourcePower",
                "/nirs\d*/data\w*/measurementList\d*/detectorGain", "/nirs\d*/data\w*/measurementList\d*/moduleIndex",
                "/nirs\d*/data\w*/measurementList\d*/sourceModuleIndex",
                "/nirs\d*/data\w*/measurementList\d*/detectorModuleIndex", "/nirs\d*/probe/wavelengthsEmission",
                "/nirs\d*/probe/sourcePos3D", "/nirs\d*/probe/detectorPos3D", "/nirs\d*/probe/frequencies",
                "/nirs\d*/probe/timeDelays", "/nirs\d*/probe/timeDelayWidths", "/nirs\d*/probe/momentOrders",
                "/nirs\d*/probe/correlationTimeDelays", "/nirs\d*/probe/correlationTimeDelayWidths",
                "/nirs\d*/probe/sourceLabels", "/nirs\d*/probe/detectorLabels", "/nirs\d*/probe/landmarkPos2D",
                "/nirs\d*/probe/landmarkPos3D", "/nirs\d*/probe/landmarkLabels", "/nirs\d*/probe/useLocalIndex",
                "/nirs\d*/aux\d*/timeOffset", "/nirs\d*/stim\d*/dataLabels"]
    return Optional


def isrequired(fld):
    flag = False
    required = getrequiredfieldsLst()
    for x in required:
        if re.match(x, fld):
            flag = True
    return flag


def isoptional(fld):
    flag = False
    required = getoptionalfieldsLst()
    for x in required:
        if re.match(x, fld):
            flag = True
    if "metaDataTags" in fld:
        flag = True
    return flag


def validate(filename, fileOut=None):
    fileID = h5py.File(filename, 'r')
    formatVersion = hdfgetdata(fileID, "/formatVersion")

    def checkdim(field, fID):
        value = fID.get(field)

        if "Pos2D" in field or "Pos3D" in field:
            dim = 2
        elif "dataTimeSeries" in field:
            if "aux" in field:
                dim = 1
            else:
                dim = 2
        elif "measurementList" in field:
            if "dataTypeLabel" in field:
                dim = 1
            else:
                dim = 0
        elif "stim" in field and "data" in field:
            dim = 2
        else:
            dim = 1
        if dim != len(value.dims):
            return False, dim
        else:
            return True, dim

    def recheckfield(field, fID):
        value = fID.get(field)

        if value.shape == (1,):
            return True
        else:
            return False

    def getallnames(gID, fieldLst, snirfFile, nirsCountFunc, dataCountFunc, stimCountFunc, auxCountFunc,
                    invalidCountFunc, invalidFldFunc, missingFldFunc):
        if isinstance(gID, h5py.Dataset):
            fieldLst.append(gID.name)

            print(Fore.WHITE + gID.name)
            val = fileID.get(gID.name)

            if h5py.check_string_dtype(val.dtype):
                dimcheck, actualDim = checkdim(gID.name, fileID)
                # string
                if val.len() == 1:
                    val = val[0].decode('ascii')
                    print('\tHDF5-STRING: {0}'.format(val))
                else:
                    val2 = []
                    for y in val:
                        val2.append(y.decode('ascii'))
                    val2 = np.array(val2)
                    print('\tHDF5-STRING 1D-Vector: <{0}x1>'.format(len(val2)))
            else:
                dimcheck, actualDim = checkdim(gID.name, fileID)
                val = np.array(val)
                if val.ndim == 1:
                    if len(val) == 1:
                        val = val[0]
                        print('\tHDF5-FLOAT: {0}'.format(val))
                        if not dimcheck:
                            dimcheck = recheckfield(gID.name, fileID)
                    else:
                        print('\tHDF5-FLOAT 1D-Vector: <{0}x1>'.format(len(val)))
                elif val.ndim == 0:
                    print('\tHDF5-Integer 0D-Scalar <0x0>')
                else:
                    print('\tHDF5-FLOAT 2D-Array: <{0}x{1}>'.format(len(val), int(val.size / len(val))))

            if not dimcheck:
                print(Fore.RED + '\tINVALID dimensions(Expected Number of Dimensions: ' + str(actualDim) + ')')
                invalidCountFunc += 1
                invalidFldFunc.append(gID.name)

            if "/aux" in gID.name or "/stim" in gID.name:
                if isrequired(gID.name):
                    print(Fore.BLUE + '\t\tRequired field when optional parent object is included')
                elif isoptional(gID.name):
                    print(Fore.GREEN + '\t\tOptional field when optional parent object is included')
                else:
                    print(Fore.RED + '\t\tINVALID field')
                    invalidCountFunc = invalidCountFunc + 1
                    invalidFldFunc.append(gID.name)
            else:
                if isrequired(gID.name):
                    print(Fore.BLUE + '\t\tRequired field')
                elif isoptional(gID.name):
                    if 'metaDataTags' in gID.name:
                        print(Fore.GREEN + '\t\tUser defined Optional metaDataTags field')
                    else:
                        print(Fore.GREEN + '\t\tOptional field')
                else:
                    print(Fore.RED + '\t\tINVALID field')
                    invalidCountFunc = invalidCountFunc + 1
                    invalidFldFunc.append(gID.name)
        else:
            for X in gID:
                if not isinstance(gID[X], h5py.Dataset):
                    if 'nirs' in X:
                        if len(snirfFile.nirs) == 0:
                            snirfFile.nirs.append(read_nirs(gID[X]))
                            nirsCountFunc += 1
                            if snirfFile.nirs[nirsCountFunc].validFlag == 1:
                                print(Fore.BLUE + gID[X].name + ' is a valid group field')
                            else:
                                print(Fore.RED + gID[X].name + ' is an INVALID group field')
                                print(Fore.RED + gID[X].name + ' is missing:')
                                for i in range(len(snirfFile.nirs[nirsCountFunc].missField)):
                                    print(Fore.RED + '\t' + snirfFile.nirs[nirsCountFunc].missField[i])
                                    invalidCountFunc += 1
                                    missingFldFunc.append(gID[X].name + snirfFile.nirs[nirsCountFunc].
                                                          missField[i])
                        else:
                            snirfFile.nirs.append(read_nirs(gID[X]))
                            nirsCountFunc += 1
                            if snirfFile.nirs[nirsCountFunc].validFlag == 1:
                                print(Fore.BLUE + gID[X].name + ' is a valid group field')
                            else:
                                print(Fore.RED + gID[X].name + ' is an INVALID group field')
                                print(Fore.RED + gID[X].name + ' is missing:')
                                for i in range(len(snirfFile.nirs[nirsCountFunc].missField)):
                                    print(Fore.RED + '\t' + snirfFile.nirs[nirsCountFunc].missField[i])
                                    invalidCountFunc += 1
                                    missingFldFunc.append(gID[X].name + snirfFile.nirs[nirsCountFunc].
                                                          missField[i])
                    elif 'metaDataTags' in X:
                        # snirfFile.nirs[nirsCountFunc].metaDataTags = read_meta(gID[X])
                        if snirfFile.nirs[nirsCountFunc].metaDataTags.validFlag == 1:
                            print(Fore.BLUE + gID[X].name + ' is a valid group field')
                        else:
                            print(Fore.RED + gID[X].name + ' is an INVALID group field')
                            print(Fore.RED + gID[X].name + ' is missing:')
                            for i in range(len(snirfFile.nirs[nirsCountFunc].metaDataTags.missField)):
                                print(Fore.RED + '\t' + snirfFile.nirs[nirsCountFunc].metaDataTags.missField[i])
                                invalidCountFunc += 1
                                missingFldFunc.append(gID[X].name + snirfFile.nirs[nirsCountFunc].
                                                      metaDataTags.missField[i])
                    elif 'data' in X:
                        # snirfFile.nirs[nirsCountFunc].data.append(read_data(gID[X]))
                        dataCountFunc += 1
                        if snirfFile.nirs[nirsCountFunc].data[dataCountFunc].validFlag == 1:
                            print(Fore.BLUE + gID[X].name + ' is a valid group field')
                        else:
                            print(Fore.RED + gID[X].name + ' is an INVALID group field')
                            print(Fore.RED + gID[X].name + ' is missing:')
                            for i in range(len(snirfFile.nirs[nirsCountFunc].data[dataCountFunc].missField)):
                                print(Fore.RED + '\t' + snirfFile.nirs[nirsCountFunc].data[dataCountFunc].missField[i])
                                invalidCountFunc += 1
                                missingFldFunc.append(gID[X].name + snirfFile.nirs[nirsCountFunc].
                                                      data[dataCountFunc].missField[i])
                    elif 'stim' in X:
                        # snirfFile.nirs[nirsCountFunc].stim.append(read_stim(gID[X]))
                        stimCountFunc += 1
                        if snirfFile.nirs[nirsCountFunc].stim[stimCountFunc].validFlag == 1:
                            print(Fore.BLUE + gID[X].name + ' is a valid group field')
                        else:
                            print(Fore.RED + gID[X].name + ' is an INVALID group field')
                            print(Fore.RED + gID[X].name + ' is missing:')
                            for i in range(len(snirfFile.nirs[nirsCountFunc].stim[stimCountFunc].missField)):
                                print(Fore.RED + '\t' + snirfFile.nirs[nirsCountFunc].stim[stimCountFunc].missField[i])
                                invalidCountFunc += 1
                                missingFldFunc.append(gID[X].name + snirfFile.nirs[nirsCountFunc].
                                                      stim[stimCountFunc].missField[i])
                    elif 'probe' in X:
                        # snirfFile.nirs[nirsCountFunc].probe = read_probe(gID[X])
                        if snirfFile.nirs[nirsCountFunc].probe.validFlag == 1:
                            print(Fore.BLUE + gID[X].name + ' is a valid group field')
                        else:
                            print(Fore.RED + gID[X].name + ' is an INVALID group field')
                            print(Fore.RED + gID[X].name + ' is missing:')
                            for i in range(len(snirfFile.nirs[nirsCountFunc].probe.missField)):
                                print(Fore.RED + '\t' + snirfFile.nirs[nirsCountFunc].probe.missField[i])
                                invalidCountFunc += 1
                                missingFldFunc.append(gID[X].name + snirfFile.nirs[nirsCountFunc].probe.missField[i])
                    elif 'aux' in X:
                        # snirfFile.nirs[nirsCountFunc].aux.append(read_aux(gID[X]))
                        auxCountFunc += 1
                        if snirfFile.nirs[nirsCountFunc].aux[auxCountFunc].validFlag == 1:
                            print(Fore.BLUE + gID[X].name + ' is a valid group field')
                        else:
                            print(Fore.RED + gID[X].name + ' is an INVALID group field')
                            print(Fore.RED + gID[X].name + ' is missing:')
                            for i in range(len(snirfFile.nirs[nirsCountFunc].aux[auxCountFunc].missField)):
                                print(Fore.RED + '\t' + snirfFile.nirs[nirsCountFunc].aux[auxCountFunc].missField[i])
                                invalidCountFunc += 1
                                missingFldFunc.append(gID[X].name + snirfFile.nirs[nirsCountFunc].
                                                      aux[auxCountFunc].missField[i])

                invalidCountFunc, invalidFldFunc, missingFldFunc = getallnames(
                    gID[X], fieldLst, snirfFile, nirsCountFunc, dataCountFunc, stimCountFunc, auxCountFunc,
                    invalidCountFunc, invalidFldFunc, missingFldFunc)

        return invalidCountFunc, invalidFldFunc, missingFldFunc

    lst = []
    snirfData = snirf
    snirfData.filename = fileID.filename
    snirfData.formatVersion = formatVersion
    nirsCount = -1
    dataCount = -1
    stimCount = -1
    auxCount = -1
    invalidCount = 0
    invalidFld = []
    missingFld = []

    if fileOut is None:
        print('-' * 40)
        print('SNIRF Validator')
        print('Version 2.0')
        print('written by T. Huppert')
        print('Updated by Team Lemon')
        print()
        print('File = {0}'.format(filename))
        print('Version = {0}'.format(formatVersion))
        print('-' * 40)

        invalidCount, invalidFld, missingFld = getallnames(fileID, lst, snirfData, nirsCount, dataCount,
                                                           stimCount, auxCount, invalidCount, invalidFld, missingFld)

        print('-' * 40)
        if invalidCount != 0:
            print(Fore.RED + "File is INVALID")
            print(Fore.RED + '\tINVALID FIELD(S) FOUND')
            if len(invalidFld) == 0:
                print(Fore.WHITE + 'NONE')
            else:
                for x in invalidFld:
                    print(Fore.RED + x)
            print(Fore.RED + '\tMISSING FIELD(S) FOUND')
            if len(missingFld) == 0:
                print(Fore.WHITE + 'NONE')
            else:
                for x in missingFld:
                    print(Fore.RED + x)
        else:
            print(Fore.WHITE + "File is VALID")
        print(Style.RESET_ALL)


def main():
    filename = sys.argv[1]
    print(filename)
    if len(sys.argv) > 2:
        fileOut = sys.argv[2]
    else:
        fileOut = None
    validate(filename, fileOut)


if __name__ == "__main__":
    main()
