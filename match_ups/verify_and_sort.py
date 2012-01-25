from pyreplib import replay, utils
import shutil, os, sys

def match_up(r):
    """ heuristic which determines the match-up according to units numbers
    naming scheme: "XvY" with P first, then T, then Z """
    s = []
    for p in r.players:
        score = 0
        for (k,v) in utils.unit_distribution(p).iteritems():
            score += v
        s.append((score, p))
    max1 = 0
    max2 = 0
    p1 = r.players[0]
    p2 = r.players[1]
    for e in s:
        if e[0] > max1:
            max2 = max1
            max1 = e[0]
            p2 = p1
            p1 = e[1]
        elif e[0] > max2:
            max2 = e[0]
            p2 = e[1]
    mu_raw = p1.race_name[0] + 'v' + p2.race_name[0]
    if mu_raw[2] == 'P': # P in front
        mu_raw = mu_raw[2] + 'v' + mu_raw[0]
    elif mu_raw[2] == 'T' and mu_raw[0] != 'P': # T in front
        mu_raw = mu_raw[2] + 'v' + mu_raw[0]
    return mu_raw

def move_if_needed(prefix):
    """ Goes through all replays in "prefix" and moves them to the right
    match-up folders (based on the "match_up" heuristic) """
    print 'working on', prefix
    for dname in os.listdir(prefix):
        if os.path.isdir(prefix+dname):
            print dname
            for fname in os.listdir(prefix+dname):
                if fname[-3:] == 'rep':
                    fullfn = prefix + dname + '/' + fname
                    print fullfn
                    rep = replay.Replay(fullfn)
                    mu = match_up(rep)
                    if dname != mu:
                        shutil.move(fullfn, prefix + mu + '/' + fname)
                        print 'moved:', fullfn
                        print 'to:', prefix+mu+'/'+fname

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "need an arg"
    else:
        if (sys.argv[len(sys.argv)-1][-3:] == 'rep'):
            print match_up(replay.Replay(sys.argv[len(sys.argv)-1]))
        else:
            move_if_needed(sys.argv[len(sys.argv)-1])

