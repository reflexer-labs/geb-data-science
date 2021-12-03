
# So covariance is the mean of the product minus the product of the means.

# http://prob140.org/textbook/content/Chapter_13/02_Properties_of_Covariance.html
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

total_s = 16*3600
total_s = 200
period_ma = 7
X = np.random.random((total_s,2))
X[:,0] = np.cos(X[:,0])

df = pd.DataFrame(X, columns=['a', 'b'])
df['prod'] = df['a'] * df['b']
df['a_mean'] = df['a'].rolling(period_ma).mean()
df['b_mean'] = df['b'].rolling(period_ma).mean()
df['prod_mean'] = df['a_mean'] * df['b_mean']

fig, ax = plt.subplots(3, sharex=True, sharey=True)

df['a'][-100:].plot(ax=ax[0], label='a', color='red')
df['a_mean'][-100:].plot(ax=ax[0], label='moving average', color='red')
ax[0].legend(loc="lower right")
df['b'][-100:].plot(ax=ax[1], label='b', color='blue')
df['b_mean'][-100:].plot(ax=ax[1], label='moving average', color='blue')
ax[1].legend(loc="lower right")

df['prod'][-100:].plot(ax=ax[2], label='spot a*b', color='orange')
df['prod_mean'][-100:].plot(ax=ax[2], label='rolling a * rolling b', color='green')
ax[2].legend(loc="lower right")
#plt.legend()
plt.show()
