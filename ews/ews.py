import numpy as np
from . import movingwindow as ts
import pyximport; pyximport.install()
from . import kolmogorov_complexity
from . import entropy 


def get_ews(x,windowsize, ac_lag):
	x = np.array(x)

	#Mean:
	mu = ts.MovingWindowAverage(x, windowsize)
	#Second Moment:
	mu2 = ts.MovingWindowAverage(x**2, windowsize)
	#Third moment:
	mu3 = ts.MovingWindowAverage(x**3, windowsize)
	#Fourth moment:
	mu4 = ts.MovingWindowAverage(x**4, windowsize)
	#Variance:
	var =  mu2 - mu**2
	#Autocorrelation:
	ac = ts.MovingAC(x,windowsize,ac_lag)
	with np.errstate(divide='ignore', invalid='ignore'):
		#Coefficient of variation:
		cov = np.sqrt(var)/mu
		#Index of dispersion:
		iod = var/mu
		#Correlation time:
		ct = -ac_lag/np.log(abs(ac))
		#Shannon entropy:
		se = entropy.MovingEntropy(x, windowsize)
		#Skewness:
		skew = (mu3 -3*mu2*mu + 2*mu**3)/(var**(3/2))
		#Kurtosis
		kurtosis = (mu4 -4*mu3*mu + 6*mu2*mu**2 -3*mu**4)/(var**2)
	#Kolmogorov complexity: (note this takes significantly longer to calculate than the other EWS)
	kc = kolmogorov_complexity.CMovingKC(x,mu, windowsize)

	out = {"timeseries": x, "mean": mu, "variance": var, 'coefficient_of_variation': cov,
			"index_of_dispersion": iod, "autocorrelation": ac, "decay_time": ct,
			"Shannon_entropy": se, "Kolmogorov_complexity": kc, "skewness": skew,
			"kurtosis": kurtosis}

	return(out)



def output_csv(data,filename):
	import pandas 
	d = pandas.DataFrame(data)
	d.to_csv(filename)





# #Detrending for pej:
# from scipy import signal
# y = signal.detrend(x, type='linear', bp = [len(x)/2])
# m = np.zeros(len(y))
# KC = kc.CMovingKC(y,m, windowsize)

# KC = kc.CMovingKC_detrend(x, windowsize)

# BinTS = kc.binaryTimeseries(x,mu)

#for i in range(len(R0)): print R0[i], x[i], mu[i], mu2[i], var[i], Cov[i], IoD[i], AC[i], CT[i], KC[i], BinTS[i], SE[i], y[i]  
