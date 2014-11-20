'''
Created on Nov 19, 2014

@author: rhf
'''
import unittest

from helper.params import Params
from develop.helper.oldmodel import OldModel
from develop.helper.newmodel import NewModel
from helper.data import Data
import numpy as np

class Test(unittest.TestCase):

    models = None
    p = None
    
    def setUp(self):
        self.p = Params()
        self.models = self.p.getAllOldAndNewModelsNames()

    def tearDown(self):
        pass


    def testModelsStandardParams1D(self):
        for oldModelName,newModelName in self.models:
            print "* Evaluating both Models:",oldModelName, "::", newModelName
            oldModelHelper = OldModelHelper(oldModelName)
            newModelHelper = NewModelHelper(newModelName)
            oldModelHelper.setModel()
            newModelHelper.setModel()
            vOld = oldModelHelper.eval1d()
            vNew = newModelHelper.eval1d()
            err = self._relativeError(vOld, vNew)
            errMax = newModelHelper.getRelativeError1D()
            self.assertLess(err, errMax)#, "For models: " + oldModelName + " :: "+ newModelName)
    
    def testModelsStandardParams2D(self):
        for oldModelName,newModelName in self.models:
            print "* Evaluating both Models:",oldModelName, "::", newModelName
            oldModelHelper = OldModelHelper(oldModelName)
            newModelHelper = NewModelHelper(newModelName)
            oldModelHelper.setModel()
            newModelHelper.setModel()
            vOld,mask = oldModelHelper.eval2d()
            vNew,mask = newModelHelper.eval2d()
            err = self._relativeError(vOld, vNew,mask)
            errMax = newModelHelper.getRelativeError2D()
            self.assertLess(err, errMax)#, "For models: " + oldModelName + " :: "+ newModelName)

        
    def _relativeError(self, value, approx, mask=None ):
        if mask is None:
            return np.max(np.abs((value-approx)/ value))
        else:
            return np.max(np.abs((value-approx)[mask]/ value[mask]))
            
            
    


class NewModelHelper():
    def __init__(self,modelName,params=None):
        self.modelName = modelName
        self.p = params if params is not None else Params()
        self.data = None
        self.modelNIterations = self.p.getNewModelUniqueCollumValue(modelName,"n_sasview")
        self.modelCutOff = self.p.getNewModelUniqueCollumValue(modelName,"cutoff")
        
    def setModel(self,modelParams=None):
        if modelParams is None:
            modelParams = self.p.getNewModelParamNamesAndValues(self.modelName)
            
        modelDType = self.p.getNewModelUniqueCollumValue(self.modelName,"dtype")
        self.model = NewModel(self.modelName,dtype=modelDType,**modelParams)        
    
    def _setData(self):
        modelQMax = self.p.getNewModelUniqueCollumValue(self.modelName,"qmax")
        self.data = Data(modelQMax)
    
    def eval1d(self):
        if self.data is None:
            self._setData()
        ret1D = self.model.eval(self.data.get1DBumps(), cutoff=self.modelCutOff, nIterations=self.modelNIterations)
        return ret1D
    
    def eval2d(self):
        if self.data is None:
            self._setData()
        ret2D = self.model.eval(self.data.get2DBumps(), cutoff=self.modelCutOff, nIterations=self.modelNIterations)
        return ret2D, self.data.get2DMask()

    def getRelativeError1D(self):
        return self.p.getNewModelUniqueCollumValue(self.modelName,"rel_error_1d")
    def getRelativeError2D(self):
        return self.p.getNewModelUniqueCollumValue(self.modelName,"rel_error_2d")
    
class OldModelHelper():
    def __init__(self,modelName,params=None):
        self.modelName = modelName
        self.p = params if params is not None else Params()
        self.data = None
        self.modelNIterations = self.p.getOldModelUniqueCollumValue(modelName,"n_sasview")
        
    def setModel(self,modelParams=None):
        if modelParams is None:
            modelParams = self.p.getOldModelParamNamesAndValues(self.modelName)
        self.model =  OldModel(self.modelName,**modelParams)    
    
    def _setData(self):
        modelQMax = self.p.getOldModelUniqueCollumValue(self.modelName,"qmax")
        self.data = Data(modelQMax)
    
    def eval1d(self):
        if self.data is None:
            self._setData()
        ret1D = self.model.eval(self.data.get1DSasView(),nIterations=self.modelNIterations)
        return ret1D
    
    def eval2d(self):
        if self.data is None:
            self._setData()
        ret2D = self.model.eval(self.data.get2DSasView(),nIterations=self.modelNIterations)
        return ret2D, self.data.get2DMask()




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
