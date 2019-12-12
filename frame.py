# config ######################################################################
ACTIONSDIR = 'out/mono/actions'
ANIMATION = 'out/anim/meshes/characters/motion/animationclips'
OVERRIDE = 'out/anim/resources/characters/motion'
SKILLDATA = 'out/mono/master/skilldata.asset'
CHARADATA = 'out/mono/master/charadata.asset'
TEXTLABEL = 'out/mono/master/textlabel.asset'

TEXTLABEL = 'TextLabel.txt'

###############################################################################
import os
import re

aidframe = {}
aidlabel = {}
def aid2frame(fname):
    global aidframe, aidlabel
    aid = re.findall(r'playeraction_(\d+).*', fname)
    if len(aid) == 1:
        aid = int(aid[0])
    else:
        return
    data = open(fname).read()
    pmds = re.findall(r'PartsMotionData _data\n.*?\n\n', data, re.DOTALL)
    label = []
    for i in pmds:
        _seconds = re.findall(r'float _seconds = (.*)\n', i)[0]
        _speed = re.findall(r'float _speed = (.*)\n', i)[0]
        ms = re.findall(r'string _motionState = "(.*)"\n', i)[0]
        label.append((ms, _seconds, _speed))
    r = re.findall(r'commandType = 15\n.*float _seconds = (.+)\n.*float _speed = (.*)\n', data)
    if len(label) >= 1:
        aidlabel[aid] = label
    if len(r) >= 1:
        _seconds, _speed = r[0]
        #duration = float(_seconds)*float(_speed)  
        duration = float(_seconds)
        frame = int(duration*60+0.01)
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
idid = {}
def cid2name():
    global idchara, idcomment, idid
    data = open(TEXTLABEL).read()
    tmp = re.findall(r'CHARA_NAME_(\d+)"\n.*_Text = "(.*)"', data)
    for i in tmp:
        idname[i[0]] = i[1]
    tmp = re.findall(r'CHARA_NAME_COMMENT_(\d+)"\n.*_Text = "(.*)"', data)
    for i in tmp:
        idcomment[i[0]] = i[1]
        idname[i[0]] = i[1]
    data = open(CHARADATA).read()
    cdes = re.findall(r'CharaDataElement data.*?\n.*?\[\d*\]\n', data, re.DOTALL)
    for i in cdes:
        cid = re.findall(r'int _Id = (\d+)\n', i)[0]
        bid = re.findall(r'int _BaseId = (\d+)\n', i)[0]
        vid = re.findall(r'int _VariationId = (\d+)\n', i)[0]
        idid[cid] = (int(bid), int(vid))

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
                f1.append(_do(cid, i))
        for i in aid2:
            if i:
                f2.append(_do(cid, i))
        print('"%s","%s","%s","%s %s %s"'%(name, f1, f2, cid, aid1, aid2))

def _do(cid, aid):
    global aidframe, idid, labelframe
    if aid in aidframe:
        canceltime = aidframe[aid]
    else:
        canceltime = -1
    if aid in aidlabel:
        labels = aidlabel[aid]
    else:
        labels = [['','0','0']]
    label = labels[-1][0]
    #startframe = float(labels[-1][1]) * float(labels[-1][2])
    startframe = float(labels[-1][1])
    startframe = int(startframe*60+0.01)
    bvid = idid[cid]
    bvid = '%d%02d'%(bvid[0], bvid[1])
    labeltime = -1
    if label in labelframe:
        labeltime = labelframe[label]
    elif 'skill_unique_' in label:
        lid = label.replace('skill_unique_', '')
        aname = 'SKL_'+lid+'_'+bvid
        for l in labelframe:
            if aname in l:
                labeltime = labelframe[l] + startframe
                break
    if canceltime >= 0:
        return canceltime
    else:
        return labeltime






if __name__ == "__main__":
    main()

