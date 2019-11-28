## config ######################################################
INDIR = 'assets'
OUTDIR = 'out_y'
#TYPE_FILTER = ['GameObject', 'MonoBehaviour']
#PATH_FILTER = ['action', 'master']
#PREFIX = 'assets/_gluonresources/resources/'
PREFIX = 'assets/_gluonresources/'

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
    elif obj.type == 'Material':
        material(obj, fpname)

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


def gameobject(obj, fpname):
    extension = os.path.splitext(fpname)[1]
    if not extension:
        fpname += '.txt'
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

def material(obj, fpname):
    data = obj.read()
    tts = data.m_SavedProperties.m_TexEnvs
    for k, i in tts.items():
        if 'm_Texture' in dir(i):
            if i.m_Texture.type == 'Texture2D':
                innername = i.m_Texture.read().name
                os.makedirs(fpname, exist_ok=True)
                texture2d(i.m_Texture, fpname+'/'+innername)
        if 'm_Sprite' in dir(i):
            print(1)
            exit()


def monobehaviour(obj, fpname):
    extension = os.path.splitext(fpname)[1]
    if not extension:
        fpname += '.txt'
    f = open(fpname, 'a')
    f.write('%s\n++++++++++++++++++++\n'%obj.path_id)
    data = obj.read()
    f.write('%s\n--------------------\n'%data.path_id)
    f.write(data.dump().replace('\r',''))
    f.write('\n')
    f.close()

def monoscript(obj, fpname):
    extension = os.path.splitext(fpname)[1]
    if not extension:
        fpname += '.txt'
    f = open(fpname, 'a')
    f.write('%s\n++++++++++++++++++++\n'%obj.path_id)
    data = obj.read()
    f.write('%s\n--------------------\n'%data.path_id)
    f.write(data.dump().replace('\r',''))
    f.write('\n')
    f.close()

def textasset(obj, fpname):
    extension = os.path.splitext(fpname)[1]
    if not extension:
        fpname += '.txt'
    data = obj.read()
    f = open(fpname, 'wb')
    f.write(data.script)

def sprite(obj, fpname):
    data = obj.read()
    #extension = os.path.splitext(fpname)[1]
    #if not extension:
    fpname += '.png'
    data.image.save(fpname)

def texture2d(obj, fpname):
    data = obj.read()
    #extension = os.path.splitext(fpname)[1]
    #if not extension:
    fpname += '.png'
    if not os.path.exists(fpname):
        try:
            data.image.save(fpname)
        except EOFError:
            pass


def main():
    global ROOT, ASSETS, DST
    global TYPE_FILTER, PATH_FILTER
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
