import logging as lg
import HtbConfigBase as HCB
import ROOT as rt
import os


class HtbInputsConfig(HCB.HtbConfigBase):
    def __init__(self, _inputF):
        lg.logging(
            'Start Initialing %s' % (self.__class__.__name__), 'SPECIAL'
        )
        HCB.HtbConfigBase.__init__(self, _inputF)
        self.SearchFile()

    def OpenFile(self):
        OFDict = {}
        for _key, _val in self.FullFN.items():
            FileList = []
            for fn in _val:
                try:
                    rf = rt.TFile(fn, 'r')
                except:
                    lg.logging('Cannot Open File %s' % (fn), 'WART')
                    os._exit(1)
                FileList.append(rf)
            OFDict[_key] = FileList
        self.RootFile = OFDict

    def GetKeys(self):
        return self.RootFile.keys()

    def SearchFile(self):
        full_F = {}
        for _key, _val in self.fConfig.items():
            exf = []
            inf = []
            if 'excludefile' in _val:
                exf = _val['excludefile']
            if 'includefile' in _val:
                inf = _val['includefile']
            try:
                _dir = os.listdir(_val['path'])
            except:
                lg.logging('Cannot Find Path %s' % (_val['path']), 'WARN')
                os._exit(1)

            for _file in _dir:
                if _file in exf:
                    continue
                elif '.root' in _file:
                    inf.append(_val['path'] + _file)
            full_F[_key] = inf
        self.FullFN = full_F

    def PrintConfig(self):
        self.printover(self.FullFN, 0)

    def Get(self, _path):
        spath = _path.strip().split('/')
        try:
            _out = self.RootFile
            for sp in spath:
                if sp is '' or sp is ' ' or sp is '\n':
                    continue
                else:
                    if type(_out) is list:
                        sp = int(sp)
                    _out = _out[sp]
        except:
            lg.logging('Failed to get value, Wrong path', 'WARN')
            _out = None
        return _out

