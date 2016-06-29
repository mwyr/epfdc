
def readabstracts(fname):
    import codecs
    import json
    
    fdata = codecs.open(fname,encoding='utf8').read()
    
    data = json.loads( fdata )
    
    return data
    
    
def fill_template(opts):
    title = opts['title']
    contentfile = opts['contentfile']
    author = opts['author']
    email = opts['email']
#    authors = opts['coauthors']
#    affils = opts['affils']
    
    buffer = """
    \stepcounter{Abstractcounter} %counter increase
    % formatting table of contents entry    
    \\addcontentsline{toc}{section} 
    { \\arabic{Abstractcounter} \n\t\t\t{""" + title + """} \\\\ \t\t\t
    \\normalfont\small """ + author + """ }
    % end -- formatting table of contents entry 
    """
    
    buffer = buffer + """
    { \centering{ \\textsc{ \\textbf{ \large{\\arabic{Abstractcounter} """ + title +"""}} } } \\\\    
    } 
    """
    
#    buffer = buffer + """  { \centering{ \\textbf{ """ + author + """}} \\\\  
#    } """
    
    names = ''
    for i,val in enumerate( opts['authors']):
        affilid = opts['authorsaffilid'][i]
        
        names = names + '\n\t\t\t\t'+val
        
        if ( len( opts['affilname'] ) != 1):
            texsuperscript = '\\textsuperscript'
            names = names + texsuperscript + str(affilid+1) 
        names = names + ','
        
    names = names[:-1] #cutting out ending comma 
    
    buffer = buffer + """  { \centering{ \\textbf{ """ + names + """} \\\\ 
    """
    buffer = buffer + '\\blfootnote{Corresponding author: ' + author + ', '
    buffer = buffer + 'e-mail: \href{mailto:' + email +'}{'+email.replace('_','\_') +'} }\n'
    # todo: handle single affiliation properly (without numbers)
        
    affil = ''
    for i,val in enumerate( opts['affilname']):
        if ( len( opts['affilname'] ) != 1):
                affil = str(i+1) + ' '
        affil = affil + val 
        buffer = buffer + """  """ + affil + """ \\\\ 
"""
    
    buffer = buffer + '\t} } \n'
    buffer = buffer + '\t\\vspace{.3cm} \n' #extra space after affiliation data
    
    buffer = buffer + """ \\input{ """ + contentfile + """}    \\\\
    """
    
    if 'image' in opts:
        imagefile = opts['image']
        captionfile = opts['captionfile']
        
        sidebyside = True
        if ( sidebyside ):
            buffer = buffer + """
            {
            
            \\begin{minipage}[c]{\\textwidth}
                \centering
                \\includegraphics[height=7cm,width=7cm,keepaspectratio]{""" + imagefile + """}
            
                { \\textbf{Figure: }\\input{""" + captionfile + """ }}
            \\end{minipage}
            
            }
            """

#    buffer = buffer + """
#    \\end{minipage}
#    """
    
    
    buffer = buffer + """
    \\vspace{.5cm}
    \\newpage
    """
    return buffer
    
def run(data):
#    for i,abstract in enumerate(data):
#        print(i, abstract['registration_status'])
    import codecs
    
    fname = 'tex/myabstracts.tex'
    with codecs.open(fname, 'w',encoding='utf8') as fout:
        for i,entry in enumerate(data):
#        for i,entry in enumerate(data[0:1]):
            print('Processing abstract: ', i)
            opts={}
            
            first_name = entry['first_name']
            last_name = entry['last_name']
            name = first_name + ' ' + last_name
            opts['author'] = name
            
            authors = []
            authorsaffilid = []
            for j,val in enumerate( entry['authors'] ):
                authors.append( val['name'] )
                curr_affilid = val['affil_id']
                authorsaffilid.append( curr_affilid )
            
            opts['authors'] = authors
            opts['authorsaffilid'] = authorsaffilid
            opts['affilname'] = entry['affils']
#            print(opts['affilname'])
                
            title = entry['title']
            opts['title'] = title
            
            content = entry['content']
            contentfile = 'abstract_content/ab' + str(i).zfill(3) + '.tex'
            with codecs.open('tex/'+contentfile,'w',encoding='utf8') as file:
                print(content, file=file)
            opts['contentfile'] = contentfile
            
            image = entry.get('image',"")
            if image is not None:
                opts['image'] = image
            
            imagecaption = entry['image_caption']
            if imagecaption is not '':
                captionfile = 'caption/cap' + str(i).zfill(3)+'.tex'
                with codecs.open('tex/'+captionfile,'w',encoding='utf8') as file:
                    print(imagecaption, file=file,end='')
                opts['captionfile'] = captionfile

            opts['email'] = entry['email']
            t= fill_template(opts)
            outfile = 'out/out' + str(i).zfill(3) + '.tex'
            with codecs.open('tex/'+outfile,'w',encoding='utf8') as file:
                print(t,file=file)
                
            inputcmd = '\input{'+ outfile +'}'
            print(inputcmd,file=fout)

def printfield(data,key):
    for i,val in enumerate(data):
        print(i, val[key])
            
if __name__ == '__main__':
    print('###############################')
    print('# 8th European Postgraduate   #')
    print('# Fluid Dynamics Conference   #')
    print('# Book of Abstracts generator #')
    print('###############################')
    
    data = readabstracts('abstracts.json')
    
    run(data)
    
