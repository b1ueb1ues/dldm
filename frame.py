# config ######################################################################
OUTFILE = 'out_frame'
INDIR = 'actions'

###############################################################################
import os
import re

fout = 0

aidframe = {}
def aid2frame(fname):
    data = open(fname).read()
    r = re.findall(r'commandType = 15\n.*float _seconds = (.+)\n.*float _speed = (.*)\n', data)
    if len(r) != 1:
        return
    _seconds, _speed = r[0]
    aid = re.findall(r'playeraction_(\d+).*', fname)[0]
    duration = float(_seconds)*float(_speed)
    frame = int(duration*60+0.01)
    print(aid, frame)
    aidframe[aid] = frame


def main():
    global OUTFILE, INDIR
    global SRC, DST
    global inprefix
    global fout
    if 'OUTFILE' not in globals():
        OUTFILE = None
    if 'INDIR' not in globals():
        INDIR = None
    ROOT = os.path.dirname(os.path.realpath(__file__))
    #SRC = os.path.join(ROOT, INDIR)
    SRC = INDIR
    DST = os.path.join(ROOT, OUTFILE)
    fout = open(DST,'w')
    inprefix = len(SRC)+1

    for root, dirs, files in os.walk(SRC, topdown=False):
        #print(root)
        if '.git' in root:
            continue
        for f in files:
            aid2frame(root+'/'+f)

sa = {}
def sid2aid():
    global sa
    data = open('skilldata.asset').read()
    r = re.findall(r'SkillDataElement data\n.*_Id = (\d+)(\n|.)*?_ActionId1 = (\d+)\n'
            + r'.*_ActionId2 = (\d+)\n'
            + r'.*_ActionId3 = (\d+)\n'
            + r'.*_ActionId4 = (\d+)\n'
            , data)
    for i in r:
        if i[0] != '0':
            sid = int(i[0])
            tmp = []
            for idx in range(2, 6):
                if i[idx] != '0':
                    tmp.append(int(i[idx]))
            sa[sid] = tmp

    print(sa)



if __name__ == "__main__":
    sid2aid()
    #main()

