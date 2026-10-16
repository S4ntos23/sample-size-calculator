import math, random, statistics
from calc_muestra import poker, trading, Z95
r = poker(5, 100, 10000)                      # EE = 100/sqrt(100)=10
assert abs(r["ee"]-10)<1e-12 and abs(r["ic_bajo"]-(5-19.6))<0.01
assert abs(r["manos_necesarias"]-100*(Z95*20)**2)<1e-6   # ~1.537M manos
assert abs(poker(5,100,r["manos_necesarias"])["ic_bajo"])<1e-9  # en n necesario, límite inferior = 0
assert math.isinf(poker(-1,90,1000)["manos_necesarias"])
t = trading(0.1, 1.0, 400)
assert abs(t["ee_media"]-0.05)<1e-12 and abs(t["n_media"]-Z95**2*100)<1e-9
assert abs(t["ee_sharpe"]-math.sqrt(1.005/400))<1e-12
assert abs(trading(0.1,1,t["n_sharpe"])["sharpe_bajo"])<1e-9
# Monte Carlo: cobertura IC media ~95% y EE del Sharpe
random.seed(1); cov=0; sh=[]
for _ in range(4000):
    x=[random.gauss(0.1,1) for _ in range(400)]
    m=statistics.fmean(x); s=statistics.stdev(x); sh.append(m/s)
    cov += abs(m-0.1) <= Z95*s/20
print("cobertura IC media:", cov/4000, "| EE Sharpe MC:", round(statistics.stdev(sh),5), "fórmula:", round(t["ee_sharpe"],5))
assert 0.935 < cov/4000 < 0.965 and abs(statistics.stdev(sh)-t["ee_sharpe"])<0.003
print("TODAS LAS PRUEBAS OK"); print(r); print(t)
