from lib import x

x.INDIR = 'assets'
x.OUTDIR = 'out/anim'
x.TYPE_FILTER = ['AnimationClip', 'AnimatorOverrideController']
x.PATH_FILTER = ['resources/characters', 'meshes']
x.PREFIX = 'assets/_gluonresources/'

x.main()

