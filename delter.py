import re, os
def delter(rpath,npath):
    with open(rpath, encoding='utf-8') as f:
        file = f.read()
    s='<link rel="stylesheet" href="{}.css">'
    a=file.find('<head>')
    b=file.find('</head>')
    ls=re.findall(s.format('(.*?)'), file[a : b])
    for l in ls:
        assert os.path.isfile(l+'.css')
        with open(l + '.css', encoding='utf-8') as f:
            css=f.read()
        file=file.replace(s.format(l), '<style>' + css + '</style>', 1)
        del css
    s='<script src="{}.js"></script>'
    ls=re.findall(s.format('(.*?)'), file[a : b])
    for l in ls:
        assert os.path.isfile(l+'.js')
        with open(l + '.js', encoding='utf-8') as f:
            js=f.read()
        file=file.replace(s.format(l), '<script>' + js + '</script>', 1)
        del js
    s='<script src="{}.js" defer></script>'
    ls=re.findall(s.format('(.*?)'), file[a : b])
    a=file.rfind('</body>')
    for l in ls:
        assert os.path.isfile(l+'.js')
        with open(l + '.js', encoding='utf-8') as f:
            js=f.read()
        file=file[:a + 7].replace(s.format(l), '', 1) + '<script>' + js + '</script>' + file[a + 7:]
        del js
    file=file.replace(' = ', '=').replace(' => ', '=>').replace(' > ','>').replace(' < ','<')\
        .replace(' && ','&&').replace(' || ','||').replace(' === ','===').replace(' !== ','!==')
    file=file.replace('\n','').replace('  ','')
    file=file.replace(': ',':').replace(', ',',').replace(';}','}')
    with open(npath,'w',encoding='utf-8')as f:
        f.write(file)
delter(r'./calendar3-3.html',r'./calendar3-3.html')