# config ######################################################################

#TYPE_FILTER = ['Sprite', 'Texture2D', 'MonoScript', 'GameObject']
#PATH_FILTER = ['resources']
IGNOR_DIR_COUNT = 2
INDIR = 'assets'
OUTDIR = 'abc'

DEBUG = 1

###############################################################################
import os
from UnityPy import AssetsManager
from collections import Counter

def dprint(*args):
    if DEBUG:
        print(*args)

g_containers = ''
def contain(container):
    global g_containers
    for k, v in container.items():
        line = '%s\t %s\n'%(v.path_id, k)
        g_containers += line

def clean(dst):
    os.system('rm -r '+dst)
    os.makedirs(dst, exist_ok=True)

def main():
    global INDIR, OUTDIR
    global TYPE_FILTER, PATH_FILTER, IGNOR_DIR_COUNT
    global ROOT, ASSETS, DST
    global g_containers
    ROOT = os.path.dirname(os.path.realpath(__file__))
    ASSETS = os.path.join(ROOT, INDIR)
    DST = os.path.join(ROOT, OUTDIR)

    if 'TYPE_FILTER' not in globals():
        TYPE_FILTER = None
    if 'PATH_FILTER' not in globals():
        PATH_FILTER = None

    clean(DST)

    for root, dirs, files in os.walk(ASSETS, topdown=False):
        print(root)
        if '.git' in root:
            continue
        for f in files:
            extension = os.path.splitext(f)[1]
            src = os.path.realpath(os.path.join(root, f))
            extract_assets(src)

    ct = os.path.join(DST, 'containers.txt')
    f_containers = open(ct, 'w')
    f_containers.write(g_containers)
    f_containers.close()


def extract_assets(src):
    global DST
    # load source
    am = AssetsManager(src)

    # iterate over assets
    for asset in am.assets.values():
        # assets without container / internal path will be ignored for now
        if not asset.container:
            continue
        else:
            contain(asset.container)

        # check which mode we will have to use
        if TYPE_FILTER:
            num_cont = sum( 1 for obj in asset.container.values() if obj.type in TYPE_FILTER)
            num_objs = sum( 1 for obj in asset.objects.values() if obj.type in TYPE_FILTER)
        else:
            num_cont = sum( 1 for obj in asset.container.values() )
            num_objs = sum( 1 for obj in asset.objects.values() )

        # check if container contains all important assets, if yes, just ignore the container
        if num_objs <= num_cont * 2:
            for asset_path, obj in asset.container.items():
                fp = os.path.join(DST, *asset_path.split('/')[IGNOR_DIR_COUNT:])
                export_obj(obj, fp)
        # otherwise use the container to generate a path for the normal objects
        else:
            extracted = []
            # find the most common path
            occurence_count = Counter(os.path.splitext(asset_path)[0] for asset_path in asset.container.keys())
            for i in asset.container.keys():
                if 'master' in i :
                    print(occurence_count)
                    exit()
            local_path = os.path.join(DST, *occurence_count.most_common(1)[0][0].split('/')[IGNOR_DIR_COUNT:])

            for obj in asset.objects.values():
                if obj.path_id not in extracted:
                    extracted.extend(export_obj(obj, local_path, append_name=True))

def filter(path, otype):
    global TYPE_FILTER
    global PATH_FILTER
    pick = 0
    if PATH_FILTER:
        for i in PATH_FILTER:
            if i in path:
                pick = 1
    else:
        pick = 1
    if TYPE_FILTER and otype not in TYPE_FILTER:
        pick *= 0
    return pick


def export_obj(obj, fp: str, append_name: bool = False) -> list:
    if not filter(fp, obj.type):
        return []
    #if obj.type in ['Material', 'Shader']: # bugged
    #if obj.type in ['MeshFilter', 'Mesh', 'Material']: # bugged
        #return []
    data = obj.read()
    if data.name :
        slash = data.name.rfind('/')
        if slash != -1:
            aname = data.name[slash+1:]
        else:
            aname = data.name
        if aname == '':
            aname = '_'
    else :
        aname = '_'

    if append_name:
        bname = aname.encode('utf8')
        if len(bname) > 200:
            aname = aname[:50]
        fp = os.path.join(fp, aname)
    #dprint('aname', aname)
    #dprint('fp', fp)

    #dprint(str(obj.type)+':'+fp)
    fp, extension = os.path.splitext(fp)
    os.makedirs(os.path.dirname(fp), exist_ok=True)

    if 0 :
        pass
    elif obj.type == 'MonoScript':
        return monoscript(data, obj, fp, extension)
    elif obj.type == 'MonoBehaviour':
        return monobehaviour(data, obj, fp, extension)
    elif obj.type == 'TextAsset':
        return textasset(data, obj, fp, extension)
    elif obj.type == "Sprite":
        return sprite(data, obj, fp, extension)
    elif obj.type == "Texture2D":
        return texture2d(data, obj, fp, extension)
    elif obj.type == "GameObject":
        return gameobject(data, obj, fp, extension)
    else:
        return common(data, obj, fp, extension)
    return [obj.path_id]


def common(data, obj, fp, extension):
    return []
    f = open(f"{fp}.txt", 'w')
    #fb = open(f"{fp}.bin", 'wb')
    f.write(data.dump())
    #fb.write(data.get_raw_data())
    return [obj.path_id]

def gameobject(data, obj, fp, extension):
    fp += '.go.txt'
    with open(f"{fp}", 'a') as f:
        f.write('%s\n++++++++++++++++++++\n'%obj.path_id)
        go = obj.read()
        cs = go.components
        for i in cs:
            data = i.read()
            f.write('%s\n--------------------\n'%data.path_id)
            f.write(data.dump().replace('\r',''))
            f.write('\n')
        f.close()
    return [obj.path_id]

def monobehaviour(data, obj, fp, extension):
    if not extension:
        extension = '.txt'
    if data.name == '':
        return []
    with open(f"{fp}{extension}", 'a') as f:
        f.write(str(obj.path_id))
        f.write('\n+++++++++++++++\n')
        f.write(data.dump().replace('\r',''))
    return [obj.path_id]

def monoscript(data, obj, fp, extension):
    if not extension:
        extension = '.txt'
    with open(f"{fp}{extension}", 'w') as f:
        f.write(str(obj.path_id))
        f.write('\n+++++++++++++++\n')
        f.write(data.dump().replace('\r',''))
    return [obj.path_id]

def textasset(data, obj, fp, extension):
    if not extension:
        extension = '.txt'
    with open(f"{fp}{extension}", 'wb') as f:
        f.write(data.script)
    return [obj.path_id]

def sprite(data, obj, fp, extension):
    extension = ".png"
    data.image.save(f"{fp}{extension}")
    return [obj.path_id, data.m_RD.texture.path_id, getattr(data.m_RD.alphaTexture, 'path_id', None)]

def texture2d(data, obj, fp, extension):
    extension = ".png"
    fp = f"{fp}{extension}"
    if not os.path.exists(fp):
        try:
            data.image.save(fp)
        except EOFError:
            pass
    return [obj.path_id]


if __name__ == '__main__':
    main()
