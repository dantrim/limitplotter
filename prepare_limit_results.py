#!/bin/env python
#
# Borrowed from makelistfiles.C
#
# Given the region, signal grid, channel,
# and signal xsec uncertainty this script
# and the path to the results directory
# containing the HistFitter output work-
# spaces this script will produce the harvest
# list files that can then be sued to get
# the limit results
#
# Requirements:
#   - environment 'LIMPLOTDIR'
#   - call setup.sh in your HistFitter area
#     so that you have libSusyFitter.so in
#     your path
#
# Note: here we do not make the histograms
#       but rather will just get the CLs values
#       directly from the list files (as well
#       as the significances)
#
# daniel.joseph.antrim@cern.ch
# July 2016
#

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import os
import sys
sys.path.append(os.environ['LIMPLOTDIR'])

import json

import subprocess
import argparse
import glob

#limitplotter
from limitplotter.utils.stat_tools import *

#HistFitter
ROOT.gSystem.Load("libSusyFitter.so")


def get_final_name() :
    '''
    Return the filename for the concatenated workspace file
    for the requested region, channel, grid, and signal
    uncertainty (syst). Appends 'Output_hypotest' if
    getting hypotest results or 'Output_upperlimit' if
    getting mu_SIG upperlimit results.
    '''

    if grid == "bWN" :
        print 45*"*"
        print " INFO NOT YET CONSIDERING SIGNAL XSEC SYS "
        print " INFO NOT YET CONSIDERING SIGNAL XSEC SYS "
        print " INFO NOT YET CONSIDERING SIGNAL XSEC SYS "
        print 45*"*"

        if upperlimit :
            return "test_%s_%s_%s_Output_upperlimit.root"%(region, channel, grid)
        else :
            #return "test_%s_%s_%s_%s_Output_hypotest.root"%(region, channel, grid, syst)
            return "test_%s_%s_%s_Output_fixSigXSec%s_hypotest.root"%(region, channel, grid, syst)
    else :
        print "get_final_name    ERROR requested grid not supported. Exiting."
        sys.exit()


def hadd_workspace_files() :
    '''
    Concatenate the workspace hypotests for the requested
    region, channel, grid, and signal uncertainty (syst).
    Puts the final file in the same results directory
    as the workspace files (user-provided: results_dir)
    '''

    final_results_filename = get_final_name()

    if grid == "bWN" and syst != "Nominal" :
        print "ERROR currently we only handle the nom case for your grid (%s)"%grid
    #cmd = "hadd -f %s%s %s%s_%s_%s*Output_hypotest.root"%(results_dir, final_results_filename, results_dir, region, channel, grid)
    cmd = "hadd -f %s%s %s%s_%s_%s*Output_fixSigXSec%s_hypotest.root"%(results_dir, final_results_filename, results_dir, region, channel, grid, syst)
    print "hadd_workspace_files    calling %s"%cmd
    subprocess.call(cmd, shell=True)

def make_harvest_list_files() :
    # CollectAndWriteHypoTestResults --> HistFitter/src/toy_utils.cxx
    formatting = ""
    if grid == "bWN" :
        formatting = "hypo_bWN_%f_%f"
    else :
        print "make_harvest_list_files    ERROR requested grid not supported. Exitting."
        sys.exit()
    cut_string = "1"

    inputfile = "%s%s"%(results_dir, get_final_name())
    print "inputfile: %s"%inputfile
    outputfile = ROOT.CollectAndWriteHypoTestResults(inputfile, formatting, "mC1:mN1", cut_string)

def move_list_files() :
    #listdir = "./list_files/%s_%s_%s/"%(region, channel, grid)
    listdir = "./list_files/%s_%s_%s_%s/"%(region, channel, grid, syst)

    cmd = "mkdir -p %s"%listdir
    print "Moving list files to %s"%listdir
    subprocess.call(cmd, shell=True)
    mv_cmd = "mv *harvest_list* %s"%listdir
    subprocess.call(mv_cmd, shell=True)
    #mv_cmd = "mv *tree_description* %s"%listdir
    #subprocess.call(mv_cmd, shell=True)
    return listdir

def humanize_list_files(listdir) :
    '''
    From the produced harvest list json file make a
    more readable limit results file that will
    be used for the plotting

    tree_description key :
        - observed CLs                          : CLs
        - observed CLs - significnace           : StatTools::GetSigma(CLs)
        - expected CLs                          : CLsexp
        - expected CLs - significance           : StatTools::GetSigma(CLsexp)
        - expected CLs +1 sigma                 : clsu1s
        - expected CLs +1 sigma - significance  : StatTools::GetSigma(clsu1s)
        - expected CLs -1 sigma                 : clsd1s
        - expected CLs -1 sigma - significance  : StatTools::GetSigma(clsd1s)
    '''


    in_list = "%stest_%s_%s_%s_Output_fixSigXSec%s_hypotest__1_harvest_list.json"%(listdir, region, channel, grid, syst)
    #in_list = "%stest_%s_%s_%s_%s_Output_hypotest__1_harvest_list.json"%(listdir, region, channel, grid, syst)
    limit_result_dir = "./limit_results_Apr6/%s_%s_%s/"%(region, channel, grid)
    mk_limresult = "mkdir -p %s"%(limit_result_dir)
    subprocess.call(mk_limresult, shell=True)
    out_result = "%s%s_%s_%s_%s_limit_results.txt"%(limit_result_dir, region, channel, grid, syst)
    #out_result = "%s%s_%s_%s_limit_results.txt"%(limit_result_dir, region, channel, grid, syst)

    outfile_template = "mX\tmY\tCLs\tCLsexp\tclsu1s\tclsd1s\tObsSig\tExpSig\tExpSigUp1s\tExpSigDn1s\n"

    ofile = open(out_result, "w")
    ofile.write(outfile_template)

    with open(in_list) as data_file :
       data = json.load(data_file)
       for signal_point in data :
           mx          = str(signal_point['mC1'])
           my          = str(signal_point['mN1'])
           cls         = str(signal_point['CLs'])
           clsexp      = str(signal_point['CLsexp'])
           clsexp_u1s  = str(signal_point['clsu1s'])
           clsexp_d1s  = str(signal_point['clsd1s'])

           obsSig = "%.2f"%ROOT.StatTools.GetSigma(float(cls))
           expSig = "%.2f"%ROOT.StatTools.GetSigma(float(clsexp))
           expSigUp1s = "%.2f"%ROOT.StatTools.GetSigma(float(clsexp_u1s))
           expSigDn1s = "%.2f"%ROOT.StatTools.GetSigma(float(clsexp_d1s))

           out_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(mx, my, cls, clsexp, clsexp_u1s, clsexp_d1s, obsSig, expSig, expSigUp1s, expSigDn1s)  
           ofile.write(out_line)

    print "Writing humanized limit results to %s"%out_result
    ofile.closed

def gather_upperlimit_results() :
    print "gatther_upperlimit_results    THIS METHOD IS NOT IMPLEMENTED YET"


###############################################################
if __name__=="__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region")
    parser.add_argument("-c", "--channel")
    parser.add_argument("-g", "--grid")
    parser.add_argument("-s", "--syst", help="Up, Down, or Nominal")
    parser.add_argument("-u", "--upperlimit", action="store_true", default = False)
    parser.add_argument("-d", "--results_dir", required=True)
    args = parser.parse_args()

    global region, channel, grid, syst, upperlimit, results_dir
    region = args.region
    channel = args.channel
    grid = args.grid
    syst = args.syst
    upperlimit = args.upperlimit
    results_dir = args.results_dir
    

    # check that the results directory exists
    if not os.path.isdir(args.results_dir) :
        print "ERROR    Results directory (%s) does not exits. Exiting."%args.results_dir
        sys.exit()
    if not results_dir.endswith("/") : results_dir += "/"

    if not upperlimit :
        # concatenate (hadd) all results
        hadd_workspace_files()

        # get the interprtation (sets axes on the TH2's and is based
        # on the workspace filename structure
        # remember: for TH2 --> y:x
        interpretation = ""
        if grid=="bWN" : interpreation = "mN1:mC1"
        else :
            print "ERROR Interpretation for requested grid (%s) unavailable. Exiting."%(grid)
            sys.exit()

        # make the harvest list files useing the concatenated
        # hypotest results
        make_harvest_list_files()

        # move the produced harvest_list_files to the list_files directory
        list_file_dir = move_list_files()
        

        # produce human readable limit results
        #list_file_dir = "/data/uclhc/uci/user/dantrim/n0225val/limitplotter/list_files/SRwt_sfdf_bWN/"
        humanize_list_files(list_file_dir)


    if upperlimit :
        # gatter the upper limit on mu_SIG results
        # this does scan of the logs that were made
        # when running the limit on the workspace
        gather_upperlimit_results()
