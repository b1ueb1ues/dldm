# config ######################################################################
OUTDIR = 'out/img_c'
INDIR = 'chara'


###############################################################################
import os
from PIL import Image

size = None

def alpha(m, a):
    global size
    (r,g,b) = m.split()
    s = Image.open(a).resize(size, Image.LANCZOS).split()
    if len(s) == 4:
        a = s[3]
    elif len(s) == 3:
        a = s[0]
    else:
        raise
    merged = Image.merge("RGBA", (r,g,b,a))
    return merged


def yuv(y, cb, cr):
    global size
    tmp = Image.open(y)
    size = tmp.size
    (z,z,z,y) = tmp.convert('RGBA').split()
    u = Image.open(cb).convert('L').resize(size, Image.LANCZOS)
    v = Image.open(cr).convert('L').resize(size, Image.LANCZOS)
    merged = Image.merge("YCbCr", (y,u,v)).convert('RGB')
    return merged

    #if os.path.exists(alpha_file_name):
    #    #(r,g,b,z) = Image.open(fname).convert('RGBA').split()
    #else:
    #    if DST:
    #        fname = DST+'/'+base_file_name[inprefix:]+"_rgb.png"
    #    else:
    #        fname = base_file_name+"_rgb.png"
    #os.makedirs(os.path.dirname(fname), exist_ok=True)
    #merged.save(fname)


def png(src, ext):
    global DST
    pass

def asset(src, ext):
    global DST
    pass

def mat(src, ext):
    global DST
    pass

def main():
    global OUTDIR, INDIR
    global SRC, DST
    global inprefix
    if 'OUTDIR' not in globals():
        OUTDIR = None
    if 'INDIR' not in globals():
        INDIR = None
    ROOT = os.path.dirname(os.path.realpath(__file__))
    SRC = INDIR
    DST = os.path.join(ROOT, OUTDIR)
    inprefix = len(SRC)+1

    for root, dirs, files in os.walk(SRC, topdown=False):
        #print(root)
        if '.git' in root:
            continue
        for f in files:
            ext = os.path.splitext(f)[1]
            src = os.path.join(root, f)
            if extension == '.png':
                png(src, ext)
            if extension == '.asset':
                asset(src, ext)
            if extension == '.mat':
                mat(src, ext)


