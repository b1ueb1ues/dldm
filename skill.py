import x

x.INDIR = 'assets'
x.OUTDIR = 'out/skill'
x.CLEAN = True
x.RENAME = False
x.TYPE_FILTER = ['GameObject', 'MonoBehaviour']
x.TYPE_FILTER += ['AnimationClip', 'AnimatorOverrideController']

x.PATH_FILTER = ['resources/characters/motion', 'meshes/characters', 'resources/master']
x.PATH_FILTER += ['resources/actions/playeraction/state']
x.PATH_FILTER += ['resources/actions/playeraction/cmn']
x.PATH_FILTER += ['resources/actions/playeraction/axe']
x.PATH_FILTER += ['resources/actions/playeraction/bow']
x.PATH_FILTER += ['resources/actions/playeraction/can']
x.PATH_FILTER += ['resources/actions/playeraction/dag']
x.PATH_FILTER += ['resources/actions/playeraction/kat']
x.PATH_FILTER += ['resources/actions/playeraction/lan']
x.PATH_FILTER += ['resources/actions/playeraction/rod']
x.PATH_FILTER += ['resources/actions/playeraction/swd']
x.PATH_FILTER += ['resources/actions/playeraction/gun']

x.PREFIX = 'assets/_gluonresources/'

x.main()

