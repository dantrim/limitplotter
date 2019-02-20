#
# Class for the grid configuration
#
# daniel.joseph.antrim@cern.ch
# July 2016
#

import ROOT
import os
import glob

import sys
sys.path.append(os.environ['LIMPLOTDIR'])

#limitplotter
from limitplotter.utils.limiters import *

class GridConfiguration() :
    def __init__(self, grid_) :
        self.name = "%s_grid_configuration"%grid_
        self.grid = grid_

        # display names for the regions
        self.displaynames = {}

        # lepton channel, if any
        self.channel = ""

        self.regions = []

        # container for the signal grid
        self.signals = []

        # canvas for limit plot
        self.limit_canvas = ROOT.TCanvas("c_limit", "", 768, 768)
        self.do_limit_plot = True
        self.show_obs_cls = False
        self.show_exp_cls = True
        self.show_obs_sig = False
        self.show_exp_sig = False

        # whether or not to make the best-sr-per-point plot
        self.do_best_sr_per_point = False
        self.best_sr_canvas = ROOT.TCanvas("c_bestSR", "", 768, 768)

        # whether or not to make the upperlimit-xsec-per-point plot
        self.do_xsec_plot = False
        self.xsec_canvas = ROOT.TCanvas("c_upXS", "", 768, 768)

        # whether or not to plot previous 8 TeV results
        self.show_previous_8TeV_result = False

    def collect_region_limit_result_files(self, r) :
        lim_results_dir = str(os.environ['LIMPLOTDIR'])
        if not lim_results_dir.endswith("/") : lim_results_dir += "/"
        lim_results_dir += "limitplotter/limit_results/"

        if self.channel != "" :
            in_lim_dir = "%s_%s_%s/"%(r.name, self.channel, self.grid)

            nom = glob.glob("%s%s*Nominal_limit_results.txt"%(lim_results_dir, in_lim_dir))
            up  = glob.glob("%s%s*Up_limit_results.txt"%(lim_results_dir, in_lim_dir))
            dn  = glob.glob("%s%s*Down_limit_results.txt"%(lim_results_dir, in_lim_dir))

            if len(nom) > 0 and len(nom) == 1 :
                print "collect_region_limit_result_files    nominal limit results file: %s"%nom[0]
                r.nominal_limit_results_file = nom[0]
            else :
                print "collect_region_limit_result_files    ERROR nominal limit results file (%s%s*Nominal_limit_results.txt) not found"%(lim_results_dir, in_lim_dir)
                sys.exit()
            if len(up) > 0 and len(up) == 1 :
                print "collect_region_limit_result_files    up limit results file: %s"%up[0]
                r.up_limit_results_file = up[0]
            else :
                print "collect_region_limit_result_files    ERROR up limit results file (%s%s*Up_limit_results.txt) not found"%(lim_results_dir, in_lim_dir)
                #sys.exit()
            if len(dn) > 0 and len(dn) == 1 :
                print "collect_region_limit_result_files    down limit results file: %s"%dn[0]
                r.dn_limit_results_file = dn[0]
            else :
                print "collect_region_limit_result_files    ERROR down limit results file (%s%s*Down_limit_results.txt) not found"%(lim_results_dir, in_lim_dir)
                #sys.exit()
        else :
            print "collect_region_limit_result_files    You must provide a signal channel!"
            sys.exit()

    def collect_limit_result_files(self) :
        for reg in self.regions :
            self.collect_region_limit_result_files(reg)

    def assign_grid(self) :
        columns = "mX mY CLs CLsexp  clsu1s  clsd1s  ObsSig  ExpSig  ExpSigUp1s  ExpSigDn1s"
        fields = columns.split(" ")
        mXidx = fields.index("mX")
        mYidx = fields.index("mY")
        nom_file = self.regions[0].nominal_limit_results_file
        lines = open(nom_file).readlines()
        for line in lines[1:] : # first line is the header
            line = line.strip()
            if not line : continue
            cols = line.split()
            #cols = line.split("\t")
            mX = float(cols[mXidx])
            mY = float(cols[mYidx])
            s = Signal(mX, mY)
            self.signals.append(s)

        print "assign_grid    %s total grid points"%len(self.signals)

    def fill_raw_results(self) :
        columns = "mX mY CLs CLsexp clsu1s clsd1s ObsSig ExpSig ExpSigUp1s ExpSigDn1s" 
        fields = columns.split(" ")
        mXidx           = fields.index("mX")
        mYidx           = fields.index("mY")
        CLsidx          = fields.index("CLs")
        CLsexpidx       = fields.index("CLsexp")
        CLsUp1sidx      = fields.index("clsu1s")
        CLsDn1sidx      = fields.index("clsd1s")
        obsSigidx       = fields.index("ObsSig")
        expSigidx       = fields.index("ExpSig")
        expSigUp1sidx   = fields.index("ExpSigUp1s")
        expSigDn1sidx   = fields.index("ExpSigDn1s")

        # fill the "nominal" raw results
        for r in self.regions :
            print "fill_raw_results    %s"%r.name
            if r.nominal_limit_results_file != "" :
                nom_file = r.nominal_limit_results_file
                lines = open(nom_file).readlines()
                for line in lines[1:] :
                    line = line.strip()
                    if not line : continue
                    cols = line.split()
                    #cols = line.split("\t")
                    mX = float(cols[mXidx])
                    mY = float(cols[mYidx])
                    for s in self.signals :
                        if s.mX == mX and s.mY == mY :
                            # raw CLs
                            s.observedCLs[r.name]       = float(cols[CLsidx])
                            s.expectedCLs[r.name]       = float(cols[CLsexpidx])
                            s.expectedCLsUp1s[r.name]   = float(cols[CLsUp1sidx])
                            s.expectedCLsDn1s[r.name]   = float(cols[CLsDn1sidx])
                            # significance
                            s.observedSig[r.name]       = float(cols[obsSigidx])
                            s.expectedSig[r.name]       = float(cols[expSigidx])
                            s.expectedSigUp1s[r.name]   = float(cols[expSigUp1sidx])
                            s.expectedSigDn1s[r.name]   = float(cols[expSigDn1sidx])
            else :
                print "fill_raw_results    ERROR nominal limit results file is \"\""
                sys.exit()

            if r.up_limit_results_file != "" :
                up_file = r.up_limit_results_file
                lines = open(up_file).readlines()
                for line in lines[1:] :
                    line = line.strip()
                    if not line : continue
                    #cols = line.split("\t")
                    cols = line.split()
                    mX = float(cols[mXidx])
                    mY = float(cols[mYidx])
                    for s in self.signals :
                        if s.mX == mX and s.mY == mY :
                            # up obs CLs
                            s.observedCLsUp1s[r.name]   = float(cols[CLsidx])
                            # up obs Sig
                            s.observedSigUp1s[r.name]   = float(cols[obsSigidx])

            else :
                print "fill_raw_results    ERROR up limits results file is \"\""
                #sys.exit()

            if r.dn_limit_results_file != "" :
                dn_file = r.dn_limit_results_file
                lines = open(dn_file).readlines()
                for line in lines[1:] :
                    line = line.strip()
                    if not line : continue
                    cols = line.split()
                    #cols = line.split("\t")
                    mX = float(cols[mXidx])
                    mY = float(cols[mYidx])
                    for s in self.signals :
                        if s.mX == mX and s.mY == mY :
                            # down obs CLs
                            s.observedCLsDn1s[r.name]   = float(cols[CLsidx])
                            # down obs Sig
                            s.observedSigDn1s[r.name]   = float(cols[obsSigidx])
            else :
                print "fill_raw_results    ERROR down limit results file is \"\""
                #sys.exit()
