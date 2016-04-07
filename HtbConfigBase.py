import json
import logging as lg


class HtbConfigBase(object):
    '''The base class of json config file'''
    def __init__(self, _inputF):
        self._djson = self.ReadJson(_inputF)
        self.ConvertToDict()
        pass

    def Get(self, _path):
        spath = _path.strip().split('/')
        try:
            _out = self.fConfig
            for sp in spath:
                if sp is '' or sp is ' ' or sp is '\n':
                    continue
                else:
                    _out = _out[sp]
        except:
            lg.logging('Failed to get value, Wrong path', 'WARN')
            _out = None
        return _out

    def ReadJson(self, _inputF):
        df = file(_inputF)
        dj = json.load(df)
        return dj

    def ConvertToDict(self):
        def loopover(_in):
            tp = type(_in)
            if tp is dict:
                _out = {}
                for _key, _val in _in.items():
                    if type(_key) is unicode:
                        _key = _key.encode()
                    _out[_key] = loopover(_val)
                return _out
            elif tp is list or tp is tuple:
                _out = []
                for _val in _in:
                    _out.append(loopover(_val))
                return _out
            elif tp is unicode:
                return _in.encode()
            else:
                return _in

        self.fConfig = loopover(self._djson)

    def printover(self, _in, nt):
        tp = type(_in)
        t = ''
        n = 0
        while n < nt:
            t = t + '\t'
            n = n + 1
        if tp is dict:
            for _key, _val in _in.items():
                if type(_val) != dict and\
                   type(_val) != list and\
                   type(_val) != tuple:
                    fs = t + str(_key) + ': ' + str(_val)
                    lg.logging(fs)
                else:
                    fs = t + 'Elements in %s :' % (str(_key))
                    lg.logging(fs, 'SPECIAL')
                    self.printover(_val, nt+1)
        elif tp is list or tp is tuple:
            for _val in _in:
                if type(_val) != dict and\
                   type(_val) != list and\
                   type(_val) != tuple:
                    fs = t + str(_val)
                    lg.logging(fs)
                else:
                    fs = t + 'Elements in list :'
                    lg.logging(fs, 'SPECIAL')
                    self.printover(_val, nt+1)
        else:
            fs = t + str(_in)
            lg.logging(fs)

    def PrintConfig(self):
        self.printover(self.fConfig, 0)
