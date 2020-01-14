import re

def findsameblock(f, blockname):
    ret = []
    loc = 0
    status = 0
    prefix = ''
    oneblock = ''
    for line in f:
        if status == 0:
            loc = line.find(blockname)
            if loc != -1 and line[loc-1] in ['\t', ' ']:
                status = 1
                oneblock = line
                prefix = line[:loc]
        elif status == 1:
            if len(line)>loc and line[loc-1] in ['\t', ' ']:
                oneblock += line
            else:
                ret.append(oneblock)
                status = 0
    if status == 1:
        ret.append(oneblock)
    return ret


def findblock(f, blockname):
    ret = []
    loc = 0
    status = 0
    prefix = ''
    oneblock = ''
    for line in f:
        if status == 0:
            loc = line.find(blockname)
            if loc != -1 and line[loc-1] in ['\t', ' ']:
                status = 1
                oneblock = line
                prefix = line[:loc]
        elif status == 1:
            if len(line)>loc and line[loc] in ['\t', ' ']:
                oneblock += line
            else:
                ret.append(oneblock)
                status = 0
    if status == 1:
        ret.append(oneblock)
    return ret

if __name__ == '__main__':
    f = open('out/skill/resources/actions/playeraction/bow/playeraction_00691110.prefab') 
    lines = f.readlines()
    r = findsameblock(lines, 'float _seconds')

    for i in r:
        print('-----');
        print(i);


