import sys, os

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

def main(fin, fout):
    for line in fin:
        idx = line.find('_command = ')
        if idx != -1:
            cmdno = line[idx+11:-1]
            line = line.replace(cmdno, r_command[int(cmdno)]);
        idx = line.find('compare = ')
        if idx != -1:
            compareno = line[idx+10:-1]
            line = line.replace(compareno, r_compare[int(compareno)]);
        fout.write(line);

if __name__ == '__main__':
    if len(sys.argv) == 1:
        with os.scandir('.') as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if entry.name[-6:] == '.asset':
                        fin = open(entry.name);
                        fout = open(entry.name+'.1', 'w')
                        main(fin, fout)
    else:
        fin = open(sys.argv[1])
        fout = open(sys.argv[1]+'.1', 'w')
        main(fin, fout)



#// Namespace: 
#public enum eMoveAction // TypeDefIndex: 8939
#{
#	// Fields
#	public int value__; // 0x10
#	public const eMoveAction none = 0; // 0x0
#	public const eMoveAction approch = 1; // 0x0
#	public const eMoveAction escape = 2; // 0x0
#	public const eMoveAction escapeTL = 3; // 0x0
#	public const eMoveAction pivot = 4; // 0x0
#	public const eMoveAction anchor = 5; // 0x0
#}
#
#// Namespace: 
#public enum eTurnAction // TypeDefIndex: 8940
#{
#	// Fields
#	public int value__; // 0x10
#	public const eTurnAction none = 0; // 0x0
#	public const eTurnAction target = 1; // 0x0
#	public const eTurnAction warldCenter = 2; // 0x0
#	public const eTurnAction north = 3; // 0x0
#	public const eTurnAction east = 4; // 0x0
#	public const eTurnAction south = 5; // 0x0
#	public const eTurnAction west = 6; // 0x0
#	public const eTurnAction pivot = 7; // 0x0
#	public const eTurnAction anchor = 8; // 0x0
#}
#public enum eTargetType // TypeDefIndex: 8941
#{
#	// Fields
#	public int value__; // 0x10
#	public const eTargetType ally = 0; // 0x0
#	public const eTargetType hostile = 1; // 0x0
#	public const eTargetType allyChild = 2; // 0x0
#	public const eTargetType minion = 3; // 0x0
#	public const eTargetType gm_turn = 4; // 0x0
#}
#public enum eCtrlState // TypeDefIndex: 9156
#{
#	// Fields
#	public int value__; // 0x10
#	public const eCtrlState none = 0; // 0x0
#	public const eCtrlState standby = 1; // 0x0
#	public const eCtrlState battle = 2; // 0x0
#	public const eCtrlState goHome = 3; // 0x0
#	public const eCtrlState route = 4; // 0x0
#}
#
#// Namespace: 
#private enum eActionState // TypeDefIndex: 9157
#{
#	// Fields
#	public int value__; // 0x10
#	public const eActionState none = 0; // 0x0
#	public const eActionState move = 1; // 0x0
#	public const eActionState rotate = 2; // 0x0
#	public const eActionState action = 3; // 0x0
#}


