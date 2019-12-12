# config ######################################################################
OUTDIR = 'out/alphaa8'
INDIR = 'out/icon'

###############################################################################
import os
from PIL import Image

#size = (512,512)
size = (1024,1024)
base_file_name = "icon/amulet/l/400001_01"


extracted = {}
def alphaa8(base_file_name, size=(1024, 1024)):
    global inprefix
    global DST
    if base_file_name in extracted:
        return
    extracted[base_file_name] = 1

    fname = base_file_name + ".png"
    alpha_file_name = base_file_name + "_alphaa8.png"
    if not os.path.exists(alpha_file_name):
        alpha_file_name = base_file_name + "_alphaA8.png"
    if not os.path.exists(alpha_file_name):
        return

    basedir = os.path.dirname(base_file_name)
    if os.path.splitext(basedir)[1] == '.mat':
        base_file_name = basedir[:-4]

    if os.path.exists(alpha_file_name):
        print(base_file_name)
        b = Image.open(fname)
        size = b.size
        (r,g,b,z) = b.convert('RGBA').split()
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
        os.makedirs(os.path.dirname(fname), exist_ok=True)
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
                bfn = src[:src.rfind('.png')]
                alphaa8(bfn)

if __name__ == "__main__":
    main()
    #alphaa8(base_file_name, size)

