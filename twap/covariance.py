
# covariance is the mean of the product minus the product of the means.
# http://prob140.org/textbook/content/Chapter_13/02_Properties_of_Covariance.html
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

total_s = 16*3600
X = np.random.random((total_s,2))
X[:,0] = np.cos(X[:,0])

df = pd.DataFrame(X, columns=['a', 'b'])
df['prod'] = df['a'] * df['b']
e_xy = df['prod'].mean()
ex_ey = df['a'].mean() * df['b'].mean()
cov_xy = df['a'].cov(df['b'])

mean_diffs = []
for n in range(4, 100, 1):
    d = []
    for _ in range(100):
        df_s = df.sample(n)
        cov_xy_est = df_s['a'].cov(df_s['b'])

        #e_xy_est = cov_xy + ex_ey
        #diff = abs(e_xy - e_xy_est)
        diff = abs(cov_xy - cov_xy_est)
        d.append(diff)
    mean_diffs.append(np.mean(d))

plt.plot(range(len(mean_diffs)), mean_diffs)
plt.show()
