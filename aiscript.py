import sys, os
from block import *
import re

OUTDIR = 'out/aiscript'
INDIR = 'out/all/resources/aiscript'
_R = True
#INFILE = 'out/bos_drg_21000401_03.asset'


src = '''
// Namespace: 
public enum Command // TypeDefIndex: 8938
{
	// Fields
	public int value__; // 0x10
	public const Command Def = 0; // 0x0
	public const Command EndDef = 1; // 0x0
	public const Command If = 2; // 0x0
	public const Command Else = 3; // 0x0
	public const Command ElseIF = 4; // 0x0
	public const Command EndIf = 5; // 0x0
	public const Command Set = 6; // 0x0
	public const Command Add = 7; // 0x0
	public const Command Sub = 8; // 0x0
	public const Command SetTarget = 9; // 0x0
	public const Command EndScript = 10; // 0x0
	public const Command Action = 11; // 0x0
	public const Command Function = 12; // 0x0
	public const Command MoveAction = 13; // 0x0
	public const Command TurnAction = 14; // 0x0
	public const Command Random = 15; // 0x0
	public const Command RecTimer = 16; // 0x0
	public const Command RecHpRate = 17; // 0x0
	public const Command AliveNum = 18; // 0x0
	public const Command Jump = 19; // 0x0
	public const Command Wake = 20; // 0x0
	public const Command ClearDmgCnt = 21; // 0x0
	public const Command UnusualPosture = 22; // 0x0
	public const Command FromActionSet = 23; // 0x0
	public const Command GM_SetTurnEvent = 24; // 0x0
	public const Command GM_CompleteTurnEvent = 25; // 0x0
	public const Command GM_SetTurnMax = 26; // 0x0
	public const Command GM_SetSuddenEvent = 27; // 0x0
	public const Command GM_SetBanditEvent = 28; // 0x0
	public const Command Mul = 29; // 0x0
	public const Command OrderCloser = 30; // 0x0
	public const Command OrderAliveFather = 31; // 0x0
	public const Command Reserve06 = 32; // 0x0
	public const Command Reserve07 = 33; // 0x0
	public const Command Reserve08 = 34; // 0x0
	public const Command Reserve09 = 35; // 0x0
	public const Command Reserve10 = 36; // 0x0
}


// Namespace: Gluon
public enum ActionTarget // TypeDefIndex: 8512
{
	// Fields
	public int value__; // 0x10
	public const ActionTarget NONE = 0; // 0x0
	public const ActionTarget MYSELF_00 = 1; // 0x0
	public const ActionTarget ALLY_HP_02 = 4; // 0x0
	public const ActionTarget ALLY_HP_03 = 5; // 0x0
	public const ActionTarget ALLY_HP_04 = 6; // 0x0
	public const ActionTarget ALLY_DISTANCE_00 = 7; // 0x0
	public const ActionTarget ALLY_DISTANCE_01 = 8; // 0x0
	public const ActionTarget ALLY_STRENGTH_00 = 9; // 0x0
	public const ActionTarget ALLY_STRENGTH_01 = 10; // 0x0
	public const ActionTarget ALLY_BUFF_00 = 11; // 0x0
	public const ActionTarget ALLY_BUFF_01 = 12; // 0x0
	public const ActionTarget ALLY_BUFF_04 = 15; // 0x0
	public const ActionTarget HOSTILE_DISTANCE_00 = 16; // 0x0
	public const ActionTarget HOSTILE_DISTANCE_01 = 17; // 0x0
	public const ActionTarget HOSTILE_HP_00 = 18; // 0x0
	public const ActionTarget HOSTILE_STRENGTH_00 = 19; // 0x0
	public const ActionTarget HOSTILE_STRENGTH_01 = 20; // 0x0
	public const ActionTarget HOSTILE_TARGET_00 = 21; // 0x0
	public const ActionTarget HOSTILE_TARGET_01 = 22; // 0x0
	public const ActionTarget HOSTILE_TARGET_02 = 23; // 0x0
	public const ActionTarget HOSTILE_RANDOM_00 = 24; // 0x0
	public const ActionTarget HOSTILE_FRONT_00 = 25; // 0x0
	public const ActionTarget HOSTILE_BEHIND_00 = 26; // 0x0
	public const ActionTarget ALL_DISTANCE_00 = 27; // 0x0
	public const ActionTarget ALL_DISTANCE_01 = 28; // 0x0
	public const ActionTarget ALL_RANDOM_00 = 29; // 0x0
	public const ActionTarget PLAYER1_TARGET = 30; // 0x0
	public const ActionTarget PLAYER2_TARGET = 31; // 0x0
	public const ActionTarget PLAYER3_TARGET = 32; // 0x0
	public const ActionTarget PLAYER4_TARGET = 33; // 0x0
	public const ActionTarget PLAYER_RANDOM = 34; // 0x0
	public const ActionTarget HOSTILE_SWOON = 35; // 0x0
	public const ActionTarget HOSTILE_BIND = 36; // 0x0
	public const ActionTarget PLAYER_RANDOM_INDIRECT = 37; // 0x0
	public const ActionTarget PLAYER_RANDOM_DIRECT = 38; // 0x0
	public const ActionTarget HOSTILE_OUT_MARKER_00 = 39; // 0x0
	public const ActionTarget HOSTILE_OUT_MARKER_01 = 40; // 0x0
	public const ActionTarget HOSTILE_OUT_MARKER_02 = 41; // 0x0
	public const ActionTarget SPECIAL_HATE = 42; // 0x0
	public const ActionTarget HOSTILE_DISTANCE_NO_LIMIT = 43; // 0x0
	public const ActionTarget REGISTERED_01 = 44; // 0x0
	public const ActionTarget REGISTERED_02 = 45; // 0x0
	public const ActionTarget REGISTERED_03 = 46; // 0x0
	public const ActionTarget REGISTERED_04 = 47; // 0x0
}

// Namespace: 
public enum eCompare // TypeDefIndex: 8946
{
	// Fields
	public int value__; // 0x10
	public const eCompare largeEqual = 0; // 0x0
	public const eCompare smallEqual = 1; // 0x0
	public const eCompare repudiation = 2; // 0x0
	public const eCompare equal = 3; // 0x0
	public const eCompare large = 4; // 0x0
	public const eCompare small = 5; // 0x0
	public const eCompare none = 6; // 0x0
}

// Namespace: 
public enum eMoveAction // TypeDefIndex: 8939
{
	// Fields
	public int value__; // 0x10
	public const eMoveAction none = 0; // 0x0
	public const eMoveAction approch = 1; // 0x0
	public const eMoveAction escape = 2; // 0x0
	public const eMoveAction escapeTL = 3; // 0x0
	public const eMoveAction pivot = 4; // 0x0
	public const eMoveAction anchor = 5; // 0x0
}

// Namespace: 
public enum eTurnAction // TypeDefIndex: 8940
{
	// Fields
	public int value__; // 0x10
	public const eTurnAction none = 0; // 0x0
	public const eTurnAction target = 1; // 0x0
	public const eTurnAction warldCenter = 2; // 0x0
	public const eTurnAction north = 3; // 0x0
	public const eTurnAction east = 4; // 0x0
	public const eTurnAction south = 5; // 0x0
	public const eTurnAction west = 6; // 0x0
	public const eTurnAction pivot = 7; // 0x0
	public const eTurnAction anchor = 8; // 0x0
}

'''

def dr(d):
    r = {}
    reg = d+r' (.*)=(.*);'
    tmp = re.findall(reg, src)
    for i in tmp:
        r[i[1].strip()] = i[0].strip()
    return r

command = dr('public const Command')
compare = dr('public const eCompare')
moveaction = dr('public const eMoveAction')
turnaction = dr('public const eTurnAction')
target = dr('public const ActionTarget')
for i in command:
    if command[i] in ['If', 'ElseIF', 'Else', 'EndIf', 'Def', 'EndDef', 'Jump']:
        command[i] = command[i].lower()

r_compare = {
    'largeEqual'  : '>=',
    'smallEqual'  : '<=',
    'repudiation' : '!=',
    'equal'       : '==',
    'large'       : '>' ,
    'small'       : '<'
}

# script If A 0 large means 0 > A
# for python we usually use A > 0, so reverse the direction of comare
rr_compare = {
    'largeEqual'  : '<=',
    'smallEqual'  : '>=',
    'repudiation' : '!=',
    'equal'       : '==',
    'large'       : '<' ,
    'small'       : '>'
}


def p1(fin, basename):
    ret = []
    tmp = 0
    for line in fin:
        idx = line.find('_command = ')
        if idx != -1:
            cmdno = line[idx+11:-1]
            line = line.replace(cmdno, command[cmdno]);
        idx = line.find('compare = ')
        if idx != -1:
            compareno = line[idx+10:-1]
            line = line.replace(compareno, compare[compareno]);
        if tmp :
            line = line[:-1] + ' ' + tmp
            tmp = 0
        else:
            idx = line.find('[')
            if idx != -1:
                if line[idx-1] in [' ', '\t']:
                    tmp = line[idx:]

        ret.append(line);
    return ret

def asm(cmd, params, jmp, pref):
    line = '%s%s'%(pref, cmd)
    if cmd in ['if', 'elseif']:
        if cmd == 'elseif':
            line = '%selif'%pref
        for p in params:
            if len(p) == 3:
                line += ' %s %s %s,'%(p[0], rr_compare[p[2]], p[1])
            else:
                for v in p:
                    line += ' ' + v
                    line += ','
        line = line[:-1] + ':    # +%d'%jmp
    elif cmd == 'else':
        line += ':'
    elif cmd == 'endif':
        line = pref+'#endif'
    elif cmd == 'def':
        line += ' ' + params[0][0] + '():'
    elif cmd == 'enddef':
        line = pref+'#enddef\n'
    elif cmd == 'Set':
        line = pref + params[0][0] + ' = '
        count = 0
        for p in params:
            if count == 0:
                count = 1
                continue
            elif count == 1:
                count = 2
            else:
                line += ', '
            line += p[0]
    elif cmd == 'Add':
        if len(params) != 2:
            errrrrrrrrr()
        line = '%s%s += %s'%(pref, params[0][0], params[1][0])
    elif cmd == 'Sub':
        if len(params) != 2:
            errrrrrrrrr()
        line = '%s%s -= %s'%(pref, params[0][0], params[1][0])
    elif cmd == 'Mul':
        if len(params) != 2:
            errrrrrrrrr()
        line = '%s%s *= %s'%(pref, params[0][0], params[1][0])
    elif cmd == 'jump':
        line = pref + '#jump +%d'%jmp
    elif cmd == 'SetTarget':
        line += '('
        for p in params:
            line += '"%s", '%target[p[0]]
        line = line[:-2] + ')'
    elif cmd == 'MoveAction':
        line += '('
        count = 0
        for p in params:
            if count == 0:
                line += '"%s", '%moveaction[p[0]]
                count += 1
            else:
                line += '%s, '%p[0]
        line = line[:-2] + ')'
    elif cmd == 'TurnAction':
        line += '('
        for p in params:
            line += '"%s", '%turnaction[p[0]]
        line = line[:-2] + ')'
    else:
        line += '('
        for p in params:
            for v in p:
                line += v + ', '
        if line[-2] == ',':
            line = line[:-2] + ')'
        else:
            line = line + ')'
        if jmp != 1:
            line += '    # +%d'%jmp
    return line

def p2(fin, basename):
    #fout = open(basename+'.2', 'w')
    fout = os.path.join(OUTDIR, os.path.splitext(basename)[0]+'.py')
    fout = fout.replace(INDIR, '')
    if not os.path.exists(os.path.dirname(fout)):
        os.makedirs(os.path.dirname(fout), exist_ok=True)
    fout = open(fout, 'w')
    lines = fin
    b = findblock(lines, 'AIScriptContainer data')
    pref = ''
    for i in b:
        idx = int(i[i.find('[')+1:i.find(']')])
        cmd = re.findall(r'int _command = (.*)\n', i)[0]
        jmp = int(re.findall(r'int _jumpStep = (.*)\n', i)[0])
        params = findblock(i.split('\n'), 'AIScriptParam data')
        if cmd in ['elseif', 'else', 'endif', 'enddef']:
            pref = pref[:-4]
            #pref = idx+': '+pref[:-4]
        row = []
        for p in params:
            columndata = findblock(p.split('\n'), 'Column data')
            for c in columndata:
                column = []
                valuedata = findblock(c.split('\n'), 'AIScriptValue data')
                for vd in valuedata:
                    vtype = int(re.findall(r'int valType = (.*)\n', vd)[0])
                    if vtype == 0:
                        v = re.findall(r'string valString = "(.*)"\n', vd)[0]
                        #v = '<%s>'%v
                    elif vtype == 1:
                        v = re.findall(r'int valInt = (.*)\n', vd)[0]
                    elif vtype == 2:
                        v = re.findall(r'float valFloat = (.*)\n', vd)[0]
                    column.append(v)
                cpr = re.findall(r'int compare = (.*)\n', i)[0]
                if cpr != 'none':
                    column.append(cpr)
                row.append(column)
        line = asm(cmd, row, jmp, pref)
        if cmd in ['if', 'def', 'elseif', 'else']:
            pref += '    '
        if line != None:
            fout.write(line+'\n')
    fout.close()
    return

def main(basename):
    print(basename)
    tmp = p1(open(basename), basename)
    p2(tmp, basename)


if __name__ == '__main__':
    for i in ['INFILE', 'R']:
        if i not in globals():
            globals()[i] = 0

    if OUTDIR:
        if not os.path.exists(OUTDIR):
            os.makedirs(OUTDIR)
    if INFILE:
        main(INFILE)
    elif len(sys.argv) == 1 : # no args
        if _R:
            for root, dirs, files in os.walk(INDIR):
                for f in files:
                    if os.path.splitext(f)[1] == '.asset':
                        main(os.path.join(root, f))
        else:
            with os.scandir(INDIR) as it:
                for entry in it:
                    if not entry.name.startswith('.') and entry.is_file():
                        if entry.name[-6:] == '.asset':
                            main(entry.name)
    else:
        main(sys.argv[1])



