# config ######################################################################
PREFIX = 'out/skill'

ACTIONSDIR = PREFIX+'/resources/actions'
ANIMATION = PREFIX+'/meshes/characters/motion/animationclips'
OVERRIDE = PREFIX+'/resources/characters/motion'
SKILLDATA = PREFIX+'/resources/master/skilldata.asset'
CHARADATA = PREFIX+'/resources/master/charadata.asset'
TEXTLABEL = PREFIX+'/resources/master/textlabel.asset'
PLAYERACTIONHITATTRIBUTE = PREFIX+'/resources/master/playeractionhitattribute.asset'

#ANIMATION = 'out/anim/'
#OVERRIDE = 'out/anim/'
#TEXTLABEL = 'TextLabel.txt'

###############################################################################
import os
import re
from block import *


hitda = {}
def playeractionhitattribute():
    global hitda
    data = open(PLAYERACTIONHITATTRIBUTE, encoding='utf8').read()
    idda = re.findall(r'string _Id = "(.*?)".*?float _DamageAdjustment = (.*?)\n', data, re.DOTALL)
    for i in idda:
        if i[0] and i[0] != '':
            if i[0] != 'CMN_AVOID':
                hitda[i[0]] = i[1]

aidframe = {}
aidlabel = {}
aidhit = {}
aidhittiming = {}
def playeraction(fname):
    global aidframe, aidlabel
    aid = re.findall(r'playeraction_(\d+).*', fname)
    if len(aid) == 1:
        aid = int(aid[0])
    else:
        return
    f = open(fname, encoding='utf8')
    data = f.read()
    f.seek(0);
    lines = f.readlines()
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
        duration = float(_seconds)*float(_speed)  
        speed = float(_speed)
        #duration = float(_seconds)
        frame = int(duration*60+0.01)
        aidframe[aid] = (frame, speed)

    #hd = re.findall(r'string _hitLabel = "(.*?)"', data, re.DOTALL)
    #hd += re.findall(r'string _hitAttrLabel = "(.*?)"', data, re.DOTALL)
    #aidhit[aid] = hd
    hd = []
    for blockdata in findblock(lines, 'HitData'):
        hd += re.findall(r'float _seconds = ([0-9\.]*)\n.*?string _hitLabel = "(.*?)"', blockdata, re.DOTALL)
    for blockdata in findblock(lines, 'FireStockBulletData'):
        hd += re.findall(r'float _seconds = ([0-9\.]*)\n.*?string _hitAttrLabel = "(.*?)"', blockdata, re.DOTALL)
    for blockdata in findblock(lines, 'BulletData'):
        hd += re.findall(r'float _seconds = ([0-9\.]*)\n.*?string _hitAttrLabel = "(.*?)"', blockdata, re.DOTALL)
    for blockdata in findblock(lines, 'ArrangeBulletData'):
        hd += re.findall(r'float _seconds = ([0-9\.]*)\n.*?string _abHitAttrLabel = "(.*?)"', blockdata, re.DOTALL)
    aidhit[aid] = []
    aidhittiming[aid] = []
    for i in hd:
        aidhittiming[aid].append(i[0])
        aidhit[aid].append(i[1])
#    if int(aid) == 691090:
#        print(aid, hd)
#        exit()
    


sa = {}
sae = {}
ssp = {}
def skilldata():
    global SKILLDATA
    global sa, sae, ssp
    data = open(SKILLDATA, encoding='utf8').read()
    sdes = re.findall(r'SkillDataElement data.*?\n.*?_ZoomWaitTime', data, re.DOTALL)
    for sde in sdes:
        sid = re.findall(r'int _Id = (\d+)\n', sde)
        aid = re.findall(r'int _ActionId1 = (\d+)\n', sde)
        trans = re.findall(r'int _TransSkill = (\d+)\n', sde)
        sp = re.findall(r'int _Sp = (\d+)\n', sde)[0]
        sp2 = re.findall(r'int _SpLv2 = (\d+)\n', sde)[0]
        sid = int(sid[0])
        if sid == 0:
            continue
        aid = int(aid[0])
        trans = int(trans[0])
        ssp[sid] = (sp, sp2)
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
def textlabel():
    global idchara, idcomment, idid
    data = open(TEXTLABEL, encoding='utf8').read()
    tmp = re.findall(r'CHARA_NAME_(\d+)"\n.*_Text = "(.*)"', data)
    for i in tmp:
        idname[i[0]] = i[1]
    tmp = re.findall(r'CHARA_NAME_COMMENT_(\d+)"\n.*_Text = "(.*)"', data)
    for i in tmp:
        idcomment[i[0]] = i[1]
        idname[i[0]] = i[1]
    data = open(CHARADATA, encoding='utf8').read()
    cdes = re.findall(r'CharaDataElement data.*?\n.*?\[\d*\]\n', data, re.DOTALL)
    for i in cdes:
        cid = re.findall(r'int _Id = (\d+)\n', i)[0]
        bid = re.findall(r'int _BaseId = (\d+)\n', i)[0]
        vid = re.findall(r'int _VariationId = (\d+)\n', i)[0]
        idid[cid] = (int(bid), int(vid))

labelframe = {}
labelid = {}
acframe = {}
override = {}
def anim(fname):
    global labelframe, labelid, acframe
    data = open(fname, encoding='utf8').read()
    if 'AnimationClip Base' in data:
        pid = re.findall(r'===\n(.*)\n', data)[0]
        name = re.findall(r'name = "(.*)"', data)[0]
        time = re.findall(r'm_StopTime = (.*)', data)[0]
        duration = float(time)
        frame = int(duration*60+0.01)
        labelframe[name] = frame
        labelid[name] = pid
        acframe[pid] = frame
    elif 'AnimatorOverrideController Base' in data:
        pid = re.findall(r'===\n(.*)\n', data)[0]
        name = re.findall(r'string name = "(.*)"\n', data)[0]
        acos = re.findall(r'AnimationClipOverride data.*?m_OriginalClip.*?m_OverrideClip.*?m_PathID = [0-9\-]+', data, re.DOTALL)
        override[name] = {}
        for i in acos:
            orig = re.findall(r'm_OriginalClip.*?m_PathID = ([0-9\-]*)', i, re.DOTALL)[0]
            over = re.findall(r'm_OverrideClip.*?m_PathID = ([0-9\-]*)', i, re.DOTALL)[0]
            override[name][orig] = over


def main():
    global OUTFILE, ACTIONSDIR
    global SRC, DST
    global idname, sae, aidframe

    textlabel()
    skilldata()
    playeractionhitattribute()

    ROOT = os.path.dirname(os.path.realpath(__file__))


    SRC = ACTIONSDIR
    for root, dirs, files in os.walk(SRC, topdown=False):
        for f in files:
            playeraction(root+'/'+f)

    SRC = ANIMATION
    for root, dirs, files in os.walk(SRC, topdown=False):
        for f in files:
            anim(root+'/'+f)

    SRC = OVERRIDE
    for root, dirs, files in os.walk(SRC, topdown=False):
        for f in files:
            anim(root+'/'+f)

    for cid in idname:
        name = idname[cid]
        if cid[:3] == '199':
            continue
        aid1 = sae[int(cid+'1')]
        aid2 = sae[int(cid+'2')]
        s1sp = ssp[int(cid+'1')][0]
        s2sp = ssp[int(cid+'2')][0]
        s1sp2 = ssp[int(cid+'1')][1]
        s2sp2 = ssp[int(cid+'2')][1]
        aido = {}
        for i in range(3, 10):
            sid = int(cid+str(i))
            if sid in sae:
                aido[sid] = sae[sid]
        f1 = []
        f2 = []
        c1 = {}
        c2 = {}
        co = {}
        fo = {}
        for i in aid1:
            if i:
                f1.append(_do(cid, i))
                c1[i] = coef(i)
        for i in aid2:
            if i:
                f2.append(_do(cid, i))
                c2[i] = coef(i)
        for sid in aido:
            aid = aido[sid]
            fo[sid] = []
            for i in aid:
                if i:
                    fo[sid].append(_do(cid, i))
                    co["%s.%s"%(sid, i)] = coef(i)

        bvid = idid[cid]
        bvid = '%d;%d'%(bvid[0], bvid[1])

        aids = {}
        for i in aid1:
            aids[i] = 1
        for i in aid2:
            aids[i] = 1
        for i in aido.values():
            for j in i:
                aids[j] = 1
        timing = ''
        if 0 in aids:
            del(aids[0])
        for i in aids:
            timing += '%d:'%i
            if i not in aidhittiming:
                continue
            for j in aidhittiming[i]:
                timing += '%.4f, '%(float(j))
            timing += '| '
        print('"%s","%s","%s"'%(name, f1, f2),
                ',"%s(%s) %s(%s)"'%(s1sp, s1sp2, s2sp, s2sp2),
                ',"%s(%s) %s %s"'%(cid, bvid, aid1, aid2),
                ',"%s | %s","%s","%s","%s"'%(c1, c2, co, fo, timing) 
                )
def coef(aid):
    da1 = []
    da2 = []
    da3 = []
    ret = '<'
    if aid not in aidhit:
        return ''
    else:
        hits = aidhit[aid]
        for i in hits:
            h = i.strip()
            if h in hitda:
                da1.append(hitda[h])
            h = h[:-1] + '2'
            if h in hitda:
                da2.append(hitda[h])
            h = h[:-1] + '3'
            if h in hitda:
                da3.append(hitda[h])

    if len(da1) >= 1:
        for i in da1:
            coef = '%.2f'%(float(i)+0.001)
            if coef != '0.00':
                ret += coef+'+'
        if ret[-1] == '+':
            ret = ret[:-1]
    if len(da2) >= 1:
        ret += ' / '
        for i in da2:
            coef = '%.2f'%(float(i)+0.001)
            if coef != '0.00':
                ret += coef+'+'
        if ret[-1] == '+':
            ret = ret[:-1]
    if len(da3) >= 1:
        if len(da2) < 1:
            ret += ' /'
        ret += ' / '
        for i in da3:
            coef = '%.2f'%(float(i)+0.001)
            if coef != '0.00':
                ret += coef+'+'
        if ret[-1] == '+':
            ret = ret[:-1]
    ret += '>'
    return ret


idwp = {
        '1':'SWD',
        '2':'KAT',
        '3':'DAG',
        '4':'AXE',
        '5':'LAN',
        '6':'BOW',
        '7':'ROD',
        '8':'CAN',
        }

def _do(cid, aid):
    global aidframe, idid, labelframe, idwp, override
    if aid in aidframe:
        canceltime = aidframe[aid]
    else:
        #canceltime = -1
        canceltime = (-1, -1)
    if aid in aidlabel:
        labels = aidlabel[aid]
    else:
        labels = [['','0','0']]
    label = labels[-1][0]
    #startframe = float(labels[-1][1]) * float(labels[-1][2])
    startframe = float(labels[-1][1])
    startframe = int(startframe*60+0.01)
    speed = float(labels[-1][2])
    bvid = idid[cid]
    bvid = '%d%02d'%(bvid[0], bvid[1])
    labeltime = -1
    if label in labelframe:
        labeltime = labelframe[label]
    elif 'skill_unique_' in label:
        lid = label.replace('skill_unique_', '')
        wid = str(cid)[2]
        wp = idwp[wid]
        aname = wp+'_SKL_'+lid
        ocname = wp.lower()+'_'+bvid
        if aname in labelid and ocname in override:
            origin_ac_id  = labelid[aname]
            override_ac_id = override[ocname][origin_ac_id]
            labeltime = acframe[override_ac_id] + startframe
    if canceltime[0] >= 0:
        if '%.2f'%canceltime[1] == '1.00':
            return canceltime[0]
        else:
            return '%d/%.2f'%(canceltime[0], canceltime[1])
    elif labeltime >= 0:
        if '%.2f'%speed == '1.00':
            return labeltime
        else:
            return '%d/%.2f'%(labeltime, speed)
    else:
        return label


if __name__ == "__main__":
    print('-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-')
    main()

