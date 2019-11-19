import os
from UnityPy import AssetsManager

outdir = 'out'

cmd = 'rm -r %s'%outdir
os.system(cmd)
cmd = 'mkdir %s'%outdir
cmd += ';mkdir %s/script'%outdir
cmd += ';mkdir %s/behaviour'%outdir
cmd += ';touch %s/container.txt'%outdir
os.system(cmd)

am = AssetsManager()
am.load_folder('/home/bblues/Downloads/data/data/com.nintendo.zaga/files/assets/')
#am.load_folder('/home/bblues/Downloads/data/data/com.nintendo.zaga/files/assets/ZZ')

g_containers = {}
scripts = {}

def contain(obj):
    global g_containers
    container = obj.assets_file._container
    cid = id(container)
    if cid not in g_containers:
        g_containers[cid] = container


for name, asset in am.assets.items():
    for _id, obj in asset.objects.items():
        if str(obj) == '<ObjectReader MonoScript>':
            contain(obj)
            data = obj.read()
            dump = data.dump()

            fname = outdir + '/script/' + str(_id)
            fout = open(fname, 'w')
            fout.write(dump)
            fout.close()

            scripts[_id] = data.class_name


for name, asset in am.assets.items():
    for _id, obj in asset.objects.items():
        if str(obj) == '<ObjectReader MonoBehaviour>':
            contain(obj)
            data = obj.read()
            dump = data.dump()

            script_id = data.script.path_id
            if script_id in scripts:
                fname = outdir + '/behaviour/' + scripts[script_id]
            else:
                fname = outdir + '/behaviour/' + str(_id)
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
