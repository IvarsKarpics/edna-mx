#
#    Project: EDNA MXv1
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) 2008-2009 European Synchrotron Radiation Facility
#                            Grenoble, France
#
#    Principal authors:      Karl Levik (karl.levik@diamond.ac.uk)
#                            Olof Svensson (svensson@esrf.fr) 
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


__authors__ = [ "Olof Svensson", "Karl Levik" ]
__contact__ = "svensson@esrf.fr"
__license__ = "GPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"

import os

from EDAssert                            import EDAssert
from EDTestCase                          import EDTestCase
from EDUtilsTest                         import EDUtilsTest
from EDUtilsPath                         import EDUtilsPath
from EDFactoryPluginStatic import EDFactoryPluginStatic


class EDTestCaseEDHandlerISPyBv1_1(EDTestCase):


    def __init__(self, _pyStrTestName=None):
        EDTestCase.__init__(self, _pyStrTestName)
        strMXv1DataHome = EDUtilsTest.getPluginTestDataDirectory(self.getClassName())
        strDataDir = "EDHandlerISPyBv1_1"
        self.strDataPath = os.path.join(strMXv1DataHome, strDataDir)


    def testGenerateXSDataInputISPyB(self):
        """
        This method is testing the generation of the XSDataInputISPyB object given a XSDataIndexingInput object.
        """
        strReferenceInputControlISPyBFile = EDUtilsPath.mergePath(self.strDataPath, "XSDataInputControlISPyB_reference.xml")
        strPath = os.path.join(self.strDataPath, strReferenceInputControlISPyBFile)
        strXMLIndexingInput = self.readAndParseFile(strPath)
        from XSDataMXv1 import XSDataInputControlISPyB
        xsDataInputControlISPyB = XSDataInputControlISPyB.parseString(strXMLIndexingInput)
        from EDHandlerXSDataISPyBv1_1 import EDHandlerXSDataISPyBv1_1
        xsDataInputISPyB = EDHandlerXSDataISPyBv1_1.generateXSDataInputISPyB(xsDataInputControlISPyB)
        strReferenceInputISPyBFile = EDUtilsPath.mergePath(self.strDataPath, "XSDataInputISPyB_reference.xml")
        strReferencePath = os.path.join(self.strDataPath, strReferenceInputISPyBFile)
        strXMLInputISPyBReference = self.readAndParseFile(strReferencePath)
        EDFactoryPluginStatic.loadModule("XSDataISPyBv1_1")
        from XSDataISPyBv1_1 import XSDataInputISPyB
        xsDataInputISPyBReference = XSDataInputISPyB.parseString(strXMLInputISPyBReference)
        # Remove the time strings since they otherwise make the test fail
        xsDataInputISPyBReference.getScreening().setTimeStamp(None)
        xsDataInputISPyB.getScreening().setTimeStamp(None)
        EDAssert.equal(xsDataInputISPyBReference.marshal(), xsDataInputISPyB.marshal())



    def process(self):
        self.addTestMethod(self.testGenerateXSDataInputISPyB)



if __name__ == '__main__':

    edTestCaseEDHandlerISPyBv1_1 = EDTestCaseEDHandlerISPyBv1_1("EDTestCaseEDHandlerISPyBv1_1")
    edTestCaseEDHandlerISPyBv1_1.execute()

