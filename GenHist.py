#!/usr/bin/env python

import HtbGenHistConfig as HGHC
import HtbGenHistRun as HGHR
import HtbInputsConfig as HIC
import sys
import os
import util

if __name__ == '__main__':
    Inputs = HIC.HtbInputsConfig(sys.argv[2])
    Inputs.OpenFile()
    Config = HGHC.HtbGenHistConfig(sys.argv[1])

    InputsNames = Inputs.GetKeys()
    xf = os.environ['MYANALYSIS'] +\
        '/' + 'XSection-MC15-13TeV-fromSusyGrp.data'
    xsec = util.XsecInit(xf)
    HLFL = []
    for IN in InputsNames:
        _hlfl = HGHR.HtbLoopFile(
            IN,
            Inputs.Get(IN),
            xsec,
            Config.General['lumi']
        )
        HLFL.append(_hlfl)

    MainRun = HGHR.HtbLoopVar(Config, HLFL)
    MainRun.LoopOver()
