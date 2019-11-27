## config ######################################################
INDIR = 'assets'
OUTDIR = 'out'
TYPE_FILTER = ['GameObject', 'MonoBehaviour']#, 'MonoScript']
DIR_FILTER = ['action','master']


################################################################
import os
from UnityPy import AssetsManager

ROOT = os.path.dirname(os.path.realpath(__file__))
ASSETS = os.path.join(ROOT, INDIR)
DST = os.path.join(ROOT, OUTDIR)

if 'TYPE_FILTER' not in globals():
    TYPE_FILTER = 0
if 'DIR_FILTER' not in globals():
    DIR_FILTER = 0

os.system('rm -r %s'%DST)

def asset_filter(path):
    if 'assets/_gluonresources/resources' in path:
        p = path.replace('assets/_gluonresources/resources/', '')
    else:
        return False
    pick = 0
    if DIR_FILTER:
        for i in DIR_FILTER:
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
            # filter { ##########
            if TYPE_FILTER and obj.type not in TYPE_FILTER:
                continue
            af = asset_filter(asset_path)
            if not af:
                continue
            # filter } ##########

            #print(asset_path)
            fpname = os.path.join(DST, af)
            if 0:
                pass
            elif obj.type == 'GameObject':
                gameobject(obj, fpname)
            elif obj.type == 'MonoBehaviour':
                monobehaviour(obj, fpname)
            elif obj.type == 'MonoScript':
                monoscript(obj, fpname)
#            elif obj.type == 'Texture2D':
#                texture2d(obj, fpname)
            else:
                common(obj, fpname)

#def texture2d(obj, fpname):
#    data = obj.read()
#    print(data.image)
#    exit()

def monoscript(obj, fpname):
    os.makedirs(os.path.dirname(fpname), exist_ok=True)
    f = open(fpname, 'a')
    f.write('%s\n++++++++++++++++++++\n'%obj.path_id)
    data = obj.read()
    f.write('%s\n--------------------\n'%data.path_id)
    f.write(data.dump().replace('\r',''))
    f.write('\n')
    f.close()

def monobehaviour(obj, fpname):
    os.makedirs(os.path.dirname(fpname), exist_ok=True)
    f = open(fpname, 'a')
    f.write('%s\n++++++++++++++++++++\n'%obj.path_id)
    data = obj.read()
    f.write('%s\n--------------------\n'%data.path_id)
    f.write(data.dump().replace('\r',''))
    f.write('\n')
    f.close()

def gameobject(obj, fpname):
    os.makedirs(os.path.dirname(fpname), exist_ok=True)
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

def common(obj, fpname):
    try:
        os.makedirs(os.path.dirname(fpname), exist_ok=True)
        data = obj.read()
        f = open(fpname, 'wb')
        f.write(data.get_raw_data())
        f.close()
    except:
        pass

def main():
    for root, dirs, files in os.walk(ASSETS, topdown=False):
        if '.git' in root:
            continue
        print(root)
        for f in files:
            src = os.path.realpath(os.path.join(root, f))
            _do(src)
    

if __name__ == '__main__':
    main()
