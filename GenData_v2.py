######################################
# Sam Meehan : Stern-Gerlach Experiment Simulator
#
#
######################################

import random
import numpy as np
from ROOT import *

def main():

    # types to generate
    #genTypes=["sig","bkg","mixed"]
    genTypes=["sig","bkg"]
    
    # number of events
    NEvents=10000
    
    # get the maximum values of the PDFs
    fmax = 0.0
    xmin = -8.0
    xmax = 8.0
    ymin = -8.0
    ymax = 8.0
    
    sigbkg = "XXX"

    for x in np.arange(xmin,xmax,0.1):
        print "Finding Max : x=",x
        for y in np.arange(ymin,ymax,0.1):
            bkg = fEval = PDF_Background(x,y)        
            if bkg>fmax:
                fmax=bkg
                sigbkg="Background"
            sig = fEval = PDF_Signal(x,y)        
            if sig>fmax:
                fmax=sig
                sigbkg="Signal"
            
    print "Maximum of PDF's : ",fmax," - ",sigbkg

    for type in genTypes:

        # lists to store the generated x and y pairs
        xgen=[]
        ygen=[]

        # continue generating until we have NEvents values
        while len(xgen)<NEvents:
        
            if len(xgen)%100==0:
                print "Generated : ",len(xgen)
        
            xTest=0
            yTest=0
        
            # using the accept reject method in 2D
            while True:
            
                # generate the uniformly distributed (x,y) pairs
                xTest = random.uniform(xmin,xmax)
                yTest = random.uniform(ymin,ymax)
            
                # generate "u" as the auxiliary variable
                uTest = random.uniform(0,fmax)
            
                # evaluate the function value of the 2D gaussian
                if type=="bkg":
                    fEval = PDF_Background(xTest,yTest)
                elif type=="sig":
                    fEval = PDF_Signal(xTest,yTest)
                elif type=="mixed":
                    typeRand = random.random()
                    if typeRand>0.73:
                        fEval = PDF_Background(xTest,yTest)
                    else:
                        fEval = PDF_Signal(xTest,yTest)
                else:
                    print "Not a valid data type ---"
            
                # if the auxiliary value "z" is below the gaussian, then accept the (x,y) pair
                if uTest<fEval:
                    break
        
            # if it broke out of the loop above, then its a good pair and we add it to the list
            xgen.append(xTest)
            ygen.append(yTest)
        
    
        # make a histogram for plotting
        hxy = TH2F("hxy","hxy",200,xmin,xmax,200,ymin,ymax)
    
        # store for assignment
        fout = open("data_v2_"+type+".txt","w")
    
        # fill the (x,y) pairs into the 2D histogram
        for i in range(len(xgen)):
            hxy.Fill(xgen[i],ygen[i])
            fout.write("{0:10} {1:10}\n".format(round(xgen[i],4), round(ygen[i],4)))
        
        # close the output file
        fout.close()
        
        # save it on a canvas
        c = TCanvas("c","c",200,200)
        hxy.Draw("colz")
        c.SaveAs("data_check_v1_xy_"+type+".eps")
        

    
def PDF_Background(xt,yt):

    # pdf that is unity below a line and then falls off as a Gaussian with the y distance from line

    # hardcode the values of the parameter
    a0 = 1
    a1 = 1
    a2 = 1
    a3 = 1
    sigma = 0.5
    
    # value of the function returned
    valFunc = 0.0
    
    # border value
    y_border = a0*(xt**3) + a1*(xt**2) + a2*(xt**1) + a3*(xt**0)
    
    # distance from half sphere
    distance = 0
    if yt>y_border:
        valFunc = 1.0
    else:    
        distance = np.abs(yt - y_border)

    # calculate the argument of the exponential
    arg   = -1.0*(1.0/(2*sigma**2))*((distance)**2)
    
    # calculate the gaussian itself
    valFunc = np.exp(arg)
    
    # return that value
    return valFunc
    
    
def PDF_Signal(xt,yt):

    # hardcode the values of the parameter
    a0 = 1
    a1 = 1
    a2 = 1
    a3 = 1
    sigma = 0.5
    
    # value of the function returned
    valFunc = 0.0
    
    # border value
    y_border = a0*(xt**3) + a1*(xt**2) + a2*(xt**1) + a3*(xt**0)
    
    # distance from half sphere
    distance = 0
    if yt<y_border:
        valFunc = 1.0
    else:    
        distance = np.abs(yt - y_border)
        
    # calculate the argument of the exponential
    arg   = -1.0*(1.0/(2*sigma**2))*((distance)**2)
    
    # calculate the gaussian itself
    valFunc = np.exp(arg)
    
    # return that value
    return valFunc
    
if __name__ == "__main__":
    main()