import os
import json
import ROOT
import logging as lg


def checkDir(_dir):
    if _dir[-1] == '/':
        return _dir
    else:
        return _dir + '/'


def MakeDir(_dir):
    try:
        os.mkdir(_dir)
    except:
        print '\33[31m%s already exists\33[0m' % (_dir)
    return

def GetData(p):
    _path = p.split('/')[0:-1]
    path = '/'.join(_path)
    return checkDir(path)

def getFile(dirs):
    filename = []
    for _dir in dirs:
        if os.path.isdir(_dir):
            _dir = checkDir(_dir)
            print 'Finding files in ', _dir
            dirL = os.listdir(_dir)

            for f in dirL:
                if '.root' not in f:
                    continue
                f = _dir + f
                if os.path.isfile(f):
                    if os.path.splitext(f)[1] == '.root':
                        filename.append(f)
        else:
            print 'Warning!', _dir, ' is not a dir, please check!'

    return filename

def FileCloser(data):
    for _name, subdata in data.items():
        for subname, f in subdata.items():
            f.Close()


def CreateRootFile(rootfilename):
    ext = os.path.splitext(rootfilename)[1]
    if ext == '':
        print 'automatically adding .root'
        rootfilename = rootfilename + '.root'
    elif ext != '' and ext != '.root':
        print 'extension name found, but is not .root,'\
            'automatically adding .root'
        rootfilename = rootfilename + '.root'
    else:
        print '.root extension name found'

    if os.path.exists(rootfilename):
        print 'the same name rootfile found, will be overloaded'

    return ROOT.TFile(rootfilename, 'recreate')


def getTotalEventsWeighted(rfile):
    try:
        tree = rfile.Get('sumWeights')
    except:
        print 'Cannot find tree "sumWeights"...Quit...'
        os._exit(1)
    Ntotal = 0
    nentries = tree.GetEntriesFast()
    for ientry in xrange(nentries):
        tree.GetEntry(ientry)
        Ntotal += tree.totalEventsWeighted
    return Ntotal


def getFirstBinContent(rfile):
    h = rfile.Get('ee/cutflow_mc_pu_zvtx')
    return h.GetBinContent(1)


def CalNorm(xs, lumi, rfile):
    Ntotal = getTotalEventsWeighted(rfile)
    return lumi * xs / Ntotal


def CalNorm2(xs, lumi, rfile):
    Ntotal = getFirstBinContent(rfile)
    return lumi * xs / Ntotal


def XsecInit(xfilename):
    xsecf = open(xfilename)
    output = {}
    lns = xsecf.readlines()
    for ln in lns:
        if ln.strip() == '':
            continue
        elif ln.strip()[0] == '#':
            continue

        sln = ln.strip()
        if '\t' in sln:
            sln = sln.expandtabs(1)
        s = sln.split(' ')
        ss = [i for i in s if i != '']
        try:
            output[str(ss[0])] = float(ss[1]) * float(ss[2])
        except:
            print 'XSection file error, ID %s' % (str(ss[0]))
    lg.logging('Done', 'SUCCESS')
    return output

def GetHist(rf, _path):
    hist = rf.Get(_path)
    return hist


