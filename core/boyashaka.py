
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sktime.datasets import load_airline
from sktime.utils.plotting import plot_series

y = load_airline()
plot_series(y)
# plt.show()
print(y.index)

fh = np.arange(1, 37)
fh
print(fh)
fh = np.array([2,5])

from sktime.forecasting.base import ForecastingHorizon

fh = ForecastingHorizon(
    pd.PeriodIndex(pd.date_range("1961-01", periods=36, freq="M")),
    is_relative=False
)

cutoff = pd.Period("1960-12", freq="M")
fh.to_relative(cutoff)
fh.to_absolute(cutoff)

from sktime.forecasting.naive import NaiveForecaster

forecaster = NaiveForecaster(strategy="last")
forecaster.fit(y)

y_pred = forecaster.predict(fh)
plot_series(y, y_pred, labels=["y", "y_pred"])
plt.show()

# step 1: data specification
y = load_airline()

# step 2: specifying forecasting horizon
fh = np.arange(1, 37)

# step 3: specifying the forecasting algorithm
forecaster = NaiveForecaster(strategy="last", sp=12)

# step 4: fitting the forecaster
forecaster.fit(y)

# step 5: querying predictions
y_pred = forecaster.predict(fh)

plot_series(y, y_pred, labels=["y", "y_pred"])
plt.show()





