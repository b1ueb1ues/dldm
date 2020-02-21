import sys

chart = {
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


fin = open(sys.argv[1])
fout = open(sys.argv[1]+'.1', 'w')
for line in fin:
    if '_command = ' in line:
        for k,v in chart.items():
            line = line.replace(str(v), k);
    fout.write(line);


