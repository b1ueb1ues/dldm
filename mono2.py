import os
from UnityPy import AssetsManager


OUTDIR = 'out'
INDIR = 'assets'
FILTER = ['Action','Data','Textlabel', 'Enemy']
#OUTDIR = 'out_test'
#INDIR = 'assets/GG'


def clean():
    global OUTDIR
    global INDIR
    global FILTER
    pwd = os.path.dirname(os.path.abspath(__file__))
    OUTDIR = pwd + '/' + OUTDIR
    INDIR = pwd + '/' + INDIR

    cmd = 'rm -r %s'%OUTDIR
    os.system(cmd)
    cmd = 'mkdir %s'%OUTDIR
    #cmd += ';mkdir %s/script'%OUTDIR
    cmd += ';mkdir %s/behaviour'%OUTDIR
    if not FILTER:
        cmd += ';mkdir %s/behaviour_id'%OUTDIR
    cmd += ';touch %s/container.txt'%OUTDIR
    os.system(cmd)





g_containers = {}
def contain(container):
    global g_containers
    cid = id(container)
    if cid not in g_containers:
        g_containers[cid] = container
    else:
        raise

def get_containers(src):
    am = AssetsManager(src)
    for asset in am.assets.values():
        contain(asset.container)

def save_containers():
    global g_containers
    out_containers = {}
    for k,v in g_containers.items():
        out_containers.update(v)

    f = open(OUTDIR+'/container.txt','w')
    for k,v in out_containers.items():
        f.write('%s\t %s\n'%(k, v))
    f.close()



def main():
    for root, dirs, files in os.walk(INDIR, topdown=False):
        if '.git' in root:
            continue
        print(root)
        for f in files:
            src = os.path.realpath(os.path.join(root, f))
            get_containers(src)
    save_containers()

    

if __name__ == '__main__':
    main()
