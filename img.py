import x, c

x.INDIR = 'assets'
x.OUTDIR = 'out/img'
x.TYPE_FILTER = ['Texture2D', 'Sprite','Material','MonoBehaviour']
#x.PATH_FILTER = []
x.PREFIX = 'assets/_gluonresources/'
x.CLEAN = False
x.RENAME = True
x.main()

c.INDIR = x.DST
c.OUTDIR = 'out/img_combined'
#c.LOOSE = True #save all pictures in one base dir, use filename to represent path
#c.CLEAN = True # clean output dir before combine
#c.RENAME = True # append output dir with number when path exists
c.main()
