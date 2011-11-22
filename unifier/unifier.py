import shutil, os, hashlib

already_seen = set()

def add_from_prefix(prefix, fprefix=''):
    print 'working on', prefix
    for dname in os.listdir(prefix):
        if os.path.isdir(prefix+dname):
            print dname
            for fname in os.listdir(prefix + dname):
                fullfn = prefix + dname + '/' + fname
                h = hashlib.sha256(open(fullfn, 'rb').read())
                if (h.hexdigest() not in already_seen):
                    shutil.copyfile(fullfn, 'replays/' + dname + '/' + fprefix + fname)
                    already_seen.add(h.hexdigest())
                    print 'added:', fullfn
                else:
                    print 'already seen:', fullfn

if __name__ == '__main__':
    add_from_prefix('replays/', 'HERE')
    add_from_prefix('../iccup/replays/', 'IC')
    add_from_prefix('../teamliquid/replays/', 'TL')
    add_from_prefix('../gosugamers/replays/', 'GG')

