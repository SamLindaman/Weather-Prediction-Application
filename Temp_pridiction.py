import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

data = pd.read_csv('CD.csv', parse_dates=['date'])

#oloumns
dta_min= data['tmin']
dta_year = data['date']

begin_year = dta_year[0:-1].dt.year
end_year = dta_year[-1:].dt.year


#Make index
dta_min = np.array(dta_min, dtype=np.float)
dta_min = pd.Series(dta_min)
dta_min.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))


#plot the graphs
dta_min.plot(figsize=(10, 6)).set_title('Time-series graph for 1 time-series')
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(111)
diff1 = dta_min.diff(1)

#first order difference

diff1.plot(ax =ax1).set_title('Perform First order difference')
diff1 = dta_min.diff(1)
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta_min, lags=30, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta_min, lags=30, ax=ax2)

# Arima Model
Arma_mod39 = sm.tsa.ARMA(dta_min, (0, 4)).fit()
print(Arma_mod39.aic, Arma_mod39.bic, Arma_mod39.hqic)
resid = Arma_mod39.resid
fig = plt.figure(figsize=(10, 4))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=30, ax=ax1)
fig = sm.graphics.tsa.plot_pacf(resid, lags=30, ax=ax2)
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit = True)



#pridict for the future 10 years
predict_year = 10
predict_end_year = end_year.values[0] + predict_year
predict_dta = Arma_mod39.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)

df = predict_dta.to_frame('weather').reset_index()
df.columns = ['years', 'weather']


# Create new .csv file to output the 10 year results
df.index = pd.to_datetime(df.index)
df.to_csv('10_year_prediction.csv', encoding='utf-8', index=False)

dataset = pd.read_csv("10_year_prediction.csv")

dataset.plot()

plt.show()

