import os
from UnityPy import AssetsManager


OUTDIR = 'out'
INDIR = 'assets'
FILTER = ['Action','Data','Textlabel', 'Enemy']
OUTDIR = 'out_test'
INDIR = 'assets/GG'


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


def contain(obj):
    global g_containers
    container = obj.assets_file._container
    cid = id(container)
    if cid not in g_containers:
        g_containers[cid] = container


clean()
am = AssetsManager()
am.load_folder(INDIR)

g_containers = {}
scripts = {}

for name, asset in am.assets.items():
    for _id, obj in asset.objects.items():
        contain(obj)
        if obj.type == 'MonoScript':
            #contain(obj)
            data = obj.read()
            dump = data.dump()

            if 0:
                fname = OUTDIR + '/script/' + str(_id)
                print(fname)
                fout = open(fname, 'w')
                dump = dump.replace('\r','')
                fout.write(dump)
                fout.close()

            scripts[_id] = data.class_name


for name, asset in am.assets.items():
    for _id, obj in asset.objects.items():
        if obj.type == 'MonoBehaviour':
            #contain(obj)
            container = obj.assets_file._container
            print('+++++++++++++++')
            print(container)
            print('-',_id)
            print('-obj',obj.path_id)
            print('-data',data.path_id)
            data = obj.read()
            dump = data.dump()
            print(dump)

            if 0:
                name = data.name
                if name != '':
                    fname = OUTDIR + '/behaviour/' + name
                else:
                    fname = OUTDIR + '/behaviour_id/' + str(_id)
            else:
                script_id = data.script.path_id
                if script_id in scripts:
                    #name = scripts[script_id]
                    fname = OUTDIR + '/behaviour/' + scripts[script_id]
                else:
                    #name = str(_id)
                    fname = OUTDIR + '/behaviour_id/' + str(_id)
            for i in FILTER:
                #print(i, fname)
                if i in fname:
                    print(fname)
                    fout = open(fname, 'a')
                    fout.write(str(_id))
                    fout.write('\n++++++++++++\n')
                    dump = dump.replace('\r','')
                    fout.write(dump)
                    fout.write('\n')
                    fout.close()
                    break


out_containers = {}
for k,v in g_containers.items():
    out_containers.update(v)

f = open(OUTDIR+'/container.txt','w')
for k,v in out_containers.items():
    f.write('%s\t %s\n'%(k, v))
f.close()
