
def readabstracts(fname):
    import codecs
    import json
    
    fdata = codecs.open(fname,encoding='utf8').read()
    
    data = json.loads( fdata )
    
    return data
    
    
    
def run(data):
#    for i,abstract in enumerate(data):
#        print(i, abstract['registration_status'])
    import codecs
    
    fname = 'tex/myabstracts.tex'
    with codecs.open(fname, 'w',encoding='utf8') as fout:
        for i,entry in enumerate(data):
            print('Processing abstract: ', i)
            opts={}
            
            first_name = entry['first_name']
            last_name = entry['last_name']
            title = entry['title']
            content = entry['content']
            
            name = first_name + ' ' + last_name
            
            contentfile = 'abstract_content/ab' + str(i).zfill(3) + '.tex'
            with codecs.open('tex/'+contentfile,'w',encoding='utf8') as file:
                print(content, file=file)
            
            imagefile = entry.get('image',"")
            if imagefile is None:
                imagefile=''
            
            imagecaption = entry['image_caption']
            if imagecaption is None:
                imagecaption=''
            else:
                captionfile = 'caption/cap' + str(i).zfill(3)+'.tex'
                with codecs.open('tex/'+captionfile,'w',encoding='utf8') as file:
                    print(imagecaption, file=file)
                opts['captionfile'] = captionfile

            
            opts['title'] = title
            opts['author'] = name
            opts['contentfile'] = contentfile
            opts['image'] = imagefile
            
            options = ''
            for key in opts:
                options = options + key + '=' + opts[key] +','
            options = options[:-1] #get rid of trailing comma
            
            lineout='\myabstract['+options+']{}'
#            lineout='\myabstract{'+title+'}'
#            lineout=lineout + '{'+name+'}'
#            lineout=lineout + '{'+ contentfile + '}'
#            lineout=lineout + '{'+ imagefile + '}'
#            lineout=lineout + '{'+ imagecaption + '}'
            print(lineout,file=fout)
        
    
if __name__ == '__main__':
    print('###############################')
    print('# 8th European Postgraduate   #')
    print('# Fluid Dynamics Conference   #')
    print('# Book of Abstracts generator #')
    print('###############################')
    
    data = readabstracts('abstracts.json')
    
    run(data)