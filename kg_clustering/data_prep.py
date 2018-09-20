'''
The functions inside of data_prep computes the varaibles needed to classify points according to KG model.

-----------------------
Requirements/Variables
-----------------------
ds = an xarray data set of monthy precipitation, temperature max and temperature min data. 
prec = Precipitation
Tmax = temperature max
Tmin = temperature min

---------
Functions
---------
monthly_means: Computes averages of data along the months.  Used in build_rolling_mean to prepare data for KG
build_rolling_mean: Computes the monthly means for a given interval delta_t across whole data. 
pth_build:  Given the mean temperature, winter and summer precipitation, compute P_th
warm_summer_mask:  This function finds the mask for the warm summer climates in the sub-sub-classes of C and D
is_sum: Used to select summer half of year
is_win: Used to select winter half of year

'''


import numpy as np
import xarray as xr
import pandas as pd
import dask.array as da


def monthly_mean(ds):
    '''
    Finds the average value for a given month for a data set.  For example, given 20 years of data, month 1 corresponds to the mean
    of each of the 20 January values.
    
    Note that the dates on these correspond to the first year rather than the whole time interval.  This is to ensure that datetime
    functions later work.
    '''
    #First, we find date index to be added back into our data array
    year_min = pd.DatetimeIndex(ds.time.values).year.min()
    date = pd.to_datetime("{}-01-16".format(year_min))
    time_index = date + pd.to_timedelta(np.arange(12), 'M')
    
    #Next, we take the mean along each month:
    ds = ds.groupby('time.month').mean('time')
    ds = ds.assign_coords(month = time_index)

    

    return ds
	
	
def build_rolling_mean(ds, delta_t):
    '''
    This function takes a data set ds and a time chunk delta_t and uses these to build a new data set of rolling averages along
    the months
    '''
    
    #First, compute how many years we will have
    year_min = pd.DatetimeIndex(ds.time.values).year.min()
    year_max = pd.DatetimeIndex(ds.time.values).year.max()
    number_years = year_max -year_min - delta_t+1
    
    #Compute the first monthly mean
    ds2 = ds.isel(time=slice(0,12*delta_t))
    ds2 = monthly_mean(ds2)
    
    #For each delta_t year span, compute the average
    for t in range(1, number_years):
        dst = ds.isel(time=slice(12*t,12*delta_t + 12*t))
        dst = monthly_mean(dst)
        ds2 = xr.concat([ds2,dst], dim = 'month')
        
    return ds2

def pth_build(Tmean, Pann, Pwsum, Pssum):
    '''
    Given the mean temperature, winter and summer precipitation, compute P_th
    '''
    #Find two thirds of the annual precip
    twothirds = (2/3)*Pann
    
    #Create the winter mask
    winter_mask = twothirds-Pwsum
    winter_mask[winter_mask>0] = 0
    winter_mask[winter_mask<0] = 1
    
    #Create the summer mask
    summer_mask = twothirds-Pssum
    summer_mask[summer_mask>0]=0
    summer_mask[summer_mask<0] = 1
    
    #Remainder mask - note that this will include the location of nan values since those experience zero precip
    else_mask = np.ones_like(Tmean) - winter_mask - summer_mask
    
    #Create Pth
    pth_win = 2*Tmean*winter_mask
    pth_sum = 2*Tmean*summer_mask + 28*summer_mask
    pth_else = 2*Tmean*else_mask + 14*else_mask
    
    pth = pth_win + pth_sum + pth_else
    
    return pth

	
def warm_summer_mask(ds):
    '''
    This function finds the mask for the warm summer climates in the sub-sub-classes of C and D
    '''
    #First, we find the monthly mean temperature for our data set
    monthly_mean = ds.groupby('month.month').mean('month')
    temp_mean = (0.5)*(monthly_mean.Tmax + monthly_mean.Tmin)
    temp_mean = np.array(temp_mean)
    
    #Now we create the mask:
    warmsum = np.copy(temp_mean)
    warmsum = np.nan_to_num(warmsum)
    warmsum[temp_mean<10] = 0
    warmsum[temp_mean>=10] = 1
    warmsum = np.sum(warmsum, axis=0)
    
    return warmsum

	
def is_sum(month):
	'''
	Used to select summer half of year
	'''
    return (month >= 4) & (month <= 9)

def is_win(month):
	'''
	Used to select winter half of year
	'''
    return (month<=3) | (month >=10)

	
###########################
#Examples of building data#
###########################

# # Select the summmer and winter half of years

# dst_summer = dst.sel(month=is_sum(dst['month.month']))
# dst_winter = dst.sel(month=is_win(dst['month.month']))

# # Compute the means, max, etc of the xarray data

# dst_mean = dst.mean(dim='month')
# dst_max = dst.max(dim='month')
# dst_min = dst.min(dim='month')
# dst_acc = dst.sum(dim='month')

# dst_summer_max = dst_summer.max(dim='month')
# dst_summer_min = dst_summer.min(dim = 'month')
# dst_summer_sum = dst_summer.sum(dim='month')

# dst_winter_max = dst_winter.max(dim='month')
# dst_winter_min = dst_winter.max(dim='month')
# dst_winter_sum = dst_winter.sum(dim='month')


# # Convert the xarray data types above into np arrays as needed for biome functions:

# # Year long Tmax, Tmin, Prec min and Prec accumulation
# T_max = np.array(dst_max.Tmax)
# P_ann = np.array(dst_acc.Prec)
# T_min = np.array(dst_min.Tmin)
# P_min = np.array(dst_min.Prec)

# # Total Prec in summer and winter
# P_s_sum = np.array(dst_summer_sum.Prec)
# P_w_sum = np.array(dst_winter_sum.Prec)

# # Min and max of Prec in summer and winter
# P_s_min = np.array(dst_summer_min.Prec)
# P_w_min = np.array(dst_winter_min.Prec)
# P_w_max = np.array(dst_winter_max.Prec)
# P_s_max = np.array(dst_summer_max.Prec)

# T_mean = 0.5*(T_max + T_min)
