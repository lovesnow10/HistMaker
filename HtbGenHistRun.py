import logging as lg
import HtbRunBase as HRB
import ROOT as rt
import util


class HtbLoopFile(HRB.HtbRunBase):
    def __init__(self, Name, LoopData, XSFile, Lumi):
        lg.logging(
            'Starting Initialing %s' % (self.__class__.__name__), 'SPECIAL'
        )
        HRB.HtbRunBase.__init__(self, LoopData)
        self.Xsection = XSFile
        self.Name = Name
        self.Lumi = Lumi
        self.Norm = {}
        self.ZLRW = [361372, 361375, 361378, 361381, 361384, 361387, 361390, 361393, 361396,
                     361399, 361402, 361405, 361408, 361411, 361414, 361417, 361420, 361423,
                     361426, 361429, 361432, 361435, 361438, 361441, 361468, 361470, 361472,
                     361474, 361476, 361478, 361480, 361482, 361484, 361486, 361488, 361490]
        self.ZHRW = [361374, 361377, 361380, 361383, 361386, 361389, 361392, 361395, 361398,
                     361401, 361404, 361407, 361410, 361413, 361416, 361419, 361422, 361425,
                     361428, 361431, 361434, 361437, 361440, 361443, 361469, 361471, 361473,
                     361475, 361477, 361479, 361481, 361483, 361485, 361487, 361489, 361491]
        self.HFcut = {"tt+bb": "abs(HF_Classification) >= 100",
                      "tt+cc": "abs(HF_Classification) > 0 && abs(HF_Classification) < 100",
                      "tt+light": "abs(HF_Classification) <= 0"}
        if 'data' not in self.Name:
            self.CalNorm()

    def _getName(self, rf):
        fn = rf.GetName()
        fn = fn.split('/')[-1]
        if 'data' in fn:
            i = fn.find('.root')
            return fn[0:i]
        else:
            fn = fn.split('.')[1]
            return fn

    def LoopOver(self, Var, Cut, Bins, Weights):
        varHist = []
        hout = []
        for f in self.DataToLoop:
            fn = self._getName(f)
            lg.logging('\tRunning %s' % (fn), 'SPECIAL')
            varHist.append(self.Do(f, fn, Var, Cut, Bins, Weights))
        if self.Name != "ttbar":
            hn = Var + '_of_' + self.Name
            hist = rt.TH1F(
                self.Name,
                hn,
                Bins['nbin'],
                Bins['xlow'],
                Bins['xup']
            )
            hist.Sumw2()
            for hl in varHist:
                for fn, h in hl.items():
                    hist.Add(h)
            hout.append(hist)
            return hout
        else:
            hn1 = Var + '_of_' + "ttbb"
            hn2 = Var + '_of_' + "ttcc"
            hn3 = Var + '_of_' + "ttlight"
            hist1 = rt.TH1F(
                "tt+bb",
                hn1,
                Bins['nbin'],
                Bins['xlow'],
                Bins['xup']
            )
            hist1.Sumw2()
            hist2 = rt.TH1F(
                "tt+cc",
                hn2,
                Bins['nbin'],
                Bins['xlow'],
                Bins['xup']
            )
            hist2.Sumw2()
            hist3 = rt.TH1F(
                "tt+light",
                hn3,
                Bins['nbin'],
                Bins['xlow'],
                Bins['xup']
            )
            hist3.Sumw2()
            for hl in varHist:
                hist1.Add(hl["tt+bb"])
                hist2.Add(hl["tt+cc"])
                hist3.Add(hl["tt+light"])
            hout.append(hist1)
            hout.append(hist2)
            hout.append(hist3)
            return hout

    def Do(self, f, fn, Var, Cut, Bins, Weights):
        hl = {}
        if self.Name != 'ttbar':
            hist = rt.TH1F(fn, '', Bins['nbin'], Bins['xlow'], Bins['xup'])
            hist.Sumw2()
            hl[fn] = hist
        else:
            hist1 = rt.TH1F(fn+"_tt+bb", '', Bins['nbin'], Bins['xlow'], Bins['xup'])
            hist1.Sumw2()
            hl["tt+bb"] = hist1
            hist2 = rt.TH1F(fn+"_tt+cc", '', Bins['nbin'], Bins['xlow'], Bins['xup'])
            hist2.Sumw2()
            hl["tt+cc"] = hist2
            hist3 = rt.TH1F(fn+"_tt+light", '', Bins['nbin'], Bins['xlow'], Bins['xup'])
            hist3.Sumw2()
            hl["tt+light"] = hist3
        tree = f.Get('nominal')
#        selc = rt.TTreeFormula("selc", Cut, tree)
#        selHF = 0
#        if self.Name == 'tt+bb':
#            selHF = rt.TTreeFormula("selHF", self.HFcut['tt+bb'], tree)
#        if self.Name == 'tt+cc':
#            selHF = rt.TTreeFormula("selHF", self.HFcut['tt+cc'], tree)
#        if self.Name == 'tt+light':
#            selHF = rt.TTreeFormula("selHF", self.HFcut['tt+light'], tree)

#        for ientry in xrange(0, tree.GetEntries()):
#            tree.GetEntry(ientry)
#            if not selc.EvalInstance():
#                continue
#            if selHF != 0:
#                if not selHF.EvalInstance():
#                    continue
#            dsid = getattr(tree, "mcChannelNumber")
#            dil_filter = 0
#            ttb_filter = 0
#            if not 'data' in fn:
#                dil_filter = getattr(tree, "truth_top_dilep_filter")
#                ttb_filter = getattr(tree, "TopHeavyFlavorFilterFlag")
#   
#            if dsid == 410000:
#                if dil_filter == 1 or ttb_filter == 5:
#                    continue
#            if dsid == 410120:
#                if dil_filter == 1:
#                    continue
#            if dsid == 410009:
#                if ttb_filter == 5:
#                    continue
#            nE = getattr(tree, "nElectrons")
#            nM = getattr(tree, "nMuons")
#            if not 'data' in fn:
#                eltruthtype = getattr(tree, "el_true_type")
#                mutruthtype = getattr(tree, "mu_true_type")
#                if nE == 2 and nM == 0:
#                    if eltruthtype[0] != 2 or eltruthtype[1] != 2:
#                        continue
#                elif nE == 0 and nM == 2:
#                    if mutruthtype[0] != 6 or mutruthtype[1] != 6:
#                        continue
#                elif nE == 1 and nM == 1:
#                    if mutruthtype[0] != 6 or eltruthtype[0] != 2:
#                        continue
#            _value = -1
#            if Var == 'pT_jet1':
#                _value = getattr(tree, "jet_pt")[0]
#            elif Var == 'pT_jet2':
#                _value = getattr(tree, "jet_pt")[1]
#            elif Var == 'eta_jet1':
#                _value = getattr(tree, "jet_eta")[0]
#            elif Var == 'eta_jet2':
#                _value = getattr(tree, "jet_eta")[1]
#            elif Var == 'phi_jet1':
#                _value = getattr(tree, "jet_phi")[0]
#            elif Var == 'phi_jet2':
#                _value = getattr(tree, "jet_phi")[1]
#            elif Var in ['pT_bJet1', 'eta_bJet1', 'phi_bJet1']:
#                mv2c20 = getattr(tree, "jet_mv2c20")
#                ib = 0
#                for ib in xrange(0, getattr(tree, "nJets")):
#                    if mv2c20[ib] > -0.4434:
#                        break
#                if Var == 'pT_bJet1':
#                    _value = getattr(tree, "jet_pt")[ib]
#                elif Var == 'eta_bJet1':
#                    _value = getattr(tree, "jet_eta")[ib]
#                elif Var == 'phi_bJet1':
#                    _value = getattr(tree, "jet_phi")[ib]
#            elif Var in ['pT_lep1', 'pT_lep2', 'eta_lep1', 'eta_lep2', 'phi_lep1', 'phi_lep2']:
#                if nE == 2 and nM == 0:
#                    if Var == 'pT_lep1':
#                        _value = getattr(tree, "el_pt")[0]
#                    elif Var == 'pT_lep2':
#                        _value = getattr(tree, "el_pt")[1]
#                    elif Var == 'eta_lep1':
#                        _value = getattr(tree, "el_eta")[0]
#                    elif Var == 'eta_lep2':
#                        _value = getattr(tree, "el_eta")[1]
#                    elif Var == 'phi_lep1':
#                        _value = getattr(tree, "el_phi")[0]
#                    elif Var == 'phi_lep2':
#                        _value = getattr(tree, "el_phi")[1]
#                elif nE == 0 and nM == 2:
#                    if Var == 'pT_lep1':
#                        _value = getattr(tree, "mu_pt")[0]
#                    elif Var == 'pT_lep2':
#                        _value = getattr(tree, "mu_pt")[1]
#                    elif Var == 'eta_lep1':
#                        _value = getattr(tree, "mu_eta")[0]
#                    elif Var == 'eta_lep2':
#                        _value = getattr(tree, "mu_eta")[1]
#                    elif Var == 'phi_lep1':
#                        _value = getattr(tree, "mu_phi")[0]
#                    elif Var == 'phi_lep2':
#                        _value = getattr(tree, "mu_phi")[1]
#                else:
#                    elpt = getattr(tree, "el_pt")[0]
#                    mupt = getattr(tree, "mu_pt")[0]
#                    if elpt > mupt:
#                        if Var == 'pT_lep1':
#                            _value = getattr(tree, "el_pt")[0]
#                        elif Var == 'pT_lep2':
#                            _value = getattr(tree, "mu_pt")[0]
#                        elif Var == 'eta_lep1':
#                            _value = getattr(tree, "el_eta")[0]
#                        elif Var == 'eta_lep2':
#                            _value = getattr(tree, "mu_eta")[0]
#                        elif Var == 'phi_lep1':
#                            _value = getattr(tree, "el_phi")[0]
#                        elif Var == 'phi_lep2':
#                            _value = getattr(tree, "mu_phi")[0]
#                    elif mupt > elpt:
#                        if Var == 'pT_lep1':
#                            _value = getattr(tree, "mu_pt")[0]
#                        elif Var == 'pT_lep2':
#                            _value = getattr(tree, "el_pt")[0]
#                        elif Var == 'eta_lep1':
#                            _value = getattr(tree, "mu_eta")[0]
#                        elif Var == 'eta_lep2':
#                            _value = getattr(tree, "el_eta")[0]
#                        elif Var == 'phi_lep1':
#                            _value = getattr(tree, "mu_phi")[0]
#                        elif Var == 'phi_lep2':
#                            _value = getattr(tree, "el_phi")[0]
#            else:
#                _value = getattr(tree, Var)
#
#            if 'data' in fn:
#                hl[fn].Fill(_value)
#            else:
#                weights = []
#                for w in Weights:
#                    weights.append(getattr(tree, w))
#                weight = 1
#                for w in weights:
#                    weight = weight * w
#                if dsid in self.ZLRW:
#                    weight = weight * 0.878
#                if dsid in self.ZHRW:
#                    weight = weight * 1.135
#                if self.Name != "ttbar":
#                    hl[fn].Fill(_value, weight)
#                else:
#                    hf = getattr(tree, "HF_Classification")
#                    if hf >= 100:
#                        hl["tt+bb"].Fill(_value, weight)
#                    elif hf >0 and hf < 100:
#                        hl["tt+cc"].Fill(_value, weight)
#                    else:
#                        hl["tt+light"].Fill(_value, weight)
#                    
#        if not 'data' in fn:
#            for f, h in hl.items():
#                h.Scale(self.Norm[fn])
#        return hl

        if 'data' in fn:
            tree.Project(fn, Var, Cut)
            return hl
        weight = ''
        for w in Weights:
            weight = weight + w + ' * '
        tree.GetEntry(0)
        dsid = getattr(tree, "mcChannelNumber")
        if dsid in self.ZLRW:
            weight = weight + '0.878' + ' * '
        if dsid in self.ZHRW:
            weight = weight + '1.135' + ' * '
        Cut = Cut + ' && ' + 'FakeRemoval == 1'
#        if self.Name == "tt+bb":
#            Cut = Cut + ' + ' + self.HFcut['tt+bb']
#        if self.Name == "tt+cc":
#            Cut = Cut + ' + ' + self.HFcut['tt+cc']
#        if self.Name == "tt+light":
#            Cut = Cut + ' + ' + self.HFcut['tt+light']
        if dsid == 410000:
            Cut = Cut + ' && ' + 'truth_top_dilep_filter != 1'
            Cut = Cut + ' && ' + 'TopHeavyFlavorFilterFlag != 5'
        if dsid == 410009:
            Cut = Cut + ' && ' + 'TopHeavyFlavorFilterFlag != 5'
        if dsid == 410120:
            Cut = Cut + ' && ' + 'truth_top_dilep_filter != 1'
        if self.Name != "ttbar":
            totalw = weight + '(' + Cut + ')'
            tree.Project(fn, Var, totalw)
            hl[fn].Scale(self.Norm[fn])
            return hl
        else:
            cut1 = Cut + ' && ' + self.HFcut['tt+bb']
            cut2 = Cut + ' && ' + self.HFcut['tt+cc']
            cut3 = Cut + ' && ' + self.HFcut['tt+light']
            totalw1 = weight + '(' + cut1 + ')'
            totalw2 = weight + '(' + cut2 + ')'
            totalw3 = weight + '(' + cut3 + ')'
            tree.Project(fn+'_tt+bb', Var, totalw1)
            tree.Project(fn+'_tt+cc', Var, totalw2)
            tree.Project(fn+'_tt+light', Var, totalw3)
            hl['tt+bb'].Scale(self.Norm[fn])
            hl['tt+cc'].Scale(self.Norm[fn])
            hl['tt+light'].Scale(self.Norm[fn])
            return hl
#        pass


    def CalNorm(self):
        for f in self.DataToLoop:
            fn = self._getName(f)
            if fn in self.Xsection:
                _xs = self.Xsection[fn]
            else:
                _xs = 1
            norm = util.CalNorm(_xs, self.Lumi, f)
#            norm = util.CalNorm2(_xs, self.Lumi, f)
            self.Norm[fn] = norm


class HtbLoopVar(HRB.HtbRunBase):
    '''Main horse for working'''
    def __init__(self, varConfig, FileList):
        lg.logging(
            'Start Initialing %s' % (self.__class__.__name__), 'SPECIAL'
        )
        HRB.HtbRunBase.__init__(self, {})
        self.varConfig = varConfig
        self.FileList = FileList

    def LoopOver(self):
        self.output = util.CreateRootFile(self.varConfig.General['output'])
        for _cut in self.varConfig.CutList:
            print '#####################################'
            lg.logging('Processing Cut %s' % (_cut))
            PlotDir1 = self.output.mkdir(_cut)
            PlotDir1.cd()
            for _var in self.varConfig.Vars[_cut]:
                lg.logging('\tProcessing Variable %s' % (_var))
                PlotDir2 = PlotDir1.mkdir(_var)
                PlotDir2.cd()
                for fl in self.FileList:
                    weights = [
                        'weight_mc',
                        'weight_leptonSF',
                        'weight_bTagSF_77',
                        'weight_pileup',
                        'weight_jvt'
                    ]
                    hl = fl.LoopOver(
                        _var,
                        self.varConfig.Cuts[_cut],
                        self.varConfig.fConfig[_cut][_var],
                        weights
                    )
                    for hist in hl:
                        hist.SetDirectory(PlotDir2)
                        hist.Write()
                lg.logging('Variable %s Done' % (_var), 'SUCCESS')
            lg.logging('Cut %s Done' % (_cut), 'SUCCESS')
        self.output.Close()
