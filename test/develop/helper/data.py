'''
Created on Nov 14, 2014

@author: rhf
'''

import math
import numpy as np

class Data(object):
    '''
    Class to store data for the models.
    
    Get SasView data for Old models
    Get Bumps data for the new models
    
    '''


    def __init__(self, qmax=0.05):
        '''
        @param qmax: Qmax should come from teh csv file
        '''
        self.qmax = qmax
        self.data1D = None
        self.data2D = None
    
    def get1DSasView(self, force=False):
        data = self._get1D(force) 
        return data.x
        
    def get2DSasView(self, force=False):
        data = self._get2D(force) 
        return [data.qx_data, data.qy_data]
    
    def get1DBumps(self, force=False):
        data = self._get1D(force) 
        return data
    
    def get2DBumps(self, force=False):
        data = self._get2D(force) 
        return data
    
    def get1DMask(self):
        """ there's no mask for 1d """
        return slice(None, None)
    
    def get2DMask(self):
        """ Inverts the mask so we can index the non masked peaks """
        return ~self.data2D.mask
    
    def _get1D(self, force):
        if force or self.data1D is None:
            from sasmodels.bumps_model import empty_data1D
            qmax = math.log10(self.qmax)
            self.data1D = empty_data1D(np.logspace(qmax-3, qmax, 128))
        return self.data1D
    def _get2D(self, force):
        if force or self.data2D is None:
            from sasmodels.bumps_model import empty_data2D, set_beam_stop
            data = empty_data2D(np.linspace(-self.qmax, self.qmax, 128))
            set_beam_stop(data, 0.004)
            self.data2D = data
        return self.data2D
    
    
def test():
    import pprint as pp
    d = Data(0.05)
    pp.pprint(d.get1D())
    print "*****************"
    pp.pprint(d.get2D())
    
    
if __name__ == "__main__":
    test()            