import sys, os
from block import *
import re

INDIR = 'out/all.0/resources/aiscript'
INFILE = 'out/bos_drg_21000401_03.asset'

command = {
'Def':0                   ,
'EndDef':1                ,
'If':2                    ,
'Else':3                  ,
'ElseIF':4                ,
'EndIf':5                 ,
'Set':6                   ,
'Add':7                   ,
'Sub':8                   ,
'SetTarget':9             ,
'EndScript':10            ,
'Action':11               ,
'Function':12             ,
'MoveAction':13           ,
'TurnAction':14           ,
'Random':15               ,
'RecTimer':16             ,
'RecHpRate':17            ,
'AliveNum':18             ,
'Jump':19                 ,
'Wake':20                 ,
'ClearDmgCnt':21          ,
'UnusualPosture':22       ,
'FromActionSet':23        ,
'GM_SetTurnEvent':24      ,
'GM_CompleteTurnEvent':25 ,
'GM_SetTurnMax':26        ,
'GM_SetSuddenEvent':27    ,
'GM_SetBanditEvent':28    ,
'Mul':29                  ,
'OrderCloser':30          ,
'OrderAliveFather':31     ,
'Reserve06':32            ,
'Reserve07':33            ,
'Reserve08':34            ,
'Reserve09':35            ,
'Reserve10':36
}

compare = {
'largeEqual'  : 0 ,
'smallEqual'  : 1 ,
'repudiation' : 2 ,
'equal'       : 3 ,
'large'       : 4 ,
'small'       : 5 ,
'none'        : 6
}

def dr(d):
    r = {}
    for k,v in d.items():
        r[v] = k
    return r

r_command = dr(command)
r_compare = dr(compare)


def p1(fin, basename):
    fout = open(basename+'.1', 'w')
    tmp = 0
    for line in fin:
        idx = line.find('_command = ')
        if idx != -1:
            cmdno = line[idx+11:-1]
            line = line.replace(cmdno, r_command[int(cmdno)]);
        idx = line.find('compare = ')
        if idx != -1:
            compareno = line[idx+10:-1]
            line = line.replace(compareno, r_compare[int(compareno)]);
        if tmp :
            line = line[:-1] + ' ' + tmp
            tmp = 0
        else:
            idx = line.find('[')
            if idx != -1:
                if line[idx-1] in [' ', '\t']:
                    tmp = line[idx:]

        fout.write(line);
    fout.close()
    return basename+'.1'

def p2(fin, basename):
    fout = open(basename+'.2', 'w')
    lines = fin.readlines()
    b = findblock(lines, 'AIScriptContainer data')
    pref = ''
    for i in b:
        idx = int(i[i.find('[')+1:i.find(']')])
        cmd = re.findall(r'int _command = (.*)\n', i)[0]
        jmp = int(re.findall(r'int _jumpStep = (.*)\n', i)[0])
        cpr = re.findall(r'int compare = (.*)\n', i)
        if cpr == []:
            cpr = 'none'
        else:
            cpr = cpr[0]
        params = findblock(i.split('\n'), 'AIScriptParam data')
        if cmd in ['ElseIF', 'Else', 'EndIf', 'EndDef']:
            pref = pref[:-4]
        #line = '%d: %s%s'%(idx, pref, cmd)
        line = '%s%s'%(pref, cmd)
        if cmd in ['If', 'Def', 'ElseIF', 'Else']:
            pref += '    '
        for p in params:
            valuedata = findblock(p.split('\n'), 'AIScriptValue data');
            for vd in valuedata:
                vtype = int(re.findall(r'int valType = (.*)\n', vd)[0])
                if vtype == 0:
                    v = re.findall(r'string valString = "(.*)"\n', vd)[0]
                    v = '<%s>'%v
                elif vtype == 1:
                    v = re.findall(r'int valInt = (.*)\n', vd)[0]
                elif vtype == 2:
                    v = re.findall(r'float valFloat = (.*)\n', vd)[0]
                line += ' ' + v
        if cpr != 'none':
            line += ' ' + cpr
        if jmp != 1:
            line += ' [+%d]'%jmp
        fout.write(line+'\n')
    fout.close()
    return basename+'.2'

def main(basename):
    fname = basename
    fname = p1(open(fname), basename)
    fname = p2(open(fname), basename)

if __name__ == '__main__':
    if INFILE :
        main(INFILE)
    elif len(sys.argv) == 1 :
        with os.scandir(INDIR) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if entry.name[-6:] == '.asset':
                        main(entry.name)
    else:
        main(sys.argv[1])



