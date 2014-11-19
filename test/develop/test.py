'''
Created on Nov 14, 2014

@author: rhf
'''

#import helper.params.Params as Params
from helper.params import Params
from develop.helper.oldmodel import OldModel
from develop.helper.newmodel import NewModel
from helper.data import Data

import pprint as pp
import numpy as np

def testOldModel():
    
    p = Params()
    allOldModelsNames = p.getAllOldModelsNames()
    
    for modelName in  allOldModelsNames:
        print "* Evaluating Old model:",  modelName
        ret1D,ret2D  = evalOldModel(p, modelName)

def evalOldModel(p, modelName):
    modelParams = p.getOldModelParamNamesAndValues(modelName)
    model = OldModel(modelName,**modelParams)
    
    modelQMax = p.getOldModelUniqueCollumValue(modelName,"qmax")
    d = Data(modelQMax)
    
    modelNIterations = p.getOldModelUniqueCollumValue(modelName,"n_sasview")
    ret1D = model.eval(d.get1DSasView(),nIterations=modelNIterations)
    ret2D = model.eval(d.get2DSasView(),nIterations=modelNIterations)
    return ret1D,ret2D, d.get2DMask()
    
def testNewModel():
    
    p = Params()
    allNewModelsNames = p.getAllNewModelsNames()
    
    for modelName in  allNewModelsNames:
        print "* Evaluating New model:",  modelName
        ret1D,ret2D  = evalNewModel(p, modelName)

def evalNewModel(p, modelName):
    modelParams = p.getNewModelParamNamesAndValues(modelName)
    
    modelDType = p.getNewModelUniqueCollumValue(modelName,"dtype")
    model = NewModel(modelName,dtype=modelDType,**modelParams)
    
    modelQMax = p.getNewModelUniqueCollumValue(modelName,"qmax")
    d = Data(modelQMax)
    
    modelNIterations = p.getNewModelUniqueCollumValue(modelName,"n_opencl")
    modelCutOff = p.getNewModelUniqueCollumValue(modelName,"cutoff")
    
    ret1D = model.eval(d.get1DBumps(), cutoff=modelCutOff, nIterations=modelNIterations)
    ret2D = model.eval(d.get2DBumps(), cutoff=modelCutOff, nIterations=modelNIterations)
    return ret1D,ret2D, d.get2DMask()

def testBothModels():
    p = Params()
    models = p.getAllOldAndNewModelsNames()
    
    for oldModelName,newModelName in models:
        print "* Evaluating both Models:",oldModelName, "::", newModelName
        
        retOld1D,retOld2D, idxOld2D  = evalOldModel(p, oldModelName)
        retNew1D,retNew2D, idxNew2D  = evalNewModel(p, newModelName)
        
        
        # 1D
        resid, relerr = np.zeros_like(retNew1D), np.zeros_like(retNew1D)
        resid = (retNew1D - retOld1D)
        relerr = resid/retOld1D
        print "1D max(|ocl-sasview|)", max(abs(resid)), "\t",
        print "1D max(|(ocl-sasview)/ocl|)", max(abs(relerr))
        
        # 2D
        resid, relerr = np.zeros_like(retNew2D), np.zeros_like(retNew2D)
        resid[idxOld2D] = (retNew2D - retOld2D)[idxOld2D]
        relerr[idxOld2D] = resid[idxOld2D]/retOld2D[idxOld2D]
        print "2D max(|ocl-sasview|)", max(abs(resid[idxOld2D])), "\t",
        print "2D max(|(ocl-sasview)/ocl|)", max(abs(relerr[idxOld2D]))
         
        print  "Relative Error: 1D = %.2e :: 2D = %.2e "%(np.max(np.abs(retNew1D - retOld1D)) / np.max(retOld1D),
                                                   np.max(np.abs((retNew2D - retOld2D)[idxOld2D])) / np.max(retOld2D[idxOld2D]))

        print  "MSE: 1D = %.2e :: 2D = %.2e "% ( _mse(retNew1D,retOld1D,None),
                                            _mse(retNew2D[idxOld2D], retOld2D[idxOld2D], None))


def _mse(A,B,ax):
    """
    Mean Squared Error between two matrices
    with ax=0 the average is performed along the row, for each column, returning an array
    with ax=1 the average is performed along the column, for each row, returning an array
    with ax=None the average is performed element-wise along the array, returning a single value
    """
    mse = ((A - B) ** 2).mean(axis=ax)
    return mse
    
if __name__ == "__main__":     
    #testOldModel()
    #testNewModel()
    testBothModels()
    print "DONE!"