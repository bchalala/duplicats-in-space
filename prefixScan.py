
from collections import defaultdict

'''
Perform prefixScan algorithm on data, return frequent patterns with corresponding support
'''
def mine(db, minsup):
    results = []
    prefixScan_rec(db, minsup, [], results, [(i, 0) for i in range(len(db))])
    return results

'''
Recursive implementation of prefixScan
'''
def prefixScan_rec(db, minsup, patt, results, mdb):
    results.append((patt, len(mdb)))

    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        for j in range(startpos, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j + 1))

    for c, newmdb in occurs.items():
        if len(newmdb) >= minsup:
            prefixScan_rec(db, minsup, patt + [c], results, newmdb)

'''
Run tests to test pattern mining
Expected output: [([], 4), ([0], 2), ([1], 4), ([1, 1], 2), ([1, 1, 1], 2), ([1, 2], 3), ([1, 2, 2], 2), ([1, 3], 2), ([1, 3, 4], 2), ([1, 4], 2), ([2], 3), ([2, 2], 2), ([3], 2), ([3, 4], 2), ([4], 2)]
'''
def testPrefixScan():
    db = [
        [0, 1, 2, 3, 4],
        [1, 1, 1, 3, 4],
        [2, 1, 2, 2, 0],
        [1, 1, 1, 2, 2],
    ]

    minsup = 2
    results = mine(db, minsup)
    print(results)



# testPrefixScan()
