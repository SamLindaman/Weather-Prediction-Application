import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.api import qqplot
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

Arma_mod39 = sm.tsa.ARMA(dta_min, (0, 4)).fit()
print(Arma_mod39.aic, Arma_mod39.bic, Arma_mod39.hqic)
resid = Arma_mod39.resid
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=30, ax=ax1)
fig = sm.graphics.tsa.plot_pacf(resid, lags=30, ax=ax2)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit = True)
plt.show()

diff1 = dta_min.diff(1)
# diff1.plot(ax=ax1)
plt.show()

predict_year = 10

predict_end_year = end_year.values[0] + predict_year
predict_dta = Arma_mod39.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)
print(predict_dta)






# print(data.head().dropna(axis='rows', how='any'))
# print('\n Data Types:')
# print(data.dtypes)

# test_stationarity(dta)



