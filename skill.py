import x

x.INDIR = 'assets'
x.OUTDIR = 'out/skill'
x.TYPE_FILTER = ['GameObject', 'MonoBehaviour']
x.TYPE_FILTER += ['AnimationClip', 'AnimatorOverrideController']
x.PATH_FILTER = ['resources/actions/playeraction', 'resources/master']
x.PATH_FILTER += ['resources/characters/motion', 'meshes/characters']
x.PREFIX = 'assets/_gluonresources/'

x.main()

