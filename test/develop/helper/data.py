'''
Created on Nov 14, 2014

@author: rhf
'''

import math
import numpy as np

class Data(object):
    '''
    classdocs
    '''


    def __init__(self, qmax=0.05):
        '''
        Constructor
        '''
        self.qmax = qmax
        self.data1D = None
        self.data2D = None
        
    def get1D(self, force=False):
        if force or self.data1D is None:
            from sasmodels.bumps_model import empty_data1D
            qmax = math.log10(self.qmax)
            data = empty_data1D(np.logspace(qmax-3, qmax, 128))
            self.data1D = data.x
        return self.data1D
    
    def get2D(self, force=False):
        if force or self.data2D is None:
            from sasmodels.bumps_model import empty_data2D, set_beam_stop
            data = empty_data2D(np.linspace(-self.qmax, self.qmax, 128))
            set_beam_stop(data, 0.004)
            self.data2D = [data.qx_data, data.qy_data]
        return self.data2D
    
    
    
def test():
    import pprint as pp
    d = Data(0.05)
    pp.pprint(d.get1D())
    print "*****************"
    pp.pprint(d.get2D())
    
    
if __name__ == "__main__":
    test()            