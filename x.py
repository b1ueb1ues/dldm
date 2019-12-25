## config ######################################################
INDIR = 'assets'
OUTDIR = 'out/x'
#TYPE_FILTER = ['GameObject', 'MonoBehaviour']
#PATH_FILTER = ['actions', 'master']
#PREFIX = 'assets/_gluonresources/resources/'
PREFIX = 'assets/_gluonresources/'
CLEAN = False
RENAME = True

DEBUG = 0
################################################################
import os, sys
from UnityPy import AssetsManager
from collections import Counter


def clean(dst):
    os.system('rm -r %s'%dst)

def dprint(*args):
    if DEBUG:
        print(*args)

g_containers = ''
def contain(obj, asset_path):
    global g_containers
    line = '%20d, %s, %s\n'%(obj.path_id, asset_path, obj.type)
    g_containers += line

def asset_filter(path, otype):
    global PREFIX, PREFIXLEN
    global TYPE_FILTER, PATH_FILTER
    path = path.lower()
    if TYPE_FILTER and otype not in TYPE_FILTER:
        return False
    if path.find(PREFIX) == 0:
        p = path[PREFIXLEN:]
    else:
        return False
    pick = 0
    if PATH_FILTER:
        for i in PATH_FILTER:
            if p.find(i) == 0:
                pick = 1
    else:
        pick = 1
    if pick:
        return p
    else:
        return False

def _do(src):
    global g_containers
    am = AssetsManager(src)
    for asset in am.assets.values():
        for asset_path, obj in asset.container.items():
            contain(obj, asset_path)
            if not obj.path_id:
                af = obj.assets_file
                for o in af.objects.values():
                    #name = o.read().name
                    name = o.read().name.split('/')[-1]
                    if name:
                        path = asset_path + '/' + name
                    else:
                        path = asset_path + '/' + '_'
                    export_obj(o, path)
                continue
            export_obj(obj, asset_path)

def export_obj(obj, asset_path):
    # filter { ##########
    af = asset_filter(asset_path, obj.type)
    if not af:
        return
    # filter } ##########

    dprint(asset_path)
    fpname = os.path.join(DST, af)
    os.makedirs(os.path.dirname(fpname), exist_ok=True)
    if 0:
        pass
    elif obj.type == 'GameObject':
        gameobject(obj, fpname)
    elif obj.type == 'Material':
        material(obj, fpname)
    elif obj.type == 'AnimatorOverrideController':
        aoc(obj, fpname)

    elif obj.type == 'MonoBehaviour':
        monobehaviour(obj, fpname)
    elif obj.type == 'MonoScript':
        monoscript(obj, fpname)
    elif obj.type == 'TextAsset':
        textasset(obj, fpname)
    elif obj.type == 'Texture2D':
        texture2d(obj, fpname)
    elif obj.type == 'Sprite':
        sprite(obj, fpname)
    else:
        common(obj, fpname)

# ------------------------------------------
def common(obj, fpname):
    data = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.txt'
    fpname = basename + ext
    while os.path.exists(fpname):
        basename += '.1'
        fpname = basename + ext
    f = open(fpname, 'w')
    f.write('%s\r\n====================\r\n'%obj.path_id)
    f.write(data.dump())
    f.close()
    #fb = open(fpname+'.bin', 'wb')
    #fb.write(data.get_raw_data())
    #fb.close()

def gameobject(obj, fpname):
    go = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.gameobject'
    fpname = basename + ext
    while os.path.exists(fpname):
        basename += '.1'
        fpname = basename + ext
    f = open(fpname, 'w')
    f.write('%s\r\n====================\r\n'%obj.path_id)
    cs = go.components
    for i in cs:
        data = i.read()
        f.write('%s\r\n--------------------\r\n'%data.path_id)
        f.write(data.dump())
        f.write('\r\n')
    f.close()

def material(obj, fpname):
    data = obj.read()
    tts = data.m_SavedProperties.m_TexEnvs
    for k, i in tts.items():
        if 'm_Texture' in dir(i):
            if i.m_Texture.type == 'Texture2D':
                innername = i.m_Texture.read().name
                os.makedirs(fpname, exist_ok=True)
                texture2d(i.m_Texture, fpname+'/'+innername)

def aoc(obj, fpname):
    data = obj.read()
    clips = data.clips
    for o in data.assets_file.objects.values():
        os.makedirs(fpname, exist_ok=True)
        d = o.read()
        if d.name and d.name != '' :
            innername = d.name
        else:
            innername = str(o.path_id)

        if o.type == 'AnimatorOverrideController':
            common(o, fpname+'/'+innername)
        elif o.type == 'AnimationClip':
            common(o, fpname+'/'+innername+'.anim')
        elif o.type == 'AssetBundle':
            continue
        else:
            common(o, fpname+'/'+innername)

def monobehaviour(obj, fpname):
    data = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.monobehaviour'
    fpname = basename + ext
    while os.path.exists(fpname):
        basename += '.1'
        fpname = basename + ext
    f = open(fpname, 'w')
    f.write('%s\r\n====================\r\n'%obj.path_id)
    f.write('%s\r\n--------------------\r\n'%data.path_id)
    f.write(data.dump())
    f.write('\r\n')
    f.close()

def monoscript(obj, fpname):
    data = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.monoscript'
    fpname = basename + ext
    while os.path.exists(fpname):
        basename += '.1'
        fpname = basename + ext
    f = open(fpname, 'w')
    f.write('%s\r\n====================\r\n'%obj.path_id)
    f.write('%s\r\n--------------------\r\n'%data.path_id)
    f.write(data.dump())
    f.write('\r\n')
    f.close()

def textasset(obj, fpname):
    data = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.textasset'
    fpname = basename + ext
    while os.path.exists(fpname):
        basename += '.1'
        fpname = basename + ext
    f = open(fpname, 'wb')
    f.write(data.script)
    f.close()

def sprite(obj, fpname):
    global CLEAN
    data = obj.read()
    basename, extension = os.path.splitext(fpname)
    fpname = basename+'.png'
    while os.path.exists(fpname):
        if not CLEAN:
            return
        basename += '.1'
        fpname = basename+'.png'
    data.image.save(fpname)

def texture2d(obj, fpname):
    global CLEAN
    data = obj.read()
    basename, extension = os.path.splitext(fpname)
    fpname = basename+'.png'
    while os.path.exists(fpname):
        if not CLEAN:
            return
        basename += '.1'
        fpname = basename+'.png'
    try:
        data.image.save(fpname)
    except EOFError:
        pass


def main():
    global INDIR, OUTDIR
    global ROOT, ASSETS, DST
    global TYPE_FILTER, PATH_FILTER
    global PREFIX
    global PREFIXLEN
    global CLEAN

    if len(sys.argv) == 2:
        INDIR = sys.argv[1]

    ROOT = os.path.dirname(os.path.realpath(__file__))
    ASSETS = os.path.join(ROOT, INDIR)
    DST = os.path.join(ROOT, OUTDIR)
    if 'TYPE_FILTER' not in globals():
        TYPE_FILTER = 0
    if 'PATH_FILTER' not in globals():
        PATH_FILTER = 0
    if PREFIX[-1] != '/':
        PREFIX += '/'
    PREFIXLEN = len(PREFIX)

    if CLEAN:
        clean(DST)
    if RENAME:
        count = 0
        base = DST
        while os.path.exists(DST):
            DST = base + '.%d'%count
            count += 1

    for root, dirs, files in os.walk(ASSETS, topdown=False):
        if '.git' in root:
            continue
        print(root)
        for f in files:
            src = os.path.realpath(os.path.join(root, f))
            _do(src)

    ct = os.path.join(DST, 'containers.txt')
    f_containers = open(ct, 'w')
    f_containers.write(g_containers)
    f_containers.close()


if __name__ == '__main__':
    main()
