import urllib2, re, time, os

fullr = r'\<div>[PZT] v [PZT]\</div>.+?replays/download[^"]+'
rr = r'replays/download[^"]+'
rnext = r'(/starcraft/replays/[^"]+)">next &raquo;'
prefix = 'http://www.iccup.com'
failed = []

def find_mu(fr):
    mu = re.search('[PZT] v [PZT]', fr).group(0).replace(' ', '')
    if mu[2] == 'P': # P in front
        mu = mu[2] + 'v' + mu[0]
    elif mu[2] == 'T' and mu[0] != 'P': # T in front
        mu = mu[2] + 'v' + mu[0]
    return mu

def dlreps(p):
    fullreplays = re.findall(fullr, p, re.DOTALL)
    for fullreplay in fullreplays:
        try:
            replay = re.findall(rr, fullreplay)[0]
            mu = find_mu(fullreplay)
            repfile = 'replays/' + mu + '/' + re.search(r'(\d+)\.html', replay).group(1) + '.rep'
            if not os.path.exists(repfile):
                output = open(repfile, 'w')
                output.write(urllib2.urlopen(
                    urllib2.urlopen(prefix + '/' + replay).geturl()).read())
                output.close()
                print 'saved', repfile
        except:
            print 'failed saving', replay
            failed.append((fullreplay, 0, len(failed)+1)) 

if __name__ == '__main__':
    #page = urllib2.urlopen(prefix + "/starcraft/replays.html").read()
    page = urllib2.urlopen(prefix + "/starcraft/replays/user.html").read()
    dlreps(page)
    mnext = re.search(rnext, page)
    print mnext
    print mnext.group(1)
    while mnext.group(1) is not '':
        try:
            page = urllib2.urlopen(prefix + mnext.group(1)).read()
            dlreps(page)
            mnext = re.search(rnext, page)
            print mnext
            print mnext.group(1)
        except urllib2.HTTPError:
            time.sleep(5)
        for (i, fail) in enumerate(failed): 
            if fail[1] < (fail[2] + 1):
                failed[i] = (failed[i][0], failed[i][1]+1, failed[i][2])
                try:
                    replay = re.findall(rr, fail[0])[0]
                    mu = find_mu(fail[0])
                    repfile = 'replays/' + mu + '/' + re.search(r'(\d+)\.html', replay).group(1) + '.rep'
                    output = open(repfile, 'w')
                    output.write(urllib2.urlopen(
                        urllib2.urlopen(prefix + '/' + replay).geturl()).read())
                    output.close()
                    print 'saved', repfile
                except:
                    print 'failed again with', replay
            else:
                del failed[i]
    for (i, fail) in enumerate(failed):
        if fail[1] < (fail[2] + 1):
            failed[i] = (failed[i][0], failed[i][1]+1, failed[i][2])
            try:
                replay = re.findall(rr, fail[0])[0]
                mu = find_mu(fail[0])
                repfile = 'replays/' + mu + '/' + re.search(r'(\d+)\.html', replay).group(1) + '.rep'
                output = open(repfile, 'w')
                output.write(urllib2.urlopen(
                    urllib2.urlopen(prefix + '/' + replay).geturl()).read())
                output.close()
                print 'saved', repfile
            except:
                print 'failed again with', replay
                time.sleep(2)
        else:
            del failed[i]
    print 'finally failed with:', len(failed)


