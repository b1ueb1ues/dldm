import x, c

x.INDIR = 'assets'
x.OUTDIR = 'out/img'
x.TYPE_FILTER = ['Texture2D', 'Sprite','Material','MonoBehaviour']
#x.PATH_FILTER = []
x.PREFIX = 'assets/_gluonresources/'
x.CLEAN = False
x.RENAME = True
x.main()

c.OUTDIR = 'out/img_combined'
c.LOOSE = 2 # 0: use full path, 1: save all pictures in out dir, use filename to represent path, 2: make full path a single dir under out dir
#c.CLEAN = True # clean output dir before combine
c.RENAME = True # append output dir with number when path exists
c.INDIR = x.DST # don't change this
c.main()
