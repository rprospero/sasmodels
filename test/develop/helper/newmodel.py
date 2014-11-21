'''
Created on Nov 14, 2014

@author: rhf
'''

from sasmodels import gpu, dll
from sasmodels.bumps_model import BumpsModel
import pprint as pp

class NewModel(object):
    '''
    Loads GPU based models from string
    '''


    def __init__(self, modelname, dtype="single",  **pars):
        '''
        
        '''
        self.modelname = modelname
        self.pars = pars
        self.model = None
        self.dtype = dtype
        
    def _buildModel(self, force=False):
        """
        Build a model
        """
        
        if force or self.model is None: 
            try:
                model = self._load_opencl(self.dtype)
            except Exception,exc:
                print exc
                print "... trying again with single precision"
                model = self._load_opencl(self.modelname, dtype='single')
            self.model = model
    
    def _load_opencl(self, dtype):
        sasmodels = __import__('sasmodels.models.'+self.modelname)
        module = getattr(sasmodels.models, self.modelname, None)
        kernel = gpu.load_model(module, dtype=dtype)
        return kernel
    
    def getModel(self, force=False):
        self._buildModel(force)
        return self.model
    
    def eval(self,data, cutoff=1e-5, nIterations=5):
        model = self.getModel()
        problem = BumpsModel(data, model, cutoff=cutoff, **self.pars)
        for _ in range(nIterations):
            problem.update()
            ret = problem.theory()
        return ret
        
        