

import bayesloop as bl
S = bl.ChangepointStudy()
S.loadExampleData()

L = bl.om.Poisson('accident_rate', bl.oint(0, 6, 1000))
T = bl.tm.ChangePoint('change_point', 'all')

mod = S.set(L, T)
res = mod.fit()

print(res.summary())