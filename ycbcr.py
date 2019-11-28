# config ######################################################################
OUTDIR = 'out_ycbcr'
INDIR = 'unitdetail'

###############################################################################
import os
from PIL import Image

#size = (512,512)
size = (1024,1024)
base_file_name = "unitdetail/amulet/400002_01/400002_01"


extracted = {}
def ycbcr(base_file_name, size=(1024, 1024)):
    global inprefix
    if base_file_name in extracted:
        return
    extracted[base_file_name] = 1

    global DST
    if os.path.exists(base_file_name+"_Y.png"):
        (z,z,z,y) = Image.open(base_file_name + "_Y.png").convert('RGBA').split()
    elif os.path.exists(base_file_name+"_y.png"):
        (z,z,z,y) = Image.open(base_file_name + "_y.png").convert('RGBA').split()
    else:
        return
    if os.path.exists(base_file_name+"_Cb.png"):
        u = Image.open(base_file_name + "_Cb.png").convert('L').resize(size, Image.LANCZOS)
    elif os.path.exists(base_file_name+"_cb.png"):
        u = Image.open(base_file_name + "_cb.png").convert('L').resize(size, Image.LANCZOS)
    else:
        return
    if os.path.exists(base_file_name+"_Cr.png"):
        v = Image.open(base_file_name + "_Cr.png").convert('L').resize(size, Image.LANCZOS)
    elif os.path.exists(base_file_name+"_cr.png"):
        v = Image.open(base_file_name + "_cr.png").convert('L').resize(size, Image.LANCZOS)
    else:
        return

    merged = Image.merge("YCbCr", (y,u,v)).convert('RGB')
    if DST:
        fname = DST+'/'+base_file_name[inprefix:]+"_rgb.png"
        os.makedirs(os.path.dirname(fname), exist_ok=True)
    else:
        fname = base_file_name+"_rgb.png"
    merged.save(fname)

    alpha_file_name = base_file_name + "_alpha.png"
    if os.path.exists(alpha_file_name):
        (r,g,b,z) = Image.open(fname).convert('RGBA').split()
        s = Image.open(alpha_file_name).resize(size, Image.LANCZOS).split()
        if len(s) == 4:
            a = s[3]
        elif len(s) == 3:
            a = s[0]
        else:
            raise
        merged = Image.merge("RGBA", (r,g,b,a))
        if DST:
            fname = DST+'/'+base_file_name[inprefix:]+"_rgba.png"
        else:
            fname = base_file_name+"_rgba.png"
        merged.save(fname)


def main():
    global OUTDIR, INDIR
    global SRC, DST
    global inprefix
    if 'OUTDIR' not in globals():
        OUTDIR = None
    if 'INDIR' not in globals():
        INDIR = None
    ROOT = os.path.dirname(os.path.realpath(__file__))
    #SRC = os.path.join(ROOT, INDIR)
    SRC = INDIR
    DST = os.path.join(ROOT, OUTDIR)
    inprefix = len(SRC)+1

    for root, dirs, files in os.walk(SRC, topdown=False):
        #print(root)
        if '.git' in root:
            continue
        for f in files:
            extension = os.path.splitext(f)[1]
            #src = os.path.realpath(os.path.join(root, f))
            src = os.path.join(root, f)
            if extension == '.png':
                e = src.rfind('_')
                bfn = src[:e]
                print(bfn)
                ycbcr(bfn)

if __name__ == "__main__":
    main()
    #ycbcr(base_file_name, size)

