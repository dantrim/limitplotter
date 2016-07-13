#
# graphs, legends, and bands, oh my!
#
# daniel.joseph.antrim@cern.ch
# July 2016
#


import ROOT as r
import array

r.TH1F.__init__._creates        = False
r.TH2F.__init__._creates        = False
r.TCanvas.__init__._creates     = False
r.TGraph.__init__._creates      = False
r.TPad.__init__._creates        = False
r.TLine.__init__._creates       = False
r.TLegend.__init__._creates     = False
r.TLatex.__init__._creates      = False

''' --------------------- '''
'''  Labels and colors    '''
''' --------------------- '''

# -----------------------------
#  define colors for plots
# -----------------------------
c_BandYellow    = "#ffe938"
c_Observed      = "#aa000"
c_Expected      = "#28373c"

# -----------------------------
#  basic text writing
# -----------------------------
def draw_text(x, y, color, text, size=0.04, angle=0.0) :
    l = r.TLatex()
    l.SetTextSize(size)
    l.SetNDC()
    l.SetTextFont(62)
    l.SetTextColor(color)
    l.SetTextAngle(angle)
    l.DrawLatex(x,y,text)

# -----------------------------
#  top left label
# -----------------------------
def draw_top_left_label(label, xpos=None, ypos=None, align=13) :
    tex = r.TLatex(0.0,0.0,'')
    tex.SetTextFont(62)
    tex.SetTextSize(0.75 * tex.GetTextSize())
    tex.SetNDC()
    tex.SetTextAlign(align)
    tex.DrawLatex((0.0 + 1.2*r.gPad.GetLeftMargin()) if not xpos else xpos,
                  (1.0-1.5*r.gPad.GetTopMargin()) if not ypos else ypos,
                  label)


# -----------------------------
#  ATLAS label
# -----------------------------
def get_atlas_label() :
    label = "#it{ATLAS Internal}"
    return label

# -----------------------------
#  Lumi Label
# -----------------------------
def get_lumi_label() :
    label = "#scale[0.8]{#int Ldt = 5.82 fb^{-1}, #sqrt{s} = 13 TeV}"
    return label

''' ---------------------- '''
'''      TH2 Methods       '''
''' ---------------------- '''
def make_frame(conf) :
    '''
    Make the frame that will provide the axes on which to make
    the plots
    '''
    frame = r.TH2F("frame", "", 50, conf.xlow, conf.xhigh, 50, conf.ylow, conf.yhigh)
    
    frame.SetLabelOffset( 0.012, "X")
    frame.SetLabelOffset( 0.012, "Y")
    
    frame.GetXaxis().SetTitleOffset( 1.33 )
    frame.GetYaxis().SetTitleOffset( 1.47 )
   # frame.GetXaxis().SetTitleOffset( 1.10 )
   # frame.GetYaxis().SetTitleOffset( 1.15 )
    
    frame.GetXaxis().SetLabelSize( 0.035 )
    frame.GetYaxis().SetLabelSize( 0.035 )
    frame.GetXaxis().SetTitleSize( 0.04 )
    frame.GetYaxis().SetTitleSize( 0.04 )
    
    frame.GetXaxis().SetTitleFont( 42 )
    frame.GetYaxis().SetTitleFont( 42 )
    frame.GetXaxis().SetLabelFont( 42 )
    frame.GetYaxis().SetLabelFont( 42 )
    
    r.gPad.SetTicks()
    r.gPad.SetLeftMargin( 0.13 )
    r.gPad.SetRightMargin( 0.08 )
    r.gPad.SetBottomMargin( 0.120 )
    r.gPad.SetTopMargin( 0.060 )
    
    return frame

''' ---------------------- '''
'''     TLine Methods      '''
''' ---------------------- '''

# -------------------------
#  vanilla line
# -------------------------
def draw_line(xl, yl, xh, yh, line_color, line_style, line_width) :
    l = r.TLine(xl, yl, xh, yh)
    l.SetNDC()
    l.SetLineColor(line_color)
    l.SetLineStyle(line_style)
    l.SetLineWidth(line_width)
    l.Draw("same")

# --------------------------
#  kinematic boundary line
# --------------------------
def draw_forbidden_line(conf) :
    '''
    Draw the line marking the kinematically forbidden
    phase space
    '''
    slope = 0.0
    beginx, beginy = 0.0, 0.0
    endx, endy = 0.0, 0.0
    y = 0.0
    if conf.forbidden_line_style == "one2one" :
        slope = 1.0
        y = slope * conf.xlow
        beginx = conf.xlow
        endy = 0.75 * conf.xhigh
    else :
        print "WARNING    draw_forbidden_line error: forbidden_line_style not supported. Line will not be drawn."
    line = r.TLine(beginx, y, endy, endy * slope)
    line.SetLineStyle(9)
    line.SetLineWidth(2)
    line.SetLineColor(r.kGray+2)
    return line

        
''' ---------------------- '''
'''    TLegend Methods     '''
''' ---------------------- '''
def make_default_legend(xl,yl,xh,yh) :
    leg = r.TLegend(xl,yl,xh,yh)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(62)
    return leg

def legend_band_entry(legend, name, fill_color, fill_style, line_color, line_style, line_width) :
    gr = r.TGraph()
    gr.SetFillColor(fill_color)
    gr.SetFillStyle(fill_style)
    gr.SetLineColor(line_color)
    gr.SetLineStyle(line_style)
    gr.SetLineWidth(line_width)
    legend.AddEntry(gr, name, "LF")

 
''' ---------------------- '''
'''     TGraph Methods     '''
''' ---------------------- '''
def make_contour(conf, reg_="", type="exp", pwc=False) :
    '''
    Make a 95% CL contour (TGraph) from the input signals
    '''
    signals = conf.signals

    g = r.TGraph2D(1)
    g.Clear()
    g.SetTitle("g_"+type)
    for s in signals :
        signif, x, y = 0.0, float(s.mX), float(s.mY)
        if pwc :
            if   type == "obs"   : signif = s.bestObservedSig
            elif type == "obsUp" : signif = s.bestObservedSigUp1s
            elif type == "obsDn" : signif = s.bestObservedSigDn1s
            elif type == "exp"   : signif = s.bestExpectedSig
            elif type == "expUp" : signif = s.bestExpectedSigUp1s
            elif type == "expDn" : signif = s.bestExpectedSigDn1s
        else :
            if reg_ == "" :
                print "make_contour    ERROR you must provide a region"
                sys.exit()
            if   type == "obs"   : signif = s.observedSig[reg_]
            elif type == "obsUp" : signif = s.observedSigUp1s[reg_]
            elif type == "obsDn" : signif = s.observedSigDn1s[reg_]
            elif type == "exp"   : signif = s.expectedSig[reg_]
            elif type == "expUp" : signif = s.expectedSigUp1s[reg_]
            elif type == "expDn" : signif = s.expectedSigDn1s[reg_]

        print signif
        print "(%.1f,%.1f) : %.1f"%(x, y, float(signif))
        g.SetPoint(g.GetN(), x, y, float(signif))

    hist = None
    hist = r.TH2F("tmp_"+type, "tmp_"+type, 50, conf.xlow, conf.xhigh, 50, conf.ylow, conf.yhigh)
    g.SetHistogram(hist)
    pvalue = 0.05
    level = r.TMath.NormQuantile(1.0-pvalue)
    if g.GetZmax() < level : return
    h = g.GetHistogram().Clone("tmp_"+g.GetName())
    h.SetDirectory(0)
    gbc, nx, ny = h.GetBinContent, h.GetNbinsX(), h.GetNbinsY()
    nPointsExcluded = len([1 for i in range(g.GetN()) if g.GetZ()[i] > level])
    h.SetContour(1)
    h.SetContourLevel(0, level)
    c = r.TCanvas('tmp_can_'+type, '')
    c.cd()
    #h.Smooth()
    h.Draw('CONT LIST')
    c.Update()
    contours = r.gROOT.GetListOfSpecials().FindObject('contours')
    if contours.GetEntries() :
        g = contours.At(0).First()
        contours.Delete()
        h.Delete()
        return g


def make_exclusion_band(conf, nom, up, down) :
    '''
    Draw the exclusion band
    Inputs:
        - nom:   TGraph contour for the nominal expected significance
        - up :   TGraph contour for the +1sigma uncertainty expected significance
        - down:  TGraph contour for the -1sigma uncertainty expected significance
    '''
    nbins   = int(max(nom.GetN(), up.GetN(), down.GetN()))
    n_nom   = int(nom.GetN())
    n_up    = int(up.GetN())
    n_down  = int(down.GetN())
    
    # containers for the x-y values for the 
    # three contours that will be fed into
    # the final contours as an array of ROOT doubles
    x_nom, y_nom    = [], []
    x_up, y_up      = [], []
    x_down, y_down  = [], []

    # fill nominal points
    for i in range(0, n_nom) :
        X, Y = r.Double(0), r.Double(0)
        nom.GetPoint(i, X, Y)
        x_nom.append(X)
        y_nom.append(Y)
    # check that nominal array has the required number of points
    if n_nom < nbins :
        for i in range(n_nom, nbins) :
            x_nom.append(x_nom[n_nom-1])
            y_nom.append(y_nom[n_nom-1])
    
    # fill the up-variation points
    for i in range(0, n_up) :
        X, Y = r.Double(0), r.Double(0)
        up.GetPoint(i, X, Y)
        x_up.append(X)
        y_up.append(Y)
        
    # check that the up array has the required number of points
    if n_up < nbins :
        for i in range(n_up, nbins) :
            x_up.append(x_up[n_up-1])
            y_up.append(y_up[n_up-1])
    
    # fill the down-variation points
    for i in range(0, n_down) :
        X, Y = r.Double(0), r.Double(0)
        down.GetPoint(i, X, Y)
        x_down.append(X)
        y_down.append(Y)

    # check that the down array has the required number of points
    if n_down < nbins :
        for i in range(n_down, nbins) :
            x_down.append(x_down[n_down-1])
            y_down.append(y_down[n_down-1])
    
    # concatenate the up and down arrays to make a complete
    # array for a single TGraph for the outer bounds of the band
    x, y = [], []
    x += x_up
    x += x_down
    y += y_up
    y += y_down

    # make the values into an array of doubles so that the
    # TGraph receives the Double_t* 
    x_nom_arr  = array.array('d', x_nom)
    y_nom_arr  = array.array('d', y_nom)
    x_up_arr   = array.array('d', x_up)
    y_up_arr   = array.array('d', y_up)
    x_down_arr = array.array('d', x_down)
    y_down_arr = array.array('d', y_down)
    x_arr      = array.array('d', x)
    y_arr      = array.array('d', y)
    
    gr = r.TGraph(nbins, x_nom_arr, y_nom_arr)
    gr_down = r.TGraph(nbins, x_down_arr, y_down_arr)
    gr_up = r.TGraph(nbins, x_up_arr, y_down_arr)
    gr_shade = r.TGraph(nbins, x_down_arr, y_down_arr)
    
    for i in range(0, nbins) :
        # set the points for the "upper semi-circle" of the band
        gr_shade.SetPoint(i, x_up_arr[i], y_up_arr[i])
        # set the points for the "lower semi-circle" of the band
        gr_shade.SetPoint(nbins+i, x_down_arr[nbins-i-1], y_down_arr[nbins-i-1])
    
    c = conf.limit_canvas
    c.cd() 
    # now draw
    gr.Draw("l")
    gr.SetLineColor( r.TColor.GetColor(c_Expected) )
    gr.SetLineStyle(7)
    gr.SetLineWidth(2)

    gr_shade.SetFillStyle( 1001 )
    gr_shade.SetFillColor( r.TColor.GetColor( c_BandYellow ) )
    gr_shade.Draw("F same")
    
    gr.Draw("l same")
    c.Update()
    

