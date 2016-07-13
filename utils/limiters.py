#
# Class for each region and signal point
#
# daniel.joseph.antrim@cern.ch
# July 2016
#

import ROOT


class Region() :
    def __init__(self, name_) :
        self.name   = name_
        self.color  = None
        self.shape  = None

        self.nominal_limit_results_file = ""
        self.up_limit_results_file = ""
        self.dn_limit_results_file = ""

    def Print(self) :
        print "Region:  %s"%self.name

class Signal() :
    def __init__(self, mX_, mY_) :
        self.mX = mX_
        self.mY = mY_


        ####################################
        ## CLs
        ####################################
        self.observedCLs                = {}    ### < { region : CLs }
        self.expectedCLs                = {}    ### < { region : CLs }
        self.expectedCLsUp1s            = {}    ### < { region : CLs }
        self.expectedCLsDn1s            = {}    ### < { region : CLs }

        ###################################
        ## Significance
        ###################################
        self.observedSig                = {}    ### < { region : sig }
        self.expectedSig                = {}    ### < { region : sig }
        self.expectedSigUp1s            = {}    ### < { region : sig }
        self.expectedSigDn1s            = {}    ### < { region : sig }

        ###################################
        ## observed CLs (up/down) with
        ## signal xsec uncertainy variations
        ###################################
        self.observedCLsUp1s            = {}    ### < { region : CLs }
        self.observedCLsDn1s            = {}    ### < { region : CLs }

        ###################################
        ## observed significance (up/down) with
        ## signal xsec uncertainy variations
        ###################################
        self.observedSigUp1s            = {}    ### < { region : sig }
        self.observedSigDn1s            = {}    ### < { region : sig }


        #####################################
        ## if doing PWC store the besties
        #####################################
        self.bestRegion = ""                    ### < region with largest significance

        # CLs
        self.bestObservedCLs        = 0.0       ### < observed CLs for point in best region
        self.bestExpectedCLs        = 0.0       ### < expected CLs for point in best region
        self.bestExpectedCLsUp1s    = 0.0       ### < expected CLs +1 sigma for point in best region
        self.bestExpectedCLsDn1s    = 0.0       ### < expected CLs -1 sigma for point in best region

        # significance
        self.bestObservedSig        = 0.0       ### < observed significnace for point in best region
        self.bestExpectedSig        = 0.0       ### < expected significance for point in best region
        self.bestExpectedSigUp1s    = 0.0       ### < expected significance +1 sigma for point in best region
        self.bestExpectedSigDn1s    = 0.0       ### < expected significance -1 sigma for point in best region

        # observed CLs with signal xsec variation
        self.bestObservedCLsUp1s    = 0.0       ### < observed CLs sigma_theory +1
        self.bestObservedCLsDn1s    = 0.0       ### < observed CLs sigma_theory -1

        # observed significnace with signal xsec variation
        self.bestObservedSigUp1s    = 0.0       ### < observed significnace sigma_theory +1
        self.bestObservedSigDn1s    = 0.0       ### < observed significance sigma_theory -1
    
    def Print(self) :
        print "Signal: (%.1f,%.1f)"%(float(self.mX), float(self.mY))


        
