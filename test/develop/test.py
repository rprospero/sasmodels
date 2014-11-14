'''
Created on Nov 14, 2014

@author: rhf
'''

import helper.params.Params as Params
#from helper.params import Params
from helper.sasview import SasViewModel
from helper.data import Data


def test():
    
    p = Params()
    allOldModelsNames = p.getAllOldModelsNames()
    
    for modelName in  allOldModelsNames:
        modelParams = p.getOldModelParamNamesAndValues(modelName)
        model = SasViewModel(modelName,modelParams)
        d = Data()
        model.eval(d.get1D())
        model.eval(d.get2D())
    
if __name__ == "__main__":
    test()     
