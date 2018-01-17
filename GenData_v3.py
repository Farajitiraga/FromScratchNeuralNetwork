######################################
# Sam Meehan : Stern-Gerlach Experiment Simulator
#
#
######################################

import random
import numpy as np
from ROOT import *

def main():

    #genTypes=["sig","bkg"]
    #genTypes=["sig"]
    
    genTypes=["mixed"]
    
    NEvents=10000

    for type in genTypes:

        # lists to store the generated x and y pairs
        xgen=[]
        ygen=[]
        zgen=[]

        # continue generating until we have NEvents values
        while len(xgen)<NEvents:
        
            if len(xgen)%100==0:
                print "Generated : ",len(xgen)
        
            xTest=0
            yTest=0
            zTest=0
        
            # using the accept reject method in 2D
            while True:
            
                # generate the uniformly distributed (x,y) pairs
                xTest = random.uniform(-4,4)
                yTest = random.uniform(-4,4)
                zTest = random.uniform(-4,4)
            
                # generate "u" as the auxiliary variable
                uTest = random.uniform(0,1)
            
                # evaluate the function value of the 2D gaussian
                if type=="bkg":
                    fEval = PDF_Background(xTest,yTest,zTest)
                elif type=="sig":
                    fEval = PDF_Signal(xTest,yTest,zTest)
                elif type=="mixed":
                    typeRand = random.random()
                    if typeRand>0.73:
                        fEval = PDF_Background(xTest,yTest,zTest)
                    else:
                        fEval = PDF_Signal(xTest,yTest,zTest)
                else:
                    print "Not a valid data type ---"
            
                # if the auxiliary value "z" is below the gaussian, then accept the (x,y) pair
                if uTest<fEval:
                    break
        
            # if it broke out of the loop above, then its a good pair and we add it to the list
            xgen.append(xTest)
            ygen.append(yTest)
            zgen.append(zTest)
        
    
        # make a histogram for plotting
        hxy = TH2F("hxy","hxy",200,-5,5,200,-5,5)
        hxz = TH2F("hxz","hxz",200,-5,5,200,-5,5)
        hyz = TH2F("hyz","hyz",200,-5,5,200,-5,5)
    
        # store for assignment
        fout = open("data_"+type+".txt","w")
    
        # fill the (x,y) pairs into the 2D histogram
        for i in range(len(xgen)):
            hxy.Fill(xgen[i],ygen[i])
            hxz.Fill(xgen[i],zgen[i])
            hyz.Fill(ygen[i],zgen[i])
            fout.write("{0:10} {1:10} {2:10}\n".format(round(xgen[i],4), round(ygen[i],4), round(zgen[i],4)))
        
        # close the output file
        fout.close()
        
        # save it on a canvas
        c = TCanvas("c","c",200,200)
        hxy.Draw("colz")
        c.SaveAs("correlation_gen_check_xy_"+type+".eps")
        hxz.Draw("colz")
        c.SaveAs("correlation_gen_check_xz_"+type+".eps")
        hyz.Draw("colz")
        c.SaveAs("correlation_gen_check_yz_"+type+".eps")
        
        

def EvalGauss2D(xt,yt):

    # hardcode the values of the parameter
    R     = 2.0
    sigma = 0.3
    
    # distance from half circle
    # break into the four quadrants
    distance = 0
    if yt>0:
        distance     = (xt**2 + yt**2)**0.5 - R
    else:
        distance_pos = (xt-R)**2+(yt)**2
        distance_neg = (xt+R)**2+(yt)**2

        distance = min([distance_pos, distance_neg])

    # calculate the argument of the exponential
    arg   = -1.0*(1.0/(2*sigma**2))*((distance)**2)
    
    # calculate the gaussian itself
    gauss = np.exp(arg)
    
    # return that value
    return gauss
    
    
def PDF_Background(xt,yt,zt):

    # hardcode the values of the parameter
    R     = 2.0
    sigma = 0.2
    
    # distance from half sphere
    distance = 0
    if zt>0:
        distance     = (xt**2 + yt**2 + zt**2)**0.5 - R
    else:
    
        alpha = float(yt)/float(xt)
        
        xC = np.sign(xt)*((R**2)*(1.0/(1+alpha**2)))**0.5
        
        yC = alpha*xC
    
        distance = ((xt-xC)**2 + (yt-yC)**2 + (zt)**2)**0.5

    # calculate the argument of the exponential
    arg   = -1.0*(1.0/(2*sigma**2))*((distance)**2)
    
    # calculate the gaussian itself
    gauss = np.exp(arg)
    
    # return that value
    return gauss
    
    
def PDF_Signal(xt,yt,zt):

    # hardcode the values of the parameter
    sigma = 0.5
    
    # distance from origin
    distance     = (xt**2 + yt**2 + zt**2)**0.5

    # calculate the argument of the exponential
    arg   = -1.0*(1.0/(2*sigma**2))*((distance)**2)
    
    # calculate the gaussian itself
    gauss = np.exp(arg)
    
    # return that value
    return gauss
    
if __name__ == "__main__":
    main()