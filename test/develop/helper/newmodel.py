'''
Created on Nov 14, 2014

@author: rhf
'''

from sasmodels import gpu, dll
from sasmodels.bumps_model import BumpsModel

class NewModel(object):
    '''
    classdocs
    '''


    def __init__(self, modelname, dtype="single",  **pars):
        '''
        Constructor
        '''
        self.modelname = modelname
        self.pars = pars
        self.model = None
        self.dtype = dtype
        
    def _buildModel(self, force=False):
        """
        pars = {'scale': 1, 'radius_pd_type': 'gaussian', 
        'sldSph': 6e-06, 'radius_pd_nsigma': 3, 'radius_pd': 0.2, 
        'radius': 120, 'radius_pd_n': 45, 'background': 0, 'sldSolv': 1e-06}
        modelname = SphereModel
        model.dispersion  = {'radius': {'npts': 45, 'type': 'gaussian', 'nsigmas': 3, 'width': 0.2}}
        
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
    
    def getModel(self):
        self._buildModel()
        return self.model
    
    def eval(self,data, cutoff=1e-5, nIterations=5):
        model = self.getModel()
        problem = BumpsModel(data, model, cutoff=cutoff, **self.pars)
        for _ in range(nIterations):
            problem.update()
            ret = problem.theory()
        return ret
        
        