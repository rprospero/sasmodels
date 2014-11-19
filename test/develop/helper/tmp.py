"""

Dummy file to add to the CSV file the high and low limits of random values. 

"""

newfile = "defs_pd_tmp.csv"
oldfile = "defs_pd.csv"

def getParamMinMaxValue(paramName):
    if any(paramName.endswith(s) for s in ('_pd_n','_pd_nsigma','_pd_type')):
        return None
    elif any(s in paramName for s in ('theta','phi','psi')):
        # orientation in [-180,180], orientation pd in [0,45]
        if paramName.endswith('_pd'):
            return ["0","45"]
        else:
            return ["-180","180"]
    elif 'sld' in paramName:
        # sld in in [-0.5,10]
        return ["-0.5","10"]
    elif paramName.endswith('_pd'):
        # length pd in [0,1]
        return ["0","1"]
    else:
        # length, scale, background in [0,200]
        return ["0","200"]


def addMinMax():
    with open(newfile, 'w') as outfile, open(oldfile, 'r') as infile:
        for idx,line in enumerate(infile):
            fields = line.split(",")
            p = fields[3] #param_new
            
            minMax = getParamMinMaxValue(p)
            if minMax is None or idx == 0:
                outfile.write(line)
            else:
                fields[5:7] = minMax
                outfile.write(",".join(fields))
                
        
if __name__ == "__main__":     
    addMinMax()