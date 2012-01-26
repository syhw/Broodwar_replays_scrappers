Requirements
============
make  
python  
pyreplib (optional, for the verification/sorting/trashing part)

Pipeline
========
Download replays
----------------
You need to download replays from replays sites, it can take a while
(2 days with the no leeching policy of ICCUP for instance):

    cd gosugamers|iccup|teamliquid && make

Unify replays
-------------
You may have downloaded the same replay numerous times, so we have 
to unify them, we do that with a hash (sha256) of the file:

    cd unifier && vim unifier.py
    # change to match the folders of the recently downloaded replays
    make

Verify and sort replays
-----------------------
Some of the replays may be corrupted and should be trashed, some others
may be sorted in the wrong match-up folder. You will now verify and sort 
them, for that, you need the pyreplib python library:

    cd match_ups && python verify_and_sort.py PATH_TO_REPLAY_FOLDER

In PATH_TO_REPLAY_FOLDER/trash, you have the corrupted replays, other valid
replays should be in their right match-up folder.

Special case of ICCUP
=====================
ICCUP server has some kind of anti-leech policy, so the download script waits
for some time after each failure. Also in the iccup/crawl.py, you can change
(commented line) if you want to use the users replays, the current default is
to use only the gosus replays of ICCUP.

Archive
=======
Do not forget about excluding all the trash your OS can put in:

    tar czf archive-name.tar.gz --exclude *.DS_Store replays/

