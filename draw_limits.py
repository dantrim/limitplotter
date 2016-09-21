#
# this script will parse the limit results in the
# limit_results directory, build the signal points,
# and make the limit plots
#
# daniel.joseph.antrim@cern.ch
# July 2016
#

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 3001;" )

import os
import sys
sys.path.append(os.environ['LIMPLOTDIR'])

from optparse import OptionParser
import glob
import operator # itemgetter

# limitplotter
from limitplotter.utils.grid_configuration import *
from limitplotter.utils.limit_plot_tools import *

def get_configuration(grid) :
    configuration_file = ""
    if grid == "bWN" :
        configuration_file = "SRwt_sfdf.py"
    else :
        print "get_configuration    ERROR unsupported grid. Exiting."
        sys.exit()

    print "get_configuration    grabbing configuration file (%s)"%configuration_file
    return configuration_file

def make_best_sr_plot(conf) :
    print "make_best_sr_plot    THIS METHOD IS NOT IMPLEMENTED"
    sys.exit()

def draw_sig_or_cls(conf, reg_="", pwc=False) :

    print "draw_sig_or_cls    NEED TO HANDLE PWC CASE"
    c = conf.limit_canvas
    c.cd()

    tex = ROOT.TLatex(0.0,0.0,"")
    tex.SetTextFont(42)
    tex.SetTextSize(0.35 * tex.GetTextSize())
    #tex.SetTextSize(0.5 * tex.GetTextSize())
    markers = []
    for s in conf.signals :
        val, x, y = 0.0, 0.0, 0.0
        x = float(s.mX)
        y = float(s.mY)
        if x > 400 : continue
        if conf.show_exp_cls :
            val = float(s.expectedCLs[reg_])
        elif conf.show_obs_cls :
            val = float(s.observedCLs[reg_])
        elif conf.show_obs_sig :
            val = float(s.observedSig[reg_])
        elif conf.show_exp_sig :
            val = float(s.expectedSig[reg_])

        #if "SRwt" in reg_ and y > 300 : continue

        tex.DrawLatex(x, y, "%.2f"%float(val))

    z_title = ""
    if   conf.show_exp_cls : z_title = "Numbers give the expected CL_{s} values"
    elif conf.show_obs_cls : z_title = "Numbers give the observed CL_{s} values"
    elif conf.show_obs_sig : z_title = "Numbers give the observed Significance"
    elif conf.show_exp_sig : z_title = "Numbers give the expected Significance"

    draw_text(0.96,0.38,ROOT.kBlack,z_title,angle=90.0, size=0.03)
    #draw_text(0.96,0.44,ROOT.kBlack,z_title,angle=90.0, size=0.03)
    c.Update()

def draw_upperlimit_xsec(conf) :
    print "draw_upperlimit_xsec    THIS METHOD IS NOT IMPLEMENTED"

def get_limit_output_name(conf) :
    outname = ""
    outname += "limplot_"
    outname += conf.base_region
    outname += "_"
    outname += conf.grid
    outname += "_"
    if conf.channel != "" :
        outname += conf.channel
        outname += "_"
    if conf.do_xsec_plot : outname += "exclXS"
    elif conf.show_exp_cls : outname += "expCLs"
    elif conf.show_obs_cls : outname += "obsCLs"
    elif conf.show_exp_sig : outname += "expSig"
    elif conf.show_obs_sig : outname += "obsSig" 
    outname += ".eps"
    return outname

def get_forbiddenlines(conf) :

    out_lines = []

    if grid == "bWN" :

        x_low = conf.xlow
        y_low = conf.ylow

        # mW line
        y_high_w = 320
        slope = 1.0
        y_w = slope * x_low - 84.8
        beginx = x_low
        endx_w = 400
        #endx_w = 1.2*320

        line_w = ROOT.TLine(beginx, y_w, endx_w, endx_w * slope - 84.8)
        line_w.SetLineStyle(2)
        line_w.SetLineWidth(2)
        line_w.SetLineColor(ROOT.kGray+3)
        out_lines.append(line_w)

        # mTop line
        beginx = 172.5
        y_t = 0.0
        endx_t = 450

        line_t = ROOT.TLine(beginx, y_t, endx_t, endx_t * slope - 172.5)
        line_t.SetLineStyle(2)
        line_t.SetLineWidth(2)
        line_t.SetLineColor(ROOT.kGray+3)
        out_lines.append(line_t)

        # mchi line
        beginx = x_low
        y_chi = 100
        endx_chi = 317
        line_chi = ROOT.TLine(beginx, y_chi, endx_chi, endx_chi * slope) 
        line_chi.SetLineStyle(2)
        line_chi.SetLineWidth(2)
        line_chi.SetLineColor(ROOT.kGray+3)
        out_lines.append(line_chi)

    else :
        print "get_forbiddenlines    ERROR unhandled grid. Will not draw kinematic boundary lines."
    return out_lines


def make_limit_plot(conf) :
    print "make_limit_plot..."

    c = conf.limit_canvas
    c.cd()

    ################################
    # draw the frame/axes
    ################################
    frame = make_frame(conf)
    frame.Draw("axis")
    frame.GetXaxis().SetTitle(conf.x_title)
    frame.GetYaxis().SetTitle(conf.y_title)
    c.Update()

    ################################# 
    # make a legend
    ################################# 
    leg = make_default_legend(0.55,0.72,0.89,0.91)

    ######################################
    # draw previous results
    ######################################
    if conf.show_previous_8TeV_result :
        rfile = ROOT.TFile(conf.previous_result_file)
        prev_wwlike = rfile.Get(conf.previous_contours["wwlike"])
        prev_stop1l = rfile.Get(conf.previous_contours["stop1l"])
        prev_stop2l = rfile.Get(conf.previous_contours["stop2l"])

        #prev_wwlike.SetLineColor(ROOT.TColor.GetColor("#FF4444"))
        #prev_stop1l.SetLineColor(ROOT.TColor.GetColor("#F685E4"))
        #prev_stop2l.SetLineColor(ROOT.TColor.GetColor("#B93B8F"))

        prev_wwlike.SetLineColor((ROOT.kAzure+6)+1)
        prev_stop1l.SetLineColor((ROOT.kSpring-5)-1)
        prev_stop2l.SetLineColor((ROOT.kOrange-3)-2)

        prev_wwlike.SetFillColorAlpha(ROOT.kAzure+6, 0.65)
        prev_stop1l.SetFillColorAlpha(ROOT.kSpring-5, 1.00)
        prev_stop2l.SetFillColorAlpha(ROOT.kOrange-3,0.65)

        prev_wwlike.SetLineWidth(3)
        prev_stop1l.SetLineWidth(3)
        prev_stop2l.SetLineWidth(3)

        #prev_wwlike.SetFillStyle( 1001 )
        #prev_wwlike.SetFillStyle( 3005 )
        #prev_wwlike.SetFillColorAlpha(ROOT.TColor.GetColor("#FF4444"), 0.1)

        prev_stop1l.Draw("same F")
        prev_stop2l.Draw("same F")
        prev_wwlike.Draw("same F")

        prev_stop1l.Draw("same")
        prev_stop2l.Draw("same")
        prev_wwlike.Draw("same")



    ################################
    # grab the 95% CL contours
    ################################

    # obs
    g_obs       = make_contour(conf, reg_=region, type="obs", pwc=False)
    #print "make_limit_plot   NOT GRABBING UP/DOWN OBSERVED CONTOURS"
    #g_obsUp = None
    #g_obsDn = None
    g_obsUp     = make_contour(conf, reg_=region, type="obsUp", pwc=False)
    g_obsDn     = make_contour(conf, reg_=region, type="obsDn", pwc=False)

    # exp
    g_exp       = make_contour(conf, reg_=region, type="exp", pwc=False)
    g_expUp     = make_contour(conf, reg_=region, type="expUp", pwc=False)
    g_expDn     = make_contour(conf, reg_=region, type="expDn", pwc=False)

   # g_obs.SetName("stop2l_3body_observed")
   # g_obs.SaveAs("observed_contour.root")

   # g_exp.SetName("stop2l_3body_expected")
   # g_exp.SaveAs("expected_contour.root")

   # g_expUp.SetName("stop2l_3body_expected_u1s")
   # g_expUp.SaveAs("expected_contour_u1s.root")

   # g_expDn.SetName("stop2l_3body_expected_d1s")
   # g_expDn.SaveAs("expected_contour_d1s.root")

    #################################
    # draw the band around the
    # expected contours
    #################################
    make_exclusion_band(conf, g_exp, g_expUp, g_expDn)
    c.Update()

    ################################
    # draw the observed contours
    ################################
    g_obs.SetLineColor(ROOT.TColor.GetColor( c_Observed ))
    g_obs.SetLineStyle(1)
    g_obs.SetLineWidth(3)
    g_obs.Draw("C same")
    c.Update()

    for g in [g_obsUp, g_obsDn] :
        if not g : continue
        g.SetLineColor(ROOT.TColor.GetColor( c_Observed ))
        g.SetLineStyle(3)
        g.SetLineWidth(2)
        g.Draw("C same")
    c.Update()


    #####################################
    # draw official and process labels
    #####################################
    draw_top_left_label(get_atlas_label(),  (0.0 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-1.6*ROOT.gPad.GetTopMargin()), font=72)
    draw_top_left_label("Preliminary", (0.125 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-1.6*ROOT.gPad.GetTopMargin()))
    draw_top_left_label(get_lumi_label(),   (0.0 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-2.7*ROOT.gPad.GetTopMargin()))
    draw_top_left_label(conf.decay_process, (0.0 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-3.65*ROOT.gPad.GetTopMargin()))
    if grid=="bWN" and region=="SRwt" :
        region_label = "SR_{W}^{3-body} + SR_{t}^{3-body}" 
        draw_top_left_label(region_label, (0.0 + 1.3*ROOT.gPad.GetLeftMargin()), (1.0-4.7*ROOT.gPad.GetTopMargin()))  
    c.Update()

    ######################################
    # draw the legend
    ######################################
    #leg = make_default_legend(0.55,0.72,0.89,0.91)
    #leg = make_default_legend(0.55,0.77,0.88,0.92)
    leg.AddEntry(g_obs, "Observed limit (#pm1 #sigma_{theory})","l")

    #lines for the +/1 1 sigma theory
    y_obs_up = 0.895 * 1.0075
    y_obs_dn = 0.8699 * 1.013
    draw_line(0.5625, y_obs_up, 0.62115, y_obs_up, ROOT.TColor.GetColor(c_Observed), line_style=3, line_width=2)
    draw_line(0.5625, y_obs_dn, 0.62115, y_obs_dn, ROOT.TColor.GetColor(c_Observed), line_style=3, line_width=2)

    legend_band_entry(leg, "Expected limit (#pm1 #sigma_{exp})", ROOT.TColor.GetColor(c_BandYellow), 1001, ROOT.TColor.GetColor(c_Expected), 7, 2)



    leg.AddEntry(prev_wwlike, "ATLAS 8 TeV (WW-like)","f")
    leg.AddEntry(prev_stop2l, "ATLAS 8 TeV (Stop-2L)","f")
    leg.AddEntry(prev_stop1l, "ATLAS 8 TeV (Stop-1L)","f")



    # now that we have all the contours, draw the legend
    leg.Draw()
    c.Update()



    #####################################
    # draw the forbidden lines
    #####################################
    kin_lines = get_forbiddenlines(conf)
    for line_ in kin_lines :
        line_.Draw()

    if "bWN" in grid :
        mwline_text = "#Delta m(#tilde{t}_{1}, #tilde{#chi}_{1}^{0}) < m_{b} + m_{W}"
        mtline_text = "#Delta m(#tilde{t}_{1}, #tilde{#chi}_{1}^{0}) < m_{t}"
        mxline_text = "#Delta m(#tilde{t}_{1}, #tilde{#chi}_{1}^{0}) < 0"

        draw_text( 0.54, 0.51, ROOT.kGray+2, mwline_text, size=0.025, angle=39)
        draw_text( 0.74, 0.51, ROOT.kGray+2, mtline_text, size=0.025, angle=41)
        draw_text( 0.35, 0.51, ROOT.kGray+2, mxline_text, size=0.025, angle=41)
        #draw_text( 0.55, 0.51, ROOT.kGray+2, mwline_text, size=0.025, angle=42)
        #draw_text( 0.75, 0.51, ROOT.kGray+2, mtline_text, size=0.025, angle=42)
        #draw_text( 0.36, 0.51, ROOT.kGray+2, mxline_text, size=0.025, angle=42)
    c.Update()
        

    ######################################
    # draw CLs on plot
    ######################################
    if(conf.show_exp_cls or conf.show_obs_cls or conf.show_exp_sig or conf.show_obs_sig) and not conf.do_xsec_plot :
        draw_sig_or_cls(conf, reg_=region)

    
    ######################################
    # draw upper limit on production xsec
    # for each point
    ######################################
    if conf.do_xsec_plot :
        draw_upperlimit_xsec(conf)


    ########################################
    # save
    ########################################
    save_name = get_limit_output_name(conf)
    print " >>> Saving limit plot to %s"%save_name
    c.SaveAs(save_name)


#######################################################
if __name__ == "__main__" :

    global grid, channel

    parser = OptionParser()
    parser.add_option("-c", "--channel", default="")
    parser.add_option("-g", "--grid", default="")
    (options, args) = parser.parse_args()

    channel     = options.channel
    grid        = options.grid

    if channel=="" or grid=="" :
        print "ERROR input options are empty (channel: %s, grid: %s)"%(channel, grid)
        sys.exit()

    conf_file = get_configuration(grid)
    #execute the grid configuration
    gridConf = GridConfiguration(grid)
    gridConf.name = gridConf
    gridConf.channel = channel
    execfile("./config/%s"%conf_file)

    # have now loaded everything
    print "=================================="
    print "  limitplotter summary            "
    print "----------------------------------"
    print " configuration file:  %s          "%conf_file
    print " grid:                %s          "%gridConf.grid
    print " channel:             %s          "%gridConf.channel
    print " base region:         %s          "%gridConf.base_region
    print " do limit plot:       %s          "%gridConf.do_limit_plot
    print " show obs CLs:        %s          "%gridConf.show_obs_cls
    print " show exp CLs:        %s          "%gridConf.show_exp_cls
    print " show obs signif.:    %s          "%gridConf.show_obs_sig
    print " show exp signif.:    %s          "%gridConf.show_exp_sig
    print " do best SR plot:     %s          "%gridConf.do_best_sr_per_point
    print " do xsec plot:        %s          "%gridConf.do_xsec_plot
    print " show previous limit: %s          "%gridConf.show_previous_8TeV_result
    print "=================================="


    # collect limit result files
    gridConf.collect_limit_result_files()

    # build the grid
    gridConf.assign_grid()

    # fill the 'raw' limit results
    gridConf.fill_raw_results()

    for s in gridConf.signals :
        print "(%.1f,%.1f)"%(float(s.mX), float(s.mY))


    # find the best SR per point (if doing PWC)
    #find_best_SR_per_point(gridConf)

    if gridConf.do_best_sr_per_point :
        make_best_sr_plot(gridConf)

    # make the limit plot
    if gridConf.do_limit_plot or gridConf.do_xsec_plot :
        make_limit_plot(gridConf)


