#%%
import matplotlib.pyplot as plt
import numpy as np
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure, show, output_file
output_notebook()
N = 3
TOOLS="pan,wheel_zoom,box_select,lasso_select,reset"
files = ['s%d-eth1.csv' % (i) for i in range(N)]
#%%
res = {}
listf = []
for name in files:
    listf.append(open(name, 'r'))
    for line in listf[-1]:
        split = line.split(', ')
        rtt = float(split[4][0:-1])
        ident = str(split[0:4])
        if ident not in res:
            res[ident] = []
        res[ident].append(rtt)

#%%
arrays =res.values()
arrays = [a for a in arrays if len(a)==3]
X = np.stack(arrays)
X
len(X)
#%%
np.cov(X.T)
#%%
for i in range(N):
    print('avg/sigma', np.mean(X[:, i]), np.var(X[:, i]))
#%%
for i in range(N):
    plt.plot(X[:, i])

plt.show()

#%%
A = np.diag(np.ones(N))-np.diag(np.ones(N-1), k=-1)
XT = np.dot(X, A)

#%%
for i in range(N):
    print('avg/sigma', np.mean(XT[:, i]), np.var(XT[:, i]))
#%%
for i in range(N):
    plt.plot(XT[:, i])
plt.show()

#%%
print('Esperado')
print([20+4*(i+1) for i in range(N)])
for i in range(N):
    p = figure(title='Salto %d\n Media %.6fms\n Mediana %.6fms' % (i+1, 1000*np.mean(XT[:, i]), 1000*np.median(XT[:, i])),
            background_fill_color="#E8DDCB",
            x_axis_type="log",
            tools = TOOLS)
    hist, edges = np.histogram(XT[:,i], bins=25)
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#036564", line_color="#033649")
    show(p)
np.cov(XT.T)*1000

#%%
print('Esperado')
a = [20+4*(i+1) for i in range(N)]
a = np.sum(a) - np.cumsum(a)
print(a)
for i in range(N):
    p = figure(title='Salto %d\n Media %.6fms\n Mediana %.6fms' % (i+1, 1000*np.mean(X[:, i]), 1000*np.median(X[:, i])),
            background_fill_color="#E8DDCB",
            x_axis_type="log",
            tools = TOOLS)
    hist, edges = np.histogram(X[:,i], bins=25)
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#036564", line_color="#033649")
    show(p)
np.cov(X.T)*1000