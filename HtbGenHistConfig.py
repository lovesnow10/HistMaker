import logging as lg
import HtbConfigBase as HCB


class HtbGenHistConfig(HCB.HtbConfigBase):
    def __init__(self, _inputF):
        lg.logging(
            'Start Initialing %s' % (self.__class__.__name__), 'SPECIAL'
        )
        HCB.HtbConfigBase.__init__(self, _inputF)
        self.DecorateConfig()
        self.General = self.fConfig['General']
        self.CutList = self.fConfig.keys()
        self.CutList.remove('General')
        self.Cuts = {}
        self.Vars = {}
        for cut in self.CutList:
            self.Cuts[cut] = self.fConfig[cut]['cut']
            self.Vars[cut] = self.fConfig[cut].keys()
            self.Vars[cut].remove('cut')

    def DecorateConfig(self):
        for _key, _val in self.fConfig.items():
            if _key == 'General' or _key == 'VARSET':
                continue
            else:
                if 'VARSET' not in _val:
                    if 'varlist' in _val:
                        for _var, _set in _val['varlist'].items():
                            self.fConfig[_key][_var] = _set
                        del self.fConfig[_key]['varlist']
                    continue
                else:
                    _varset = _val['VARSET']
                    for _var, _set in self.fConfig['VARSET'][_varset].items():
                        self.fConfig[_key][_var] = _set
                    if 'varlist' in _val:
                        for _var, _set in _val['varlist'].items():
                            self.fConfig[_key][_var] = _set
                        del self.fConfig[_key]['varlist']
                    del self.fConfig[_key]['VARSET']
        del self.fConfig['VARSET']
