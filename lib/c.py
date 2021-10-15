# config ######################################################################
OUTDIR = 'out/img_combined'
INDIR = 'out/img'
IGNORE = 'assets/_gluuonresources/'
LOOSE = 2
CLEAN = False
RENAME = True

DEBUG = 0
if DEBUG:
    INDIR = 'out/img/images/ingame/minimap/bg035/atlas'
DBG_SRCROOT = 'out/img'
DBG_IDFILE = 'out/img/_/%s'
DBG_CONTAINERS = 'out/img/containers.txt'
###############################################################################
import os
import re
from PIL import Image


if DEBUG:
    def dprint(*args, **kwargs):
        print(*args, **kwargs)
else:
    def dprint(*args, **kwargs):
        return

def _dst(fname):
    dprint(fname)
    global DST, inprefix
    if LOOSE == 2:
        d, b = os.path.split(fname)
        dd = d.split('/')
        tmp = '/'.join(dd[:-1])
        lastname = tmp[inprefix:].replace('/','.')+'/'+dd[-1]+'.'+b
        if lastname[0] == '/':
            lastname = lastname[1:]
        dst = os.path.join(DST, lastname)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        return dst
    elif LOOSE:
        lastname = fname[inprefix:].replace('/','_')
        if lastname[0] == '/':
            lastname = lastname[1:]
        dst = os.path.join(DST, lastname)
        return dst
    else:
        lastname = fname[inprefix:]
        if lastname[0] == '/':
            lastname = lastname[1:]
        dst = os.path.join(DST, lastname)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        return dst

if DEBUG:
    def _src(pid):
        global SRC, containers, idfile
        if pid in containers:
            fname, atype = containers[pid]
            return os.path.join(DBG_SRCROOT, fname)
        src = DBG_IDFILE%pid
        if os.path.exists(src):
            return src
        return None
else:
    def _src(pid):
        global SRC, containers, idfile
        if pid in containers:
            fname, atype = containers[pid]
            return os.path.join(SRC, fname)
        src = idfile%pid
        if os.path.exists(src):
            return src
        return None

def _alpha(m, a): 
    if type(m) == str:
        m = Image.open(m)
    if not a :
        return m
    size = m.size
    (r,g,b,z) = m.convert('RGBA').split()
    s = Image.open(a).resize(size, Image.LANCZOS).split()
    if len(s) == 4:
        a = s[3]
    elif len(s) == 3:
        a = s[0]
    else:
        raise
    merged = Image.merge("RGBA", (r,g,b,a))
    return merged

def _yuv(y, cb, cr, a=None): # params: filename
    if not y:
        return
    tmp = Image.open(y)
    size = tmp.size
    (z,z,z,y) = tmp.convert('RGBA').split()
    u = Image.open(cb).convert('L').resize(size, Image.LANCZOS)
    v = Image.open(cr).convert('L').resize(size, Image.LANCZOS)
    merged = Image.merge("YCbCr", (y,u,v)).convert('RGB')
    if a:
        merged = _alpha(merged, a)
    return merged

def _png(fname):
    base, ext = os.path.splitext(fname)
    if '_alphaa8' in base:
        m = fname.replace('_alphaa8', '')
        if os.path.exists(m):
            c = _alpha(m, fname)
            c.save(_dst(fname))
            return
    elif '_alpha' in base:
        m = fname.replace('_alpha', '')
        if os.path.exists(m):
            c = _alpha(m, fname)
            c.save(_dst(fname))
            return
    aname = base+'_alphaa8'+ext 
    if os.path.exists(aname):
        return
    aname = base+'_alpha'+ext 
    if os.path.exists(aname):
        return
    fr = open(fname, 'rb')
    fw = open(_dst(fname), 'wb')
    fw.write(fr.read())

def _tga(fname):
    base, ext = os.path.splitext(fname)
    img = Image.open(fname)
    img.save(_dst(base+'.png'))

def _mat(fname, outname=None):
    if fname == None or fname == '':
        raise
    if not outname:
        outname = fname
    data = open(fname).read()
    name = re.findall(r'string name = "(.*)"\n', data)
    if len(name) != 1:
        raise
    name = name[0]

    m = re.findall(r'first = "_MainTex".*?m_PathID = (.*?)\n', data, re.DOTALL)
    a = re.findall(r'first = "_AlphaTex".*?m_PathID = (.*?)\n', data, re.DOTALL)
    ma = re.findall(r'first = "_MaskAlphaTex".*?m_PathID = (.*?)\n', data, re.DOTALL)

    y = re.findall(r'first = "_TexY".*?m_PathID = (.*?)\n', data, re.DOTALL)
    cb = re.findall(r'first = "_TexCb".*?m_PathID = (.*?)\n', data, re.DOTALL)
    cr = re.findall(r'first = "_TexCr".*?m_PathID = (.*?)\n', data, re.DOTALL)
    ta = re.findall(r'first = "_TexA".*?m_PathID = (.*?)\n', data, re.DOTALL)

    if len(m)>=2 or len(a)>=2 or len(ma)>=2 \
            or len(y)>=2 or len(cb)>=2 or len(cr)>=2 or len(ta)>=2:
        raise

    isma = 0
    isyuva = 0
    if len(m) and m[0] != '0':
        isma = 1
        m = _src(m[0])
        if len(a) and a[0] != '0':
            a = _src(a[0])
        else:
            a = None

    if len(y) and y[0] != '0':
        isyuva = 1
        y = _src(y[0])
        u = _src(cb[0])
        v = _src(cr[0])
        if len(ta) and ta[0] != '0':
            ta = _src(ta[0])
        else:
            ta = None

    if isma:
        #output ma
        base, ext = os.path.splitext(outname)
        dname = os.path.dirname(outname)
        dst = _dst(dname+'_ma/'+name+'.mat.png')
        #if not os.path.exists(dst):
        #    raise
        count = 0
        while os.path.exists(dst):
            dst = _dst(dname+'_ma/'+name+'.mat.%d.png'%count)
            count += 1
        c = _alpha(m, a)
        c.save(dst)
    if isyuva:
        #output yuva
        base, ext = os.path.splitext(outname)
        dname = os.path.dirname(outname)
        dst = _dst(dname+'_yuv/'+name+'.mat.png')
        #if os.path.exists(dst):
        #    raise
        count = 0
        while os.path.exists(dst):
            dst = _dst(dname+'_yuv/'+name+'.mat.%d.png'%count)
            count += 1
        c = _yuv(y, u, v, ta)
        if c:
            c.save(dst)

def asset_save(img, fname, name, t):
    outname = os.path.join(fname, name)
    outname = _dst(outname+'.png')
    img.save(outname)

def _asset(fname):
    data = open(fname).read()
    name = re.findall(r'string name = "(.*)"\n', data)
    if len(name) > 0:
        name = name[0]
    else:
        name = None
    regex = r'\[(\d+)\]\n.*\n'
    regex += '.*PPtr<\$Texture2D> textureY\n.*\n.*m_PathID = (.*)\n'
    regex += '.*PPtr<\$Texture2D> textureCb\n.*\n.*m_PathID = (.*)\n'
    regex += '.*PPtr<\$Texture2D> textureCr\n.*\n.*m_PathID = (.*)\n'
    tmp = re.findall(regex, data)
    yuv = {}
    for i in tmp:
        yuv[i[0]] = (i[1], i[2], i[3])

    regex = r'\[(\d+)\]\n'
    regex += '.*PPtr<\$Texture2D> data\n.*\n.*m_PathID = (.*)\n'
    tmp = re.findall(regex, data)
    tdata = {}
    for i in tmp:
        tdata[i[0]] = i[1]

    regex = r'\[(\d+)\]\n.*\n'
    regex += '.*colorIndex = (.*)\n.*alphaIndex = (.*)\n'
    tmp = re.findall(regex, data)
    pair = {}
    for i in tmp:
        pair[i[0]] = (i[1], i[2])

    dprint(fname)
    if len(pair) > 0:
        for i in pair:
            m = pair[i][0]
            a = pair[i][1]
            if m == '-1':
                continue
            if m in yuv:
                m = yuv[m]
                isyuv = 1
            elif m in tdata:
                m = tdata[m]
                isyuv = 0
            else:
                raise
            if a in tdata:
                a = tdata[a]
            else:
                a = None
            if isyuv:
                c = _yuv( _src(m[0]), _src(m[1]), _src(m[2]), _src(a) )
            else:
                c = _alpha( _src(m), _src(a) )
            if c:
                asset_save(c, fname, name+'_'+i, 'yuv')

    mat = re.findall(r'PPtr<\$Material>.*\n.*\n.*m_PathID = (.*)\n', data)
    count = 0
    if len(mat)>0:
        for i in mat:
            if i != '0':
                _mat(_src(i), fname+'.mat')
                #_mat(_src(i), fname+'/%s.mat'%i)

def clean(dst):
    os.system('rm -r %s'%dst)

def main():
    global INDIR, IGNORE, inprefix
    global ROOT, SRC, DST
    global containers, idfile
    ROOT = os.path.dirname(os.path.realpath(__file__)) + '/..'
    SRC = os.path.join(ROOT, INDIR)
    DST = os.path.join(ROOT, OUTDIR)
    inprefix = len(SRC)+1
    containers = {}
    if IGNORE[-1] != '/':
        IGNORE += '/'
    ignore = len(IGNORE)-1

    if DEBUG:
        c = DBG_CONTAINERS
    else:
        c = os.path.join(SRC, 'containers.txt')
    for i in open(c):
        _id, path, _type = i.split(',')
        containers[_id.strip()] = (path.strip()[ignore:], _type)

    idfile = os.path.join(SRC, '_') + '/%s'

    if CLEAN:
        clean(DST)
    if RENAME:
        count = 0
        base = DST
        while os.path.exists(DST):
            DST = base + '.%d'%count
            count += 1

    os.makedirs(DST, exist_ok=True)

    # start walk
    for root, dirs, files in os.walk(SRC, topdown=False):
        if files == []:
            continue
        if '.git' in root:
            continue
        if root[-1] == '_' :
            continue
        print(root)
        for f in files:
            ext = os.path.splitext(f)[1]
            src = os.path.join(root, f)
            if ext == '.png':
                _png(src)
            elif ext == '.tga':
                _tga(src)
            elif ext == '.mat':
                _mat(src)
            elif ext == '.asset':
                _asset(src)

def test():
    #m = _yuv(INDIR+'/_/-5468202399702066998.png',
    #    INDIR+'/_/-7892557579526219953.png',
    #    INDIR+'/_/2115422073092249201.png')
    m = Image.open('1.png')
    ma = _alpha(m, '2.png')
    ma.save('test.png')

if __name__ == '__main__':
    main()
