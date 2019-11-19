import os
from UnityPy import AssetsManager


outdir = 'out'
indir = 'assets'
#outdir = 'out_test'
#indir = 'assets/ZZ'


def clean():
    global outdir
    global indir
    pwd = os.path.dirname(os.path.abspath(__file__))
    outdir = pwd + '/' + outdir
    indir = pwd + '/' + indir

    cmd = 'rm -r %s'%outdir
    os.system(cmd)
    cmd = 'mkdir %s'%outdir
    cmd += ';mkdir %s/script'%outdir
    cmd += ';mkdir %s/behaviour'%outdir
    cmd += ';mkdir %s/behaviour_id'%outdir
    cmd += ';touch %s/container.txt'%outdir
    os.system(cmd)


def contain(obj):
    global g_containers
    container = obj.assets_file._container
    cid = id(container)
    if cid not in g_containers:
        g_containers[cid] = container


clean()
am = AssetsManager()
am.load_folder(indir)

g_containers = {}
scripts = {}

for name, asset in am.assets.items():
    for _id, obj in asset.objects.items():
        if obj.type == 'MonoScript':
            contain(obj)
            data = obj.read()
            dump = data.dump()

            fname = outdir + '/script/' + str(_id)
            print(fname)
            fout = open(fname, 'w')
            fout.write(dump)
            fout.close()

            scripts[_id] = data.class_name


for name, asset in am.assets.items():
    for _id, obj in asset.objects.items():
        if obj.type == 'MonoBehaviour':
            contain(obj)
            data = obj.read()
            dump = data.dump()

            name = data.name
            if name != '':
                fname = outdir + '/behaviour/' + name
            else:
                fname = outdir + '/behaviour_id/' + str(_id)

            #script_id = data.script.path_id
            #if script_id in scripts:
            #    fname = outdir + '/behaviour/' + scripts[script_id]
            #else:
            #    fname = outdir + '/behaviour/' + str(_id)
            print(fname)
            fout = open(fname, 'w')
            fout.write(dump)
            fout.close()


out_containers = {}
for k,v in g_containers.items():
    out_containers.update(v)

f = open(outdir+'/container.txt','w')
for k,v in out_containers.items():
    f.write('%s\t %s\n'%(k, v))
f.close()
