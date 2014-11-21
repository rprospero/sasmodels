'''
Created on Nov 13, 2014

@author: rhf

See:
http://web.mit.edu/yamins/www/tabular/

'''

# Ugly way of importing tab!! TO FIX!
import os
dirname, filename = os.path.split(os.path.abspath(__file__))
import sys
sys.path.append(dirname)

import tabular as tb
import pprint
import numpy as np
from docutils.nodes import row
from pytools.datatable import Row
import ast
from random import uniform


def singleton(cls):
    """
    Poor singleton decorator!
    Note that super() and classmethods won't work on any class decorated!! 
    """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class Params(object):
    '''
    Interface with the CSV file. 
    '''

    def __init__(self, csvFilename="defs_pd.csv"):
        '''
        Constructor
        '''
        self.filename = self._getFullPath(csvFilename)
        print "Using:",self.filename
        self.data = tb.tabarray(SVfile = self.filename, delimiter=',')
        self.data = self._increaseStringLenght(self.data)
    
    def getOldModelParamValue(self,modelName,ParamName):
        return self.data[ (self.data['model_old']==modelName)  & (self.data['param_old']==ParamName) ]['value']
    
    def getNewModelParamValue(self,modelName,ParamName):
        return self.data[ (self.data['model_new']==modelName)  & (self.data['param_new']==ParamName) ]['value']
        
    def getOldModelParamNamesAndValues(self,modelName):
        records = self.data[ self.data['model_old']==modelName ][['param_old','value']].extract()
        return self._fromTabularToDict(records)
    
    def getNewModelParamNamesAndValues(self,modelName):
        records =  self.data[ self.data['model_new']==modelName ][['param_new','value']].extract()
        return self._fromTabularToDict(records)
    
    def getModelsParamNamesAndValuesRandom(self,oldModelName,newModelName):
        """
        Returns list of lists with two dictionaries of params for old and new models
        """
        records =  self.data[ (self.data['model_old']==oldModelName) & (self.data['model_new']==newModelName) ][['param_old','param_new','value','low','high']].extract()
        if len(records) == 0:
            raise ValueError("Problem getting ParamNamesAndValuesLimit: Make sure oldModelName and newModelName are in the same row!")
        return self._evalFieldsToRandom(records)
    
    def getAllOldModelsNames(self):
        records =  self.data['model_old']
        return np.unique(records).tolist()
    
    def getAllNewModelsNames(self):
        records =  self.data['model_new']
        return np.unique(records).tolist()
    
    def getAllOldAndNewModelsNames(self):
        records =  self.data[['model_old','model_new']]
        return np.unique(records).tolist()
    
    def getOldModelUniqueCollumValue(self,modelName,collumnName):
        """ Collumn value must be unique """
        records = self.data[ self.data['model_old']==modelName  ][collumnName]
        singleRecord =  np.unique(records)
        if len(singleRecord) > 1:
            raise ValueError("Collumn value is not unique! Check CSV File!")
        else:
            return singleRecord[0]
    
    def getNewModelUniqueCollumValue(self,modelName,collumnName):
        """ Collumn value must be unique """
        records = self.data[ self.data['model_new']==modelName  ][collumnName]
        singleRecord =  np.unique(records)
        if len(singleRecord) > 1:
            raise ValueError("Collumn value is not unique! Check CSV File!")
        else:
            return singleRecord[0]
    
    
    def _getFullPath(self,filename):
        dirname, _ = os.path.split(os.path.abspath(__file__))
        if os.path.isabs(filename):
            if os.path.exists(filename):
                return filename
            else:
                raise IOError(filename)
        else:
            path = os.path.join(dirname, filename)
            if os.path.exists(path):
                return path
            else :
                raise IOError(path)
                

    def _fromTabularToDict(self,record):
        retDic = {}
        for k, v in record:
            try:
                v = ast.literal_eval(v)
            except:
                pass
            retDic[k]=v
        return retDic

    def _evalFields(self,records):
        ret = []
        for row in records:
            sub = []
            for i in row:
                try:
                    i = ast.literal_eval(i)
                except:
                    pass
                sub.append(i)
            ret.append(sub)
        return ret
    
    def _evalFieldsToRandom(self,records):
        """
        input [ ['param_old','param_new','value','low','high'], ... ]
        Output {oldParam:value, .. },{newParam : value, }
        """
        oldParams = {}
        newParams = {}
        for row in records:
            if 'nan' not in row[-1] and 'nan' not in row[-2]:
                maxValue = ast.literal_eval(row[-1])
                minValue = ast.literal_eval(row[-2])
                v = uniform(minValue,maxValue)
            else:
                try:
                    v = ast.literal_eval(row[-3])
                except:
                    v = row[-3] # text
            oldParams[row[0]]=v
            newParams[row[1]]=v
        return oldParams, newParams
    
    def _createNewCsvFileWithPDParams(self, paramsNewToExclude = ['scale', 'background', 'sld', 'solvent_sld', 
                                                                  'core_sld', 'shell_sld', 'solvent_sld' ]):
        """
        Create new CSV file with _pd concatenate to fields
        Save the output file as *_pd_tmp.csv
        """
        outFile = self.filename.split('.')[0]+'_pd_tmp.'+self.filename.split('.')[1]
        paramsToAddPD = np.setdiff1d(self.data['param_new'], paramsNewToExclude)
        
        for row in self.data:
            if row['param_new'] in paramsToAddPD:
                newModelParPD = row['param_new'] + "_pd"
                oldModelParPD = row['param_old'] + "_pd"
                newModelParPDN = row['param_new'] + "_pd_n"
                oldModelParPDN = row['param_old'] + "_pd_n"
                newModelParPDType = row['param_new'] + "_pd_type"
                oldModelParPDType = row['param_old'] + "_pd_type"
                newModelParPDSigma = row['param_new'] + "_pd_sigma"
                oldModelParPDSigma = row['param_old'] + "_pd_sigma"
                
                newRow = row.copy()
                newRow['param_new'] = newModelParPD
                newRow['param_old'] = oldModelParPD
                self.data = self.data.addrecords(newRow)
    
                newRow = row.copy()
                newRow['param_new'] = newModelParPDN
                newRow['param_old'] = oldModelParPDN
                self.data = self.data.addrecords(newRow)
                
                newRow = row.copy()
                newRow['param_new'] = newModelParPDType
                newRow['param_old'] = oldModelParPDType
                self.data = self.data.addrecords(newRow)
                
                newRow = row.copy()
                newRow['param_new'] = newModelParPDSigma
                newRow['param_old'] = oldModelParPDSigma
                self.data = self.data.addrecords(newRow)
    
        self.data.sort(order=['model_old','model_new','param_old','param_new'])
        self.data.saveSV(outFile)
    
    def _increaseStringLenght(self, nparray):
        """
        CSV to numpy cuts the string field size to the maximum strlen
        This function increases the string witdh to 48 chars
        """ 
        inTypes = nparray.dtype
        outTypes = []        
        for t in inTypes.descr:
            tout = t[1]
            if tout.startswith('|S'):
                tout = 'S48'
            outTypes.append((t[0],tout))
        return nparray.astype(outTypes)
    
    
    
def test():
    p = Params()
    #print p.data
    #pprint.pprint(p.getOldModelParamValue('CappedCylinderModel','len_cyl'))
    #pprint.pprint(p.getOldModelParamNamesAndValuesLimit('CappedCylinderModel'))
    #pprint.pprint(p.getOldModelUniqueCollumValue('CappedCylinderModel','cutoff'))
    pprint.pprint(p.getModelsParamNamesAndValuesRandom('CappedCylinderModel', 'capped_cylinder'))
    
    #p._createNewCsvFileWithPDParams()
    
if __name__ == "__main__":
    test()        