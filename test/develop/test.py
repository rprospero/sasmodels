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

def testOldModel():
    
    p = Params()
    allOldModelsNames = p.getAllOldModelsNames()
    
    for modelName in  allOldModelsNames:
        print "* Evaluating Old model:",  modelName
        modelParams = p.getOldModelParamNamesAndValues(modelName)
        model = OldModel(modelName,**modelParams)
        
        modelQMax = p.getOldModelUniqueCollumValue(modelName,"qmax")
        d = Data(modelQMax)
        
        modelNIterations = p.getOldModelUniqueCollumValue(modelName,"n_sasview")
        model.eval(d.get1DSasView(),nIterations=modelNIterations)
        model.eval(d.get2DSasView(),nIterations=modelNIterations)
        
def testNewModel():
    
    p = Params()
    allNewModelsNames = p.getAllNewModelsNames()
    
    for modelName in  allNewModelsNames:
        print "* Evaluating New model:",  modelName
        modelParams = p.getNewModelParamNamesAndValues(modelName)
        
        modelDType = p.getNewModelUniqueCollumValue(modelName,"dtype")
        model = NewModel(modelName,dtype=modelDType,**modelParams)
        
        modelQMax = p.getNewModelUniqueCollumValue(modelName,"qmax")
        d = Data(modelQMax)
        
        modelNIterations = p.getNewModelUniqueCollumValue(modelName,"n_opencl")
        modelCutOff = p.getNewModelUniqueCollumValue(modelName,"cutoff")
        
        model.eval(d.get1DBumps(), cutoff=modelCutOff, nIterations=modelNIterations)
        model.eval(d.get2DBumps(), cutoff=modelCutOff, nIterations=modelNIterations)

def testBothModels():
    p = Params()
    models = p.getAllOldAndNewModelsNames()
    
    for oldModelName,newModelName in models:
        print "* Evaluating both Models:",oldModelName, "::", newModelName
        
    

    
if __name__ == "__main__":
    testBothModels()     
    #testOldModel()
   # testNewModel()
    print "DONE!"