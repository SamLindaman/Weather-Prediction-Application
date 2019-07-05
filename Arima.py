import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# def test_stationarity(timeSeries):
#     # Determining rolling statistics
#     rolmean = timeSeries.rolling(12).mean()
#     rolstd = timeSeries.rolling(12).std()
#
#     # Plot rolling Statistics:
#     orig = plt.plot(timeSeries, color='blue', label='Original')
#     mean = plt.plot(rolmean, color='red', label='Rolling Mean')
#     std = plt.plot(rolstd, color='black', label='Rolling Std')
#     plt.legend(loc='best')
#     plt.title('Rolling Mean & Std Deviation')
#     plt.show()
#
#     # perform dickey-Fuller test:
#     print('Results of Test:')
#     dftest = adfuller(timeSeries, autolag='AIC')
#     dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
#     for key, value in dftest[4].items():
#         dfoutput['Critical Val (%s)' % key] = value
#     print(dfoutput)


# dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
data = pd.read_csv('CD.csv', parse_dates=['date'])


dta_min = data['tmin']
dta_year = data['date']
# dta_min.head(10)

begin_year = dta_year[0:1].dt.year
end_year = dta_year[-1:].dt.year

dta_min = np.array(dta_min, dtype=np.float)
dta_min = pd.Series(dta_min)
dta_min.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))

dta_min.plot(figsize=(10, 6))
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_acf(dta_min, lags=30, ax=ax1)
fig = sm.graphics.tsa.plot_pacf(dta_min, lags=30, ax=ax2)

diff1 = dta_min.diff(1)
# diff1.plot(ax=ax1)
plt.show()




# print(data.head().dropna(axis='rows', how='any'))
# print('\n Data Types:')
# print(data.dtypes)

# test_stationarity(dta)



