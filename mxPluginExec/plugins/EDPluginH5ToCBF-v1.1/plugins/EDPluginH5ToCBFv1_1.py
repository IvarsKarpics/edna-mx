# coding: utf8
#
#    Project: MX Plugin Exec
#             http://www.edna-site.org
#
#    Copyright (C) ESRF
#
#    Principal author:       Olof Svensson
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Olof Svensson"
__license__ = "GPLv3+"
__copyright__ = "ESRF"

import os
import time
import shutil

from EDPluginExecProcessScript import EDPluginExecProcessScript
from EDUtilsImage import EDUtilsImage

from XSDataCommon import XSDataString
from XSDataCommon import XSDataFile

from XSDataH5ToCBFv1_1 import XSDataInputH5ToCBF
from XSDataH5ToCBFv1_1 import XSDataResultH5ToCBF

class EDPluginH5ToCBFv1_1(EDPluginExecProcessScript):
    """
    This plugin runs H5ToXDS to create CBF files from an Eiger HDF5 file. 
    """


    def __init__(self):
        EDPluginExecProcessScript.__init__(self)
        self.setXSDataInputClass(XSDataInputH5ToCBF)
        self.setDataOutput(XSDataResultH5ToCBF())
        self.CBFFile = None
        self.tmpCBFFile = None


    def checkParameters(self):
        """
        Checks the mandatory parameters.
        """
        self.DEBUG("EDPluginH5ToCBFv1_1.checkParameters")
        self.checkMandatoryParameters(self.dataInput, "Data Input is None")
        self.checkMandatoryParameters(self.dataInput.hdf5File, "HDF5 file is None")


    def preProcess(self, _edObject=None):
        EDPluginExecProcessScript.preProcess(self)
        self.DEBUG("EDPluginH5ToCBFv1_1.preProcess")
        xsDataInputH5ToCBF = self.getDataInput()
        self.setScriptCommandline(self.generateCommands(xsDataInputH5ToCBF))



    def process(self, _edObject=None):
        EDPluginExecProcessScript.process(self)
        self.DEBUG("EDPluginH5ToCBFv1_1.process")

    def postProcess(self, _edObject=None):
        EDPluginExecProcessScript.postProcess(self)
        self.DEBUG("EDPluginH5ToCBFv1_1.postProcess")



    def finallyProcess(self, _edObject=None):
        EDPluginExecProcessScript.finallyProcess(self)
        self.DEBUG("EDPluginH5ToCBFv1_1.finallyProcess")
        if self.tmpCBFFile is not None:
            if os.path.exists(self.tmpCBFFile):
                os.remove(self.tmpCBFFile)
        if self.CBFFile is not None:
            if os.path.exists(self.CBFFile):
                self.dataOutput.outputCBFFile = XSDataFile(XSDataString(self.CBFFile))


    def generateCommands(self, _xsDataInputH5ToCBF):
        """
        This method creates a list of commands for H5ToXDS
        """
        self.DEBUG("EDPluginH5ToCBFv1_1.generateCommands")

        hdf5File = _xsDataInputH5ToCBF.hdf5File.path.value
        directory = os.path.dirname(hdf5File)
        prefix = EDUtilsImage.getPrefix(hdf5File)

        imageNumber = _xsDataInputH5ToCBF.imageNumber.value

        if _xsDataInputH5ToCBF.hdf5ImageNumber is None:
            hdf5ImageNumber = imageNumber
        else:
            hdf5ImageNumber = _xsDataInputH5ToCBF.hdf5ImageNumber.value

        if "master" in hdf5File:
            masterFile = hdf5File
        else:
            masterFile = os.path.join(directory, prefix + "_{0}_master.h5".format(hdf5ImageNumber))

        CBFFileName = prefix + "_%04d" % imageNumber + ".cbf"
        tmpCBFFileName = "tmp_" + CBFFileName

        if _xsDataInputH5ToCBF.forcedOutputDirectory is None:
            self.CBFFile = os.path.join(directory, CBFFileName)
        else:
            forcedOutputDirectory = self.dataInput.forcedOutputDirectory.path.value
            if not os.path.exists(forcedOutputDirectory):
                os.makedirs(forcedOutputDirectory, 0755)
            self.CBFFile = os.path.join(forcedOutputDirectory, CBFFileName)

        self.tmpCBFFile = os.path.join(self.getWorkingDirectory(), tmpCBFFileName)

        scriptCommandLine = "{0} {1} {2}".format(masterFile, imageNumber - hdf5ImageNumber + 1, tmpCBFFileName)

        return scriptCommandLine
