from lib import x

x.INDIR = 'assets'
x.OUTDIR = 'out/mono'
x.TYPE_FILTER = ['GameObject', 'MonoBehaviour']
x.PATH_FILTER = ['actions', 'master','aiscript']
x.PREFIX = 'assets/_gluonresources/resources/'

x.main()

