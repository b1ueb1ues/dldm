import os
from UnityPy import AssetsManager
from collections import Counter
import zipfile

TYPES = ['MonoScript','MonoBehaviour'] #,'TextAsset']
FILTER = ['resources/master', 'resources/actions']

ROOT = os.path.dirname(os.path.realpath(__file__))

# source folder
ASSETS = os.path.join(ROOT, 'assets')
# destination folder
DST = os.path.join(ROOT, 'extracted')
# number of dirs to ignore
# e.g. IGNOR_DIR_COUNT = 2 will reduce
# 'assets/assetbundles/images/story_picture/small/15.png'
# to
# 'images/story_picture/small/15.png'

IGNOR_DIR_COUNT = 2

os.system('rm -r '+DST)
os.makedirs(DST, exist_ok=True)


def main():
    for root, dirs, files in os.walk(ASSETS, topdown=False):
        print(root)
        if '.git' in root:
            continue
        for f in files:
            #print(f)
            extension = os.path.splitext(f)[1]
            src = os.path.realpath(os.path.join(root, f))

            if extension == ".zip":
                archive = zipfile.ZipFile(src, 'r')
                for zf in archive.namelist():
                    extract_assets(archive.open(zf))
            else:
                extract_assets(src)


def extract_assets(src):
    # load source
    am = AssetsManager(src)

    # iterate over assets
    for asset in am.assets.values():
        # assets without container / internal path will be ignored for now
        if not asset.container:
            continue

        # check which mode we will have to use
        num_cont = sum(1 for obj in asset.container.values() if obj.type in TYPES)
        num_objs = sum(1 for obj in asset.objects.values() if obj.type in TYPES)

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
            local_path = os.path.join(DST, *occurence_count.most_common(1)[0][0].split('/')[IGNOR_DIR_COUNT:])

            for obj in asset.objects.values():
                if obj.path_id not in extracted:
                    extracted.extend(export_obj(obj, local_path, append_name=True))



def export_obj(obj, fp: str, append_name: bool = False) -> list:
    global FILTER
    pick = 0
    for i in FILTER:
        if i in fp:
            pick = 1
    if not pick:
        return []
    if obj.type not in TYPES:
        return []
    data = obj.read()
    if append_name:
        fp = os.path.join(fp, data.name)

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
    return [obj.path_id]


def monobehaviour(data, obj, fp, extension):
    if not extension:
        extension = '.txt'
    if data.name == '':
        fp += '_'
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
