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
c.OUDIR = 'out/img_combined'
#c.LOOSE = True
c.main()
