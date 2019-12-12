# config ######################################################################
ACTIONSDIR = 'out/mono/actions'
ANIMATION = 'out/anim/meshes/characters/motion/animationclips'
OVERRIDE = 'out/anim/resources/characters/motion'
SKILLDATA = 'out/mono/master/skilldata.asset'
TEXTLABEL = 'out/mono/master/textlabel.asset'
#TEXTLABEL = 'TextLabel.txt'

###############################################################################
import os
import re

aidframe = {}
def aid2frame(fname):
    data = open(fname).read()
    r = re.findall(r'commandType = 15\n.*float _seconds = (.+)\n.*float _speed = (.*)\n', data)
    if len(r) != 1:
        return
    _seconds, _speed = r[0]
    aid = re.findall(r'playeraction_(\d+).*', fname)
    aid = int(aid[0])
    duration = float(_seconds)*float(_speed)
    frame = int(duration*60+0.01)
    #print(aid, frame)
    aidframe[aid] = frame

sa = {}
sae = {}
def sid2aid():
    global SKILLDATA
    global sa, sae
    data = open(SKILLDATA).read()
    sdes = re.findall(r'SkillDataElement data.*?\n.*?\[\d*\]\n', data, re.DOTALL)
    for sde in sdes:
        sid = re.findall(r'int _Id = (\d+)\n', sde)
        aid = re.findall(r'int _ActionId1 = (\d+)\n', sde)
        trans = re.findall(r'int _TransSkill = (\d+)\n', sde)
        sid = int(sid[0])
        aid = int(aid[0])
        trans = int(trans[0])
        sa[sid] = [aid, trans]
    for i in sa:
        aid = sa[i]
        while aid[-1] != 0:
            aid = aid[:-1] + sa[aid[-1]][:]
            if aid[-1] == i:
                aid[-1] = 0
        sae[i] = aid

idname = {}
idcomment = {}
def cid2name():
    global idchara, idcomment
    data = open(TEXTLABEL).read()
    tmp = re.findall(r'CHARA_NAME_(\d+)"\n.*_Text = "(.*)"', data)
    for i in tmp:
        idname[i[0]] = i[1]
    tmp = re.findall(r'CHARA_NAME_COMMENT_(\d+)"\n.*_Text = "(.*)"', data)
    for i in tmp:
        idcomment[i[0]] = i[1]
        idname[i[0]] = i[1]

labelframe = {}
def anim2frame(fname):
    global labelframe
    if os.path.splitext(fname)[1] != '.anim':
        return
    data = open(fname).read()
    name = re.findall(r'name = "(.*)"', data)[0]
    time = re.findall(r'm_StopTime = (.*)', data)[0]
    duration = float(time)
    frame = int(duration*60+0.01)
    labelframe[name] = frame


def main():
    global OUTFILE, ACTIONSDIR
    global SRC, DST
    global idname, sae, aidframe

    cid2name()
    sid2aid()

    ROOT = os.path.dirname(os.path.realpath(__file__))

    SRC = ACTIONSDIR
    for root, dirs, files in os.walk(SRC, topdown=False):
        for f in files:
            aid2frame(root+'/'+f)

    SRC = ANIMATION
    for root, dirs, files in os.walk(SRC, topdown=False):
        for f in files:
            anim2frame(root+'/'+f)

    SRC = OVERRIDE
    for root, dirs, files in os.walk(SRC, topdown=False):
        for f in files:
            anim2frame(root+'/'+f)
    global labelframe
    print(labelframe)
    exit()

    for cid in idname:
        name = idname[cid]
        if cid[:3] == '199':
            continue
        aid1 = sae[int(cid+'1')]
        aid2 = sae[int(cid+'2')]
        f1 = []
        f2 = []
        for i in aid1:
            if i:
                if i in aidframe:
                    f1.append(aidframe[i])
                else:
                    f1.append(-1)
        for i in aid2:
            if i:
                if i in aidframe:
                    f2.append(aidframe[i])
                else:
                    f2.append(-1)
        print('%s,%s,%s,"%s %s %s"'%(name, f1, f2, cid, aid1, aid2))







if __name__ == "__main__":
    main()

