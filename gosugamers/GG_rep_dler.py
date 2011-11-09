import urllib2, re, time

prefix = 'http://www.gosugamers.net/starcraft/'
url = prefix + 'replays.php?&format=1on1&start='
fullreps = r'title=(Protoss|Zerg|Terran).*?title=(Protoss|Zerg|Terran).*?(admin/a_replays\.php\?dl=\d+)'
failed = []
failedpages = []

def find_mu(r1, r2):
    mu = r1 + 'v' + r2
    if r2 == 'P': # P in front
        mu = r2 + 'v' + r1 
    elif r2 == 'T' and r1 != 'P': # T in front
        mu = r2 + 'v' + r1 
    return mu

def download_and_write((mu, replink)):
    repfile = 'replays/' + mu + '/' + replink.split('=')[1] + '.rep'
    f = open(repfile, "wb")
    f.write(urllib2.urlopen(prefix + replink).read())
    f.close()
    print "saved replay ", repfile

def download_all_reps_on(page):
    fullreplays = re.findall(fullreps, page, re.DOTALL)
    print fullreplays
    for fullreplay in fullreplays:
        mu = find_mu(fullreplay[0][0], fullreplay[1][0])
        try:
            download_and_write((mu, fullreplay[2]))
        except:
            print "failed saving", fullreplay[2]
            failed.append((mu, fullreplay[2]))
    for fail in failed:
        try:
            download_and_write(fail)
        except:
            time.sleep(10)
            print "failed again saving", fail[1]

if __name__ == '__main__':
    for i in range(0, 7800, 100): # see why here http://www.gosugamers.net/starcraft/replays.php
        try:
            print 'dling page:', str(i)
            page = urllib2.urlopen(url + str(i)).read()
            download_all_reps_on(page)
        except: 
            time.sleep(10)
            print 'failed with rep page:', str(i)
            failedpages.append(i)
    for i in failedpages:
        try:
            print 'dling page:', str(i)
            page = urllib2.urlopen(url + str(i)).read()
            download_all_reps_on(page)
        except: 
            time.sleep(10)
            print 'ultimately failed with rep page:', str(i)
    print 'failed for that much pages:', len(failedpages)
    print 'failed for that much reps:', len(failed)

