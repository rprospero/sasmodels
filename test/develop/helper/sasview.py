'''
Created on Nov 14, 2014

@author: rhf
'''
from IPython.nbconvert.filters import datatypefilter

class SasViewModel(object):
    '''
    classdocs
    '''


    def __init__(self, modelname, **pars):
        '''
        Constructor
        '''
        self.modelname = modelname
        self.pars = pars
        self.model = None
        
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
            # convert model parameters from sasmodel form to sasview form
            #print "old",sorted(pars.items())
            modelname  = self.modelname
            #print "new",sorted(pars.items())
            sans = __import__('sans.models.'+modelname)
            ModelClass = getattr(getattr(sans.models,modelname,None),modelname,None)
            if ModelClass is None:
                raise ValueError("could not find model %r in sans.models"%modelname)
            model = ModelClass()
                    
            for k,v in self.pars.items():
                if k.endswith("_pd"):
                    model.dispersion[k[:-3]]['width'] = v
                elif k.endswith("_pd_n"):
                    model.dispersion[k[:-5]]['npts'] = v
                elif k.endswith("_pd_nsigma"):
                    model.dispersion[k[:-10]]['nsigmas'] = v
                elif k.endswith("_pd_type"):
                    model.dispersion[k[:-8]]['type'] = v
                else:
                    model.setParam(k, v)
            self.model = model
            
    
    def getModel(self):
        self._buildModel()
        return self.model
    
    def eval(self,data):
        model = self.getModel()
        ret = model.evalDistribution(data)
        return ret
        
        