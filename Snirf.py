import h5py as h5py
import numpy as np
import re
from colorama import Fore, Style
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class SnirfClass:

    class NirsClass:
        class AuxClass:
            def Print(self):
                printDataset(self)

        class ProbeClass:
            def Print(self):
                printDataset(self)

        class StimClass:
            def Print(self):
                printDataset(self)

        class DataClass:

            class MeasurementListClass:
                def __init__(self):
                    return

                def __str__(self):
                    return printDatast(oneClass=self)

            def Print(self):
                for attribute in self.__dict__.keys():
                    if attribute[:2] != '__' and 'addGroup' not in attribute and 'Print' not in attribute:
                        value = getattr(self, attribute)
                        if not callable(value):
                            print(attribute, '=', value)
                        else:
                            print('\t' + attribute + ':')
                            value.Print(self=value)

        class MetaDataTagsClass:
            def Print(self):
                printDataset(self)

        def __init__(self):
            return

        def addGroup(self, groupName):
            if "aux" in groupName:
                setattr(self, groupName, AuxClass)
            elif "probe" in groupName:
                setattr(self, groupName, ProbeClass)
            elif "stim" in groupName:
                setattr(self, groupName, StimClass)
            elif "data" in groupName:
                setattr(self, groupName, DataClass)
            elif "metaDataTags" in groupName:
                setattr(self, groupName, MetaDataTagsClass)
            elif "measurementList" in groupName:
                setattr(self, groupName, MeasurementListClass)
            else:
                return

        def Print(self):
            for attribute in self.__dict__.keys():
                if attribute[:2] != '__' and 'addGroup' not in attribute and 'Print' not in attribute:
                    value = getattr(self, attribute)
                    if not callable(value):
                        print(attribute, '=', value)
                    else:
                        print(attribute + ':')
                        value.Print(self=value)

    def addGroup(self, groupName):
        setattr(self, groupName, NirsClass)


def printDataset(oneClass):
    for attribute in oneClass.__dict__.keys():
        if attribute[:2] != '__':
            value = getattr(oneClass, attribute)
            if not callable(value):
                print('\t' + attribute, '=', value)
            else:
                print(attribute + ':')
                value.Print(self=value)

def buildSnirfClass(filePath):

    def getData(gID):
        # check actual data type and dimension, and print accordingly
        if h5py.check_string_dtype(gID.dtype):  # string
            actualDim = gID.ndim
            if gID.len() == 1:
                data = gID[0].decode('ascii')
                msg = Fore.CYAN + '\t\tHDF5-STRING'
            else:
                data = []
                for y in gID:
                    data.append(y.decode('ascii'))
                data = np.array(data)
                msg = Fore.CYAN + '\t\tHDF5-STRING 1D-Array'
        else:
            data = gID[()]
            if gID.ndim == 2:
                msg = Fore.CYAN + '\t\tHDF5-FLOAT 2D-Array'
                actualDim = gID.ndim
            elif gID.ndim == 1:  # always a float
                dimension = gID.shape
                if dimension[0] == 1:
                    msg = Fore.CYAN + '\t\tHDF5-FLOAT 1D-Array'
                    actualDim = 0
                else:
                    msg = Fore.CYAN + '\t\tHDF5-FLOAT Point'
                    actualDim = gID.ndim
            elif gID.ndim == 0:
                msg = Fore.CYAN + '\t\tHDF5-Integer'
                actualDim = gID.ndim
            else:
                return
        return actualDim, data, msg

    def buildDataset(oneClass, oneGroup):
        if isinstance(oneGroup, h5py.Group):
            for xx in oneGroup.keys():
                oneDataset = oneGroup[xx]
                if isinstance(oneDataset, h5py.Dataset):
                    [actualDim, data, msg] = getData(oneDataset)
                    setattr(oneClass, xx, data)
                else:
                    setattr(oneClass, xx, measurementListClass)
                    newClass = getattr(oneClass, xx)
                    buildDataset(newClass, oneDataset)
        return oneClass

    if ".snirf" in filePath:
        fileID = h5py.File(filePath, 'r')
    else:
        print(Fore.RED + "Invalid filepath!")

    # generate snirf class
    oneSnirf = SnirfClass
    for ii in fileID.keys():
        oneName = fileID[ii]
        if isinstance(oneName, h5py.Group):
            for jj in oneName.keys():  # /nirs
                oneSnirf.addGroup(self=oneSnirf, groupName=ii)
                oneNirs = getattr(oneSnirf, ii)
                oneNirs.addGroup(self=oneNirs, groupName=jj)
                buildDataset(getattr(oneNirs, jj), oneName[jj])
        else:
            if h5py.check_string_dtype(oneName.dtype):
                setattr(oneSnirf, ii, oneName[0].decode('ascii'))
    return oneSnirf

def saveSnirfClass(snirfObject, fName):

    def writeGroup(f, groupObj, attribute):
        grp = f.create_group(attribute)

        for field in groupObj.__dict__.keys():
            if field[:2] != '__' and 'addGroup' not in field and 'Print' not in field:
                if isinstance(getattr(groupObj, field), type):
                    writeGroup(grp, eval('groupObj.' + field), field)
                else:
                    if isinstance(getattr(groupObj, field), str):
                        grp.create_dataset(field, data=[eval('groupObj.' + field + ".encode('UTF-8')")])
                    elif isinstance(getattr(groupObj, field), np.ndarray):
                        if isinstance(getattr(groupObj, field)[0], str):
                            grpField = eval('groupObj.' + field)
                            strArray = [grpField[i].encode('UTF-8') for i in range(grpField.size)]
                            grp.create_dataset(field, data=strArray)
                        else:
                            grp.create_dataset(field, data=eval('groupObj.' + field))
                    else:
                        grp.create_dataset(field, data=eval('groupObj.' + field))
        return f

    fname = fName.replace(".snirf", "") + "_validated.snirf"

    with h5py.File(fname, 'w') as f:
        for attribute in snirfObject.__dict__.keys():
            if attribute[:2] != '__' and 'addGroup' not in attribute and 'Print' not in attribute:
                if isinstance(getattr(snirfObject, attribute), type):
                    f = writeGroup(f, eval('oneSnirf.' + attribute), attribute)
                else:
                    f.create_dataset(attribute, data=[eval('oneSnirf.' + attribute)])
