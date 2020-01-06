# config ######################################################################
OUTDIR = 'out_img'
INDIR = 'out/y'
IGNORE = 'assets/_gluuonresources/'

###############################################################################
import os
import re
from PIL import Image


def _alpha(m, a): 
    if type(m) == str:
        m = Image.open(m)
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
    tmp = Image.open(y)
    size = tmp.size
    (z,z,z,y) = tmp.convert('RGBA').split()
    u = Image.open(cb).convert('L').resize(size, Image.LANCZOS)
    v = Image.open(cr).convert('L').resize(size, Image.LANCZOS)
    merged = Image.merge("YCbCr", (y,u,v)).convert('RGB')
    if a:
        merged = _alpha(merged, a)
    return merged

def _dst(fname):
    global DST, inprefix
    dst = os.path.join(DST, fname[inprefix:])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    return dst

def _src(pid):
    global SRC, containers
    if pid in containers:
        fname, atype = containers[pid]
        return os.path.join(SRC, fname)
    src = os.path.join(SRC, '_/%s'%pid )
    if os.path.exists(src):
        return src


def _png(fname):
    fr = open(fname, 'rb')
    fw = open(_dst(fname), 'wb')
    fw.write(fr.read())

def _mat(fname, outname=None):
#    print('_mat')
#    print(fname)
    if fname == None:
        print('no fname')
        exit()
        return
    if not outname:
        outname = fname
    data = open(fname).read()
    name = re.findall(r'string name = "(.*)"\n', data)
    if len(name) != 1:
        print('no name')
        print(name)
        exit()
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
        dst = _dst(dname+'/'+name+'.mat.png')
        #dst = _dst(base+'.png')
        if os.path.exists(dst):
            raise
        if a:
            c = _alpha(m, a)
            c.save(dst)
        else:
            fw = open(dst, 'wb')
            fr = open(m, 'rb')
            fw.write(fr.read())
    if isyuva:
        #output yuva
        base, ext = os.path.splitext(outname)
        dname = os.path.dirname(outname)
        dst = _dst(dname+'/'+name+'.mat.png')
        #dst = _dst(base+'.png')
        count = 0
        while os.path.exists(dst):
            dst = _dst(dname+'/'+name+'.%d.mat.png'%count)
            count += 1
        c = _yuv(y, u, v, ta)
        c.save(dst)

def asset_save(img, fname, name, t):
    print('assetsave',fname)
    exit()
    img.save(fname)

def _asset(fname):
    data = open(fname).read()
    name = re.findall(r'string name = "(.*)"\n', data)
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
    alpha = {}
    for i in tmp:
        alpha[i[0]] = i[1]

    regex = r'\[(\d+)\]\n.*\n'
    regex += '.*colorIndex = (.*)\n.*alphaIndex = (.*)\n'
    tmp = re.findall(regex, data)
    pair = {}
    for i in tmp:
        pair[i[0]] = (i[1], i[2])

    if len(pair) > 0:
        for i in pair:
            m = yuv[ pair[i][0] ]
            a = alpha[ pair[i][1] ]
            m = _yuv(_src(m[0]), _src(m[1]), _src(m[2]))
            c = _alpha(m, _src(a))
            asset_save(c, fname, name, 'yuv')

    mat = re.findall(r'PPtr<\$Material>.*\n.*\n.*m_PathID = (.*)\n', data)
    if len(mat)>0:
        for i in mat:
            print(i)
            _mat(_src(i), fname+'.mat/'+i)

    return


def main():
    global INDIR, IGNORE, inprefix
    global ROOT, SRC, DST
    global containers
    ROOT = os.path.dirname(os.path.realpath(__file__))
    SRC = INDIR
    DST = os.path.join(ROOT, OUTDIR)
    inprefix = len(SRC)+1
    containers = {}
    if IGNORE[-1] != '/':
        IGNORE += '/'
    ignore = len(IGNORE)-1

    c = os.path.join(SRC, 'containers.txt')
    for i in open(c):
        _id, path, _type = i.split(',')
        containers[_id.strip()] = (path.strip()[ignore:], _type)

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
            if ext == '.asset':
                _asset(src)
            #if ext == '.png':
            #    _png(src)
            #elif ext == '.mat':
            #    _mat(src)
            #elif ext == '.asset':
            #    _asset(src)

def test():
    m = _yuv(INDIR+'/_/-5468202399702066998.png',
        INDIR+'/_/-7892557579526219953.png',
        INDIR+'/_/2115422073092249201.png')
    ma = _alpha(m, INDIR+'/_/-6566012995429355999.png')
    ma.save('test.png')

if __name__ == '__main__':
    main()
