from pyreplib import replay, utils
import shutil, os, hashlib

already_seen = set()

def players_date(rep):
    s = ''
    for p in rep.players:
        s += p
    s += rep.date

def add_from_prefix(prefix):
    print 'working on', prefix
    for dname in os.listdir(prefix):
        print dname
        for fname in os.listdir(prefix + dname):
            s = players_date(replay.Replay(fname))
            if (s not in already_seen):
                shutil.copyfile(prefix + dname + '/' + fname, 'replays/' + dname + '/' + fname)
                already_seen.add(s)
                print 'added:', fname
            else:
                print 'already seen:', fname

if __name__ == '__main__':
    shutil.copytree('../iccup/replays', 'replays')
    print 'added all iccup replays'
    for dname in os.listdir('replays'):
        for fname in os.listdir('replays/' + dname):
            print fname
            try:
                s = players_date(replay.Replay(fname))
                already_seen.add(s)
                print 'added:', fname
            except:
                print 'didnt work on', fname
    add_from_prefix('../teamliquid/replays')
    add_from_prefix('../gosugamers/replays')

