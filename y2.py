## config ######################################################
INDIR = 'assets'
OUTDIR = 'out/y'
TYPE_FILTER = ['MonoBehaviour','Texture2D','Sprite', 'Material']
#TYPE_FILTER = ['GameObject', 'MonoBehaviour']
#PATH_FILTER = ['actions', 'master']
#PREFIX = 'assets/_gluonresources/resources/'
PREFIX = 'assets/_gluonresources/'
SUBASSET = True
ALLID = False
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

g_nocontainers = ''
def nocontain(obj):
    global g_nocontainers
    if obj.read:
        name = obj.read().name
    line = '%20d, %s, %s\n'%(obj.path_id, name, obj.type)
    g_nocontainers += line

def asset_filter(path, otype):
    global PREFIX, PREFIXLEN
    global TYPE_FILTER, PATH_FILTER
    path = path.lower()
    if TYPE_FILTER and otype not in TYPE_FILTER:
        return False
    if path.find(PREFIX) == 0:
        p = path[PREFIXLEN:]
    elif path[0:2] == '_/':
        p = path
    elif path[0:3] == '__/':
        p = path
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

def read_tree(_in, _out):
    if type(_in) != dict and type(_in) != list:
        return
    for k, i in _in.items():
        if type(i) == dict:
            read_tree(i, _out)
        elif type(i) == list:
            for l in i:
                read_tree(l, _out)
        elif k=='m_PathID':
            _out[i] = 1


queue = {}
extracted = {}
def read_orig_file(src):
    global g_containers
    global queue, extracted
    am = AssetsManager(src)
    queue = {}
    extracted = {}

    for asset in am.assets.values():
        for o in asset.objects.values():
            dprint(o,o.read().name, o.path_id)
            queue[o.path_id] = o

    for asset in am.assets.values():
        for asset_path, obj in asset.container.items():
            contain(obj, asset_path)
            if obj.path_id:
                export_obj(obj, asset_path, dup=True)
            else:
                dprint('obj no path_id')
                raise
    if ALLID:
        for _id, obj in queue.items():
            if obj:
                nocontain(obj)
                export_obj(obj, '__/'+str(_id))


def export_obj(obj, asset_path, filter=True, dup=False):
    global queue, extracted
    if dup :
        extracted[obj.path_id] = queue[obj.path_id]
    else:
        if queue[obj.path_id]:
            extracted[obj.path_id] = queue[obj.path_id]
            queue[obj.path_id] = None
        else:
            return
    if filter:
        af = asset_filter(asset_path, obj.type)
        if af:
            fpname = os.path.join(DST, af)
        else:
            return
    else:
        fpname = asset_path

    #dprint(asset_path)
    os.makedirs(os.path.dirname(fpname), exist_ok=True)
    if not obj.type:
        pass
    elif obj.type == 'GameObject':
        gameobject(obj, fpname, asset_path)
    elif obj.type == 'Material':
        material(obj, fpname, asset_path)
    elif obj.type == 'MonoBehaviour':
        monobehaviour(obj, fpname, asset_path)
    elif obj.type == 'MonoScript':
        monoscript(obj, fpname, asset_path)
    elif obj.type == 'AnimatorOverrideController':
        aoc(obj, fpname, asset_path)
    elif obj.type == 'TextAsset':
        textasset(obj, fpname, asset_path)
    elif obj.type == 'Texture2D':
        texture2d(obj, fpname, asset_path)
    elif obj.type == 'Sprite':
        sprite(obj, fpname, asset_path)
    else:
        common(obj, fpname, asset_path)

# ------------------------------------------
def common(obj, fpname, asset_path):
    data = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.txt'
    fpname = basename + ext
    count = 0
    while os.path.exists(fpname):
        fpname = basename+'.%d'%count + ext
        count += 1
    f = open(fpname, 'w')
    f.write('====================\r\n%s\r\n'%obj.path_id)
    f.write(data.dump())
    f.close()


def gameobject(obj, fpname, asset_path):
    go = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.gameobject'
    fpname = basename + ext
    count = 0
    while os.path.exists(fpname):
        fpname = basename+'.%d'%count + ext
        count += 1
    f = open(fpname, 'w')
    f.write('====================\r\n%s\r\n'%obj.path_id)
    f.write(go.dump())
    cs = go.components
    for i in cs:
        data = i.read()
        f.write('--------------------\r\n%s\r\n'%data.path_id)
        f.write(data.dump())
        f.write('\r\n')
        #dname = os.path.dirname(asset_path)
        #fname = os.path.basename(asset_path)
        #export_obj(i, '_/%s'%i.path_id )
    f.close()

def material(obj, fpname, asset_path):
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.mat'
    data = obj.read()
    f = open(fpname,'w')
    f.write(data.dump())
    f.close()
    if SUBASSET:
        tt = data.read_type_tree()
        mat = {}
        read_tree(tt, mat)
        dname = os.path.dirname(asset_path)
        fname = os.path.basename(asset_path)
        for i in mat:
            if i in queue:
                obj = queue[i]
                if obj:
                    nocontain(obj)
                    export_obj(obj, '_/%s'%obj.path_id )


def aoc(obj, fpname, asset_path):
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.aoc'
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


def monobehaviour(obj, fpname, asset_path):
    global queue
    data = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.monobehaviour'
    fpname = basename + ext
    count = 0
    while os.path.exists(fpname):
        fpname = basename+'.%d'%count + ext
        count += 1
    f = open(fpname, 'w')
    f.write(data.dump())
    f.write('\r\n')
    f.close()

    if SUBASSET:
        tt = data.read_type_tree()
        mono_content_ids = {}
        read_tree(tt, mono_content_ids)
        dname = os.path.dirname(asset_path)
        fname = os.path.basename(asset_path)
        for i in mono_content_ids:
            if i in queue:
                obj = queue[i]
                if obj:
                    nocontain(obj)
                    export_obj(obj, '_/%s'%obj.path_id )



def monoscript(obj, fpname, asset_path):
    data = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.monoscript'
    fpname = basename + ext
    count = 0
    while os.path.exists(fpname):
        fpname = basename+'.%d'%count + ext
        count += 1
    f = open(fpname, 'w')
    f.write('====================\r\n%s\r\n'%obj.path_id)
    f.write('--------------------\r\n%s\r\n'%data.path_id)
    f.write(data.dump())
    f.write('\r\n')
    f.close()

def textasset(obj, fpname, asset_path):
    data = obj.read()
    basename, ext = os.path.splitext(fpname)
    if not ext:
        ext = '.textasset'
    fpname = basename + ext
    count = 0
    while os.path.exists(fpname):
        fpname = basename+'.%d'%count + ext
        count += 1
    f = open(fpname, 'wb')
    f.write(data.script)
    f.close()

def sprite(obj, fpname, asset_path):
    global CLEAN
    data = obj.read()
    basename, extension = os.path.splitext(fpname)
    ext = '.png'
    fpname = basename+ext
    count = 0
    while os.path.exists(fpname):
        if not CLEAN:
            return
        fpname = basename+'.%d'%count + ext
        count += 1
    data.image.save(fpname)

def texture2d(obj, fpname, asset_path):
    global CLEAN
    data = obj.read()
    basename, extension = os.path.splitext(fpname)
    ext = '.png'
    fpname = basename+ext
    count = 0
    while os.path.exists(fpname):
        if not CLEAN:
            return
        fpname = basename+'.%d'%count + ext
        count += 1
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
            read_orig_file(src)

    ct = os.path.join(DST, 'containers.txt')
    f_containers = open(ct, 'w')
    f_containers.write(g_containers)
    f_containers.close()
    ct = os.path.join(DST, 'nocontainers.txt')
    f_containers = open(ct, 'w')
    f_containers.write(g_nocontainers)
    f_containers.close()


if __name__ == '__main__':
    main()
