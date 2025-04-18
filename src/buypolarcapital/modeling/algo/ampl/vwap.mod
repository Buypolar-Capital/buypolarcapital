set TIMES;

param price {TIMES};        # Estimated price per time bucket
param max_volume {TIMES};   # Max volume allowed per time bucket
param total_shares;         # Total shares to be traded

var x {t in TIMES} >= 0;     # Shares traded in time t

minimize Total_Cost:
    sum {t in TIMES} price[t] * x[t];

subject to TotalVolume:
    sum {t in TIMES} x[t] = total_shares;

subject to VolumeCap {t in TIMES}:
    x[t] <= max_volume[t];
