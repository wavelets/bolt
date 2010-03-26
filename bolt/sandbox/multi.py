"""

"""

import numpy as np
import bolt

from time import time

def main(args):
    import nltk

    ftrain = args[0]
    ftest = args[1]
    print ftrain, ftest

    dtrain = bolt.io.MemoryDataset.load(ftrain, verbose = 0)
    dtest = bolt.io.MemoryDataset.load(ftest, verbose = 0)

    cats = ['alt.atheism',
 'comp.graphics',
 'comp.os.ms-windows.misc',
 'comp.sys.ibm.pc.hardware',
 'comp.sys.mac.hardware',
 'comp.windows.x',
 'misc.forsale',
 'rec.autos',
 'rec.motorcycles',
 'rec.sport.baseball',
 'rec.sport.hockey',
 'sci.crypt',
 'sci.electronics',
 'sci.med',
 'sci.space',
 'soc.religion.christian',
 'talk.politics.guns',
 'talk.politics.mideast',
 'talk.politics.misc',
 'talk.religion.misc']
    
    cats = dict(((i,c) for i,c in enumerate(cats)))
    k = len(cats)
    
    model = bolt.GeneralizedLinearModel(dtrain.dim,k, biasterm = False)
    trainer = bolt.SGD(bolt.ModifiedHuber(), reg = 0.00001, epochs = 100)
    #trainer = bolt.PEGASOS(reg = 0.001, epochs = 20)
    ova = bolt.OVA(trainer)
    ova.train(model,dtrain)

    ref = [cats[y] for y in dtest.iterlabels()]
    pred = [cats[z] for z in model.predict(dtest.iterinstances())]
    cm = nltk.metrics.ConfusionMatrix(ref, pred)

    print "\n"
    print "="*30
    print "Evaluation".center(30)
    print "="*30
    print "\n"
    print cm.pp()
    
    print "Accuracy: ", nltk.metrics.accuracy(ref, pred)

    print "\n"

    gold = dict([(c,[]) for c in cats.values()])
    for i,c in enumerate(ref):
        gold[c].append(i)

    
    outs = dict([(c,[]) for c in cats.values()])
    for i,c in enumerate(pred):
        outs[c].append(i)

    f1s = []
    print "%s\t%s" % ("Category".ljust(25),"F1".center(6))
    print "-"*38
    for c in cats.values():
        f1 = nltk.metrics.f_measure(set(gold[c]),set(outs[c]))
        print "%s\t%.4f" % (c.ljust(25),f1)
        f1s.append(f1)
    print "-"*38
    print "%s\t%.4f" % ("Mean".ljust(25), np.mean(f1s))

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
