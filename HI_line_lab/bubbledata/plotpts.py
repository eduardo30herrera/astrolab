import numpy as np 
import matplotlib.pyplot as plt
import readspec_mod as rsm
import os
#================================================#
#We must read in all data from a point and plot  #
#it on one graph and then go to another point and#
#repeat for as many files as we have taken       #
#================================================#

def boxavg(data, radius=10): #in this part we will need to put in one of the data and a radius to take an average
    new = np.zeros(data.shape)
    for i in np.arange(radius, len(data)-radius+1):
        new[i] = np.median(data[i-radius:i+radius])
    return new #in this state, I don't think I've defined "new" as an array to be plotted especially on the plots below

#b = [-70., -68., -66., -64., -62., -60., -58., -56., -54., -52., -50.,
#       -48., -46., -44., -42., -40., -38., -36., -34., -32., -30., -28.,
#       -26., -24., -22., -20., -18., -16., -14., -12., -10.]
b = [-32.]
for i in b:
    File = np.load('Points/'+str(i)+'.npz')
    longpts = File['x'] #the longitude points we will need to plot
    for n in longpts:
        onept = n
        if not os.path.isfile('bubbleOFF'+str(n)+','+str(i)+'0.log'): #if for some reason, the file does not exist, as in we have not 
            continue
        if not os.path.isfile('bubbleON'+str(n)+','+str(i)+'0.log'):  #taken any data for that position in the sky,
            continue
        if not os.path.isfile('bubbleNOISE_OFF'+str(n)+','+str(i)+'0.log'): #then this part of the code will skip over it without
            continue
        if not os.path.isfile('bubbleNOISE_ON'+str(n)+','+str(i)+'0.log'):  #having to break the for-loop
            continue
        
        spec_off = rsm.readSpec('bubbleOFF'+str(n)+','+str(i)+'0.log') #shifted the below by 4 MHz
        spec_off = boxavg(np.mean(spec_off,1))#[250:-250] 

        spec_on = rsm.readSpec('bubbleON'+str(n)+','+str(i)+'0.log') #on frequency 
        spec_on = boxavg(np.mean(spec_on,1))#[250:-250]

        noise_off = rsm.readSpec('bubbleNOISE_OFF'+str(n)+','+str(i)+'0.log') #spec_off with noise diode
        noise_off = boxavg(np.mean(noise_off,1))#[250:-250]

        noise_on = rsm.readSpec('bubbleNOISE_ON'+str(n)+','+str(i)+'0.log') #spec_on freq with noise diode on
        noise_on = boxavg(np.mean(noise_on,1))#[250:-250]

        fc = 1272.4+150
        f_range = np.linspace(fc-6, fc+6, spec_off.shape[0])        

        plt.plot(f_range, spec_off, label = "Spec off") 
        plt.plot(f_range, spec_on, label = "Spec on")   
        plt.plot(f_range, noise_off, label= "Noise off") 
        plt.plot(f_range, noise_on, label= "Noise on")
        plt.title('Cleaned Spectra')
        plt.xlabel('MHz')
        plt.ylabel('counts')
        plt.legend()
        plt.show()
        
        #P_on = np.sum(noise_on - spec_on)/100. #we divide by 100 kelvin here
        #t_sys_on = np.sum(spec_on)/P_on
        #P_off = np.sum(noise_off - spec_off)/100. #we divide by 100 kelvin here
        #t_sys_off = np.sum(spec_off)/P_off
        T_noise = 100
        Y_on = np.sum(noise_on)/np.sum(spec_on) #we divide by 100 kelvin here
        t_sys_on = T_noise/(Y_on-1)
        Y_off = np.sum(noise_off)/np.sum(spec_off) #we divide by 100 kelvin here
        t_sys_off = T_noise/(Y_off-1)
        
        G_ratio = (np.sum(spec_on)/np.sum(spec_off))
        
        spec_off = spec_off * G_ratio
        noise_off = noise_off * G_ratio
        
        cal_on = ((spec_on[(2731-1365):(2731+1366)]/spec_off[(2731-1365):(2731+1366)])-1) * t_sys_on
        cal_off = ((spec_off[(5461-1365):(5461+1366)]/spec_on[(5461-1365):(5461+1366)])-1) * t_sys_on

        new_f_range = np.linspace(1420.4-2,1420.4+2,1365*2+1)

        coeff_on = np.polyfit(np.delete(new_f_range, np.s_[1280:-1280]), np.delete(cal_on,np.s_[1280:-1280]), 5)
        coeff_off = np.polyfit(np.delete(new_f_range, np.s_[1280:-1280]), np.delete(cal_off,np.s_[1280:-1280]), 5)
        fit_on = (coeff_on[0] * new_f_range**5) + (coeff_on[1]*new_f_range**4) + (coeff_on[2]*new_f_range**3) + (coeff_on[3]*new_f_range**2) + (coeff_on[4]*new_f_range) + (coeff_on[5])
        fit_off = (coeff_off[0] * new_f_range**5) + (coeff_off[1]*new_f_range**4) + (coeff_off[2]*new_f_range**3) + (coeff_off[3]*new_f_range**2) + (coeff_off[4]*new_f_range) + (coeff_off[5])
        
        cal_on = cal_on - fit_on
        cal_off = cal_off - fit_off
        cal = (cal_on + cal_off)/2.
        
        plt.plot(new_f_range, cal)
        plt.ylabel('Temperature (K)', fontsize=20)
        plt.xlabel('Frequency (MHz)', fontsize=20)
        plt.title('Calibrated Spectrum', fontsize=24)
        #plt.plot(new_f_range, cal_on)
        #plt.plot(new_f_range, cal_off)
        plt.show()
        #=================================#
        #now we will save the final       #
        #calibrated spectrum so that they #
        #can be used for our image        #
        #=================================#
        
