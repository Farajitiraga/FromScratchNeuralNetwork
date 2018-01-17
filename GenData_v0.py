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
    genTypes=["sig","bkg","mixed"]
    
    # number of events
    NEvents=10000

    # get the maximum values of the PDFs
    fmax = 0.0
    xmin = -8.0
    xmax = 8.0
    
    sigbkg = "XXX"

    for x in np.arange(xmin,xmax,0.01):
        bkg = fEval = PDF_Background(x)        
        if bkg>fmax:
            fmax=bkg
            sigbkg="Background"
        sig = fEval = PDF_Signal(x)        
        if sig>fmax:
            fmax=sig
            sigbkg="Signal"
            
    print "Maximum of PDF's : ",fmax," - ",sigbkg


    # generate all types
    for type in genTypes:

        # lists to store the generated x and y pairs
        xgen=[]

        # continue generating until we have NEvents values
        while len(xgen)<NEvents:
        
            if len(xgen)%100==0:
                print "Generated : ",len(xgen)
        
            xTest=0
        
            # using the accept reject method in 1D
            while True:
            
                # generate the uniformly distributed (x) values
                xTest = random.uniform(xmin,xmax)
            
                # generate "u" as the auxiliary variable
                uTest = random.uniform(0,fmax)
            
                # evaluate the function value of the 2D gaussian
                if type=="bkg":
                    fEval = PDF_Background(xTest)
                elif type=="sig":
                    fEval = PDF_Signal(xTest)
                elif type=="mixed":
                    typeRand = random.random()
                    if typeRand>0.73:
                        fEval = PDF_Background(xTest)
                    else:
                        fEval = PDF_Signal(xTest)
                else:
                    print "Not a valid data type ---"
            
                # if the auxiliary value "z" is below the gaussian, then accept the (x,y) pair
                if uTest<fEval:
                    break
        
            # if it broke out of the loop above, then its a good pair and we add it to the list
            xgen.append(xTest)
        
    
        # make a histogram for plotting
        hx = TH1F("hx","hx",200,xmin,xmax)
    
        # store for assignment
        fout = open("data_v0_"+type+".txt","w")
    
        # fill the (x,y) pairs into the 2D histogram
        for i in range(len(xgen)):
            hx.Fill(xgen[i])
            fout.write("{0:10}\n".format(round(xgen[i],4)))
        
        # close the output file
        fout.close()
        
        # save it on a canvas
        c = TCanvas("c","c",200,200)
        hx.Draw("colz")
        c.SaveAs("data_check_v0_x_"+type+".eps")
        
        


    
    
def PDF_Background(xt):

    # hardcode the values of the parameter
    R     = 0.0
    sigma = 1.0
   
    # distance
    distance = R-xt

    # calculate the argument of the exponential
    arg   = -1.0*(1.0/(2*sigma**2))*((distance)**2)
    
    # calculate the gaussian itself
    gauss = np.exp(arg)
    
    # return that value
    return gauss
    
    
def PDF_Signal(xt):

    # hardcode the values of the parameter
    R     = 3.0
    sigma = 1.5

    # distance
    distance = R-xt

    # calculate the argument of the exponential
    arg   = -1.0*(1.0/(2*sigma**2))*((distance)**2)
    
    # calculate the gaussian itself
    gauss = np.exp(arg)
    
    # return that value
    return gauss
    
if __name__ == "__main__":
    main()