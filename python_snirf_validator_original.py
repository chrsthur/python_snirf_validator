#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 3 13:28 2020
Updated on Tue Sep 7 13:59 2021

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


class data:
    dataTimeSeries = None
    time = None
    measurementList = measurementList()


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


class aux:
    name = None
    dataTimeSeries = None
    time = None
    timeOffSet = None


class stim:
    name = None
    data = None
    dataLabels = None


class metaDataTags:
    SubjectID = None
    MeasurementDate = None
    MeasurementTime = None
    LengthUnit = None
    TimeUnit = None
    FrequencyUnit = None


class snirf:
    filename = None
    formatVersion = None
    data = None
    stim = None
    probe = probe()
    aux = None
    metaDataTags = metaDataTags()


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

    return m


def read_data(gID):
    d = data

    d.dataTimeSeries = hdfgetdata(gID, 'dataTimeSeries')
    d.time = hdfgetdata(gID, 'time')
    for fld in gID:
        if 'measurementList' in fld:
            d.measurementList = read_measurementList(gID[fld])

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

    return p


def read_aux(gID):
    a = aux
    a.name = hdfgetdata(gID, 'name')
    a.dataTimeSeries = hdfgetdata(gID, 'dataTimeSeries')
    a.time = hdfgetdata(gID, 'time')
    a.timeOffSet = hdfgetdata(gID, 'timeOffSet')

    return a


def read_stim(gID):
    s = stim
    s.name = hdfgetdata(gID, 'name')
    s.data = hdfgetdata(gID, 'data')
    s.dataLabels = hdfgetdata(gID, 'dataLabels')
    return s


def read_meta(gID):
    md = metaDataTags
    md.SubjectID = hdfgetdata(gID, 'SubjectID')
    md.MeasurementDate = hdfgetdata(gID, 'MeasurementDate')
    md.MeasurementTime = hdfgetdata(gID, 'MeasurementTime')
    md.LengthUnit = hdfgetdata(gID, 'LengthUnit')
    md.TimeUnit = hdfgetdata(gID, 'TimeUnit')
    md.FrequencyUnit = hdfgetdata(gID, 'FrequencyUnit')
    return md


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

    def getallnames(gID, fieldLst):
        if isinstance(gID, h5py.Dataset):
            fieldLst.append(gID.name)
        else:
            for X in gID:
                getallnames(gID[X], fieldLst)

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

    lst = []

    getallnames(fileID, lst)

    if fileOut is None:
        print('-' * 40)
        print('SNIRF Validator')
        print('Version 1.0')
        print('written by T. Huppert')
        print()
        print('File = {0}'.format(filename))
        print('Version = {0}'.format(formatVersion))
        print('-' * 40)

        foundInvalid = 0

        lstInvalid = []

        for x in lst:
            print(Fore.WHITE + x)
            val = fileID.get(x)
            if h5py.check_string_dtype(val.dtype):
                dimcheck, actualDim = checkdim(x, fileID)
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
                dimcheck, actualDim = checkdim(x, fileID)
                val = np.array(val)
                if val.ndim == 1:
                    if len(val) == 1:
                        val = val[0]
                        print('\tHDF5-FLOAT: {0}'.format(val))
                        if not dimcheck:
                            dimcheck = recheckfield(x, fileID)
                    else:
                        print('\tHDF5-FLOAT 1D-Vector: <{0}x1>'.format(len(val)))
                elif val.ndim == 0:
                    print('\tHDF5-Integer 0D-Scalar <0x0>')
                else:
                    print('\tHDF5-FLOAT 2D-Array: <{0}x{1}>'.format(len(val), int(val.size / len(val))))

            if not dimcheck:
                print(Fore.RED + '\tINVALID dimensions(Expected Number of Dimensions: ' + str(actualDim) + ')')
                foundInvalid = foundInvalid + 1
                lstInvalid.append(x)
            if "/aux" in x or "/stim" in x:
                if isrequired(x):
                    print(Fore.BLUE + '\t\tRequired field when optional parent object is included')
                elif isoptional(x):
                    print(Fore.GREEN + '\t\tOptional field when optional parent object is included')
                else:
                    print(Fore.RED + '\t\tINVALID field')
                    foundInvalid = foundInvalid + 1
                    lstInvalid.append(x)
            else:
                if isrequired(x):
                    print(Fore.BLUE + '\t\tRequired field')
                elif isoptional(x):
                    if 'metaDataTags' in x:
                        print(Fore.GREEN + '\t\tUser defined Optional metaDataTags field')
                    else:
                        print(Fore.GREEN + '\t\tOptional field')
                else:
                    print(Fore.RED + '\t\tINVALID field')
                    foundInvalid = foundInvalid + 1
                    lstInvalid.append(x)

        print('-' * 40)
        if len(lstInvalid) != 0:
            print(Fore.RED + "File is INVALID")
            print(Fore.RED + '\tINVALID ENTRIES FOUND')
            for x in lstInvalid:
                print(Fore.RED + x)
        else:
            print(Fore.WHITE + "File is VALID")
        print(Style.RESET_ALL)
    else:  # write to file
        text_file = open(fileOut, "w")
        text_file.write('\n' + '\n' + '-' * 40)
        text_file.write('\n' + '\n' + 'SNIRF Validator')
        text_file.write('\n' + '\n' + 'Version 1.0')
        text_file.write('\n' + 'written by T. Huppert')
        text_file.write('\n')
        text_file.write('\n' + 'File = {0}'.format(filename))
        text_file.write('\n' + 'Version = {0}'.format(formatVersion))
        text_file.write('\n' + '-' * 40)

        foundInvalid = 0

        lstInvalid = []

        for x in lst:
            text_file.write('\n' + x)
            val = fileID.get(x)
            if h5py.check_string_dtype(val.dtype):
                # string
                if val.len() == 1:
                    val = val[0].tobytes().decode('ascii')
                    text_file.write('\n' + '\tHDF5-STRING: {0}'.format(val))
                else:
                    val2 = []
                    for y in val:
                        val2.append(y.tobytes().decode('ascii'))
                    val2 = np.array(val2)
                    text_file.write('\n' + '\tHDF5-STRING 1D-Vector: <{0}x1>'.format(len(val2)))
            else:
                val = np.array(val)
                if val.ndim == 1 and len(val) == 1:
                    val = val[0]
                    text_file.write('\n' + '\tHDF5-FLOAT: {0}'.format(val))
                elif val.ndim == 1:
                    text_file.write('\n' + '\tHDF5-FLOAT 1D-Vector: <{0}x1>'.format(len(val)))
                else:
                    text_file.write(
                        '\n' + '\tHDF5-FLOAT 2D-Array: <{0}x{1}>'.format(len(val), int(val.size / len(val))))

            dimcheck, actualDim = checkdim(x, fileID)
            if not dimcheck:
                print(Fore.RED + '\tINVALID dimensions(Expected Number of Dimensions: ' + str(actualDim) + ')')
                foundInvalid = foundInvalid + 1
                lstInvalid.append(x)

            if isrequired(x):
                text_file.write('\n' + '\t\tRequired field')
            elif isoptional(x):
                text_file.write('\n' + '\t\tOptional field')
            else:
                text_file.write('\n' + '\t\tINVALID field')
                foundInvalid = foundInvalid + 1
                lstInvalid.append(x)

        text_file.write('\n' + '-' * 40)
        if len(lstInvalid) != 0:
            text_file.write('\n' + "File is INVALID")
            text_file.write('\n' + '\tINVALID ENTRIES FOUND')
            for x in lstInvalid:
                text_file.write('\n' + x)
        else:
            text_file.write('\n' + "File is VALID")
        text_file.close()
    return foundInvalid == 0


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
