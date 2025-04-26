
from pandas_datareader import data as pdr
import datetime 
import matplotlib.pyplot as plt

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime.today()

df_10y = pdr.DataReader('GS10', 'fred', start, end)
df_2y = pdr.DataReader('GS2', 'fred', start, end)
print(df_10y.head())
print(df_2y.head())

df = df_10y.rename(columns={'GS10':'10Y'}).join(df_2y.rename(columns={'GS2':'2Y'}))
df['Spread'] = df['10Y'] - df['2Y']

# plt.figure(figsize=(10,5))
# plt.plot(df.index, df["Spread"])
# plt.show()

from statsmodels.tsa.arima.model import ARIMA
import numpy as np 

train_data = df['Spread']
model = ARIMA(train_data, order=(1,1,1))
model_fit = model.fit()

fc_res = model_fit.get_forecast(steps=30)
print(fc_res)
fc_mean = fc_res.predicted_mean
print(fc_mean)
cf_int = fc_res.conf_int()
print(cf_int)

plt.figure(figsize=(10,5))
plt.plot(train_data.index, train_data, label='obs')
plt.plot(fc_mean.index, fc_mean, label='fc')
plt.fill_between(fc_mean.index, cf_int.iloc[:,0], cf_int.iloc[:,1], color='pink', alpha=0.3)
plt.title('arima forecast of 10y-2y spread')
plt.xlabel('date')
plt.ylabel('spread')
plt.legend()
plt.show()


