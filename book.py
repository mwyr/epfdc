
def readabstracts(fname):
    import codecs
    import json
    
    fdata = codecs.open(fname,encoding='utf8').read()
    
    data = json.loads( fdata )
    
    return data
    
    
if __name__ == '__main__':
    print('###############################')
    print('# 8th European Postgraduate   #')
    print('# Fluid Dynamics Conference   #')
    print('# Book of Abstracts generator #')
    print('###############################')
    
    data = readabstracts('abstracts.json')
    