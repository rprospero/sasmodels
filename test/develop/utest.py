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
import pprint as pp

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
            print "* testModelsStandardParams1D:",oldModelName, "::", newModelName
            oldModelHelper = OldModelHelper(oldModelName)
            newModelHelper = NewModelHelper(newModelName)
            oldModelHelper.setModel()
            newModelHelper.setModel()
            vOld = oldModelHelper.eval1d()
            vNew = newModelHelper.eval1d()
            err = self._relativeError(vOld, vNew)
            errMax = newModelHelper.getRelativeError1D()
            self.assertLess(err, errMax)#, "For models: " + oldModelName + " :: "+ newModelName)
    
    def testModelsRandomParams1D(self):
        for oldModelName,newModelName in self.models:
            print "* testModelsRandomParams1D:",oldModelName, "::", newModelName
            
            p = Params()
            oldModelParams,newModelParams = p.getModelsParamNamesAndValuesRandom(oldModelName, newModelName) 
    
            oldModelHelper = OldModelHelper(oldModelName)
            newModelHelper = NewModelHelper(newModelName)
            oldModelHelper.setModel(oldModelParams)
            newModelHelper.setModel(newModelParams)
            vOld = oldModelHelper.eval1d()
            vNew = newModelHelper.eval1d()
            err = self._relativeError(vOld, vNew)
            errMax = newModelHelper.getRelativeError1D()
            self.assertLess(err, errMax, "For models: " + oldModelName + " :: "+ newModelName + 
                            " :: ERROR: Obtained: %.2e, Max: %.2e, Absolute: %.2e"%(err, errMax,self._absoluteError(vOld, vNew))+
                            "\n" + "1D Old: " + pp.pformat(oldModelParams) + "\n1D New: " + pp.pformat(newModelParams) +
                            "1D VOld: " + pp.pformat(vOld)+
                            "1D VNew: " + pp.pformat(vNew))
            
    def testModelsStandardParams2D(self):
        for oldModelName,newModelName in self.models:
            print "* testModelsStandardParams2D:",oldModelName, "::", newModelName
            oldModelHelper = OldModelHelper(oldModelName)
            newModelHelper = NewModelHelper(newModelName)
            oldModelHelper.setModel()
            newModelHelper.setModel()
            vOld, mask = oldModelHelper.eval2d()
            vNew, mask = newModelHelper.eval2d()
            err = self._relativeError(vOld, vNew,mask)
            errMax = newModelHelper.getRelativeError2D()
            self.assertLess(err, errMax)#, "For models: " + oldModelName + " :: "+ newModelName)

    def testModelsRandomParams2D(self):
        for oldModelName,newModelName in self.models:
            print "* testModelsRandomParams2D:",oldModelName, "::", newModelName
            
            p = Params()
            oldModelParams,newModelParams = p.getModelsParamNamesAndValuesRandom(oldModelName, newModelName) 
    
            oldModelHelper = OldModelHelper(oldModelName)
            newModelHelper = NewModelHelper(newModelName)
            oldModelHelper.setModel(oldModelParams)
            newModelHelper.setModel(newModelParams)
            vOld, mask = oldModelHelper.eval2d()
            vNew, mask = newModelHelper.eval2d()
            err = self._relativeError(vOld, vNew,mask)
            errMax = newModelHelper.getRelativeError2D()
            self.assertLess(err, errMax, "For models: " + oldModelName + " :: "+ newModelName + 
                            " :: ERROR: Obtained: %.2e, Max: %.2e, Absolute: %.2e"%(err, errMax,self._absoluteError(vOld, vNew,mask))+
                            "\n2D Old: " + pp.pformat(oldModelParams) + "\n2D New: " + pp.pformat(newModelParams) +
                            "\n2D VOld: " + pp.pformat(vOld)+
                            "\n2D VNew: " + pp.pformat(vNew))


    

        
    def _relativeError(self, value, approx, mask=None ):
        if mask is None:
            return np.max(np.abs((value-approx)/ value))
        else:
            return np.max(np.abs((value-approx)[mask]/ value[mask]))
            
    def _absoluteError(self, value, approx, mask=None ):
        if mask is None:
            return np.max(np.abs(value-approx))
        else:
            return np.max(np.abs((value-approx)[mask]))
            
    


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
    
    
