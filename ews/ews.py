import numpy as np
from . import movingwindow as ts
#import pyximport; pyximport.install()
from . import kolmogorov_complexity
from . import entropy


def get_ews(x,windowsize, ac_lag, se = True, kc = True):
    '''
    Calculate early-warning signals from time series data.
    :param x: time series data (either 1-dimensional numpy array or list)
    :param windowsize: integer number of time points in moving window
    :param ac_lag: integer lag used to calculated the autocovariance, autocorrelation and decay time
    :param se: Boolean. If True calculate the moving Shannon entropy. This is significantly slower
    :param kc: Boolean. If True calculate the moving Kolmogorov complexity. This is around 10x slower
    :return: dict containing all early-warning signals and original time series
    '''

    x = np.array(x, dtype = 'float')


    # Mean:
    mu = ts.MovingWindowAverage(x, windowsize)
    # Variance:
    var = ts.MovingWindowAverage((x-mu)**2, windowsize)
    # Autocovariance
    cm = x-mu
    cm_lag = np.concatenate([np.zeros(ac_lag), cm[:-ac_lag]])
    var_lag = np.concatenate([np.zeros(ac_lag), var[:-ac_lag]])
    acov = ts.MovingWindowAverage(cm*cm_lag, windowsize)

    with np.errstate(divide='ignore', invalid='ignore'):
        # Autocorrelation:
        ac = acov / np.sqrt(var * var_lag)
        # Coefficient of variation:
        cov = np.sqrt(var)/mu
        # Index of dispersion:
        iod = var/mu
        # Correlation time:
        ct = -ac_lag/np.log(abs(ac))
        # Skewness:
        skew = ts.MovingWindowAverage(cm**3, windowsize)/(var**(3/2))
        # Kurtosis
        kurtosis = ts.MovingWindowAverage(cm**4, windowsize)/(var**2)

    out = {"timeseries": x, "mean": mu, "variance": var, 'coefficient_of_variation': cov,
           "index_of_dispersion": iod, "autocorrelation": ac, "decay_time": ct,
           "skewness": skew,
           "kurtosis": kurtosis, "autocovariance": acov}

    # Kolmogorov complexity:
    if(kc == True):
        out["Kolmogorov_complexity"] = kolmogorov_complexity.CMovingKC(x,mu, windowsize)
        
    # Shannon entropy
    if(se == True):
        with np.errstate(divide='ignore', invalid='ignore'):
            out["Shannon_entropy"] = entropy.MovingEntropy(x, windowsize)


    return(out)



def output_csv(data,filename):
    import pandas
    d = pandas.DataFrame(data)
    d.to_csv(filename)
