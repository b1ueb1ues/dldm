## config ######################################################
INDIR = 'assets'
OUTDIR = 'out_attr'
TYPE_FILTER = ['GameObject', 'MonoBehaviour']
PATH_FILTER = ['action', 'master']
EXTRACT_OBJECT = True
PREFIX = 'assets/_gluonresources/resources/'

################################################################
import os
from UnityPy import AssetsManager
from collections import Counter


def asset_filter(path):
    if PREFIX in path:
        p = path.replace(PREFIX, '')
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
            export_obj(obj, asset_path)

def export_obj(obj, asset_path):
    # filter { ##########
    if TYPE_FILTER and obj.type not in TYPE_FILTER:
        return
    af = asset_filter(asset_path)
    if not af:
        return
    # filter } ##########

    #print(asset_path)
    fpname = os.path.join(DST, af)
    os.makedirs(os.path.dirname(fpname), exist_ok=True)
    if 0:
        pass
    elif obj.type == 'GameObject':
        gameobject(obj, fpname)
    elif obj.type == 'MonoBehaviour':
        monobehaviour(obj, fpname)

def monobehaviour(obj, fpname):
    f = open(fpname, 'a')
    f.write('%s\n++++++++++++++++++++\n'%obj.path_id)
    data = obj.read()
    f.write('%s\n--------------------\n'%data.path_id)
    f.write(data.dump().replace('\r',''))
    f.write('\n')
    f.close()

def gameobject(obj, fpname):
    f = open(fpname, 'a')
    f.write('%s\n++++++++++++++++++++\n'%obj.path_id)

    go = obj.read()
    cs = go.components
    for i in cs:
        data = i.read()
        f.write('%s\n--------------------\n'%data.path_id)
        f.write(data.dump().replace('\r',''))
        f.write('\n')
    f.close()

ROOT = None
ASSETS = None
DST = None
def main():
    global ROOT
    global ASSETS
    global DST
    ROOT = os.path.dirname(os.path.realpath(__file__))
    ASSETS = os.path.join(ROOT, INDIR)
    DST = os.path.join(ROOT, OUTDIR)
    if 'TYPE_FILTER' not in globals():
        TYPE_FILTER = 0
    if 'PATH_FILTER' not in globals():
        PATH_FILTER = 0

    os.system('rm -r %s'%DST)

    for root, dirs, files in os.walk(ASSETS, topdown=False):
        if '.git' in root:
            continue
        print(root)
        for f in files:
            src = os.path.realpath(os.path.join(root, f))
            _do(src)

if __name__ == '__main__':
    main()
