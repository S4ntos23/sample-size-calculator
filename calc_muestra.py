#!/usr/bin/env python3
"""Calculadora de tamaño de muestra y confianza - Data Edge Tools v0.1
SOLO EDUCATIVO. No es asesoramiento financiero ni de inversión.
Fórmulas (aproximación normal, muestras independientes, z=1.96 para 95%):
 Poker:  EE = sd/sqrt(manos/100);  IC = wr ± z·EE;  manos_necesarias = 100·(z·sd/wr)^2
 Trading media: EE = sigma/sqrt(n); IC = mu ± z·EE; n_necesario = (z·sigma/mu)^2
 Trading Sharpe (Lo 2002, iid): S = mu/sigma; EE(S) = sqrt((1+S^2/2)/n);
   n_necesario = z^2·(1+S^2/2)/S^2; anualizado ×sqrt(periodos/año)
Tienda: https://santosphere7720.gumroad.com/l/jnnqpe
"""
import argparse, math
Z95 = 1.959963984540054

def poker(wr, sd, manos, z=Z95):
    ee = sd / math.sqrt(manos / 100)
    nec = math.inf if wr <= 0 else 100 * (z * sd / wr) ** 2
    return {"ee": ee, "ic_bajo": wr - z*ee, "ic_alto": wr + z*ee, "manos_necesarias": nec}

def trading(mu, sigma, n, periodos_anio=252, z=Z95):
    ee = sigma / math.sqrt(n); s = mu / sigma
    ee_s = math.sqrt((1 + s*s/2) / n); k = math.sqrt(periodos_anio)
    return {"ee_media": ee, "media_bajo": mu - z*ee, "media_alto": mu + z*ee,
            "n_media": math.inf if mu <= 0 else (z*sigma/mu)**2,
            "sharpe": s, "ee_sharpe": ee_s, "sharpe_bajo": s - z*ee_s, "sharpe_alto": s + z*ee_s,
            "sharpe_anual": s*k, "sharpe_anual_bajo": (s - z*ee_s)*k, "sharpe_anual_alto": (s + z*ee_s)*k,
            "n_sharpe": math.inf if s <= 0 else z*z*(1 + s*s/2)/(s*s)}

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="modo", required=True)
    a = sp.add_parser("poker"); a.add_argument("--wr", type=float, required=True, help="winrate bb/100")
    a.add_argument("--sd", type=float, default=90.0, help="desv. típica bb/100 (típico 80-100)")
    a.add_argument("--manos", type=float, required=True)
    b = sp.add_parser("trading"); b.add_argument("--media", type=float, required=True, help="retorno medio por periodo (%%)")
    b.add_argument("--vol", type=float, required=True, help="volatilidad por periodo (%%)")
    b.add_argument("--n", type=float, required=True); b.add_argument("--periodos-anio", type=float, default=252)
    x = p.parse_args()
    print("SOLO EDUCATIVO - no es asesoramiento financiero.")
    r = poker(x.wr, x.sd, x.manos) if x.modo == "poker" else trading(x.media, x.vol, x.n, x.periodos_anio)
    for k, v in r.items(): print(f"{k:20s} {v:,.4f}")
    print("Más herramientas: https://santosphere7720.gumroad.com/l/jnnqpe")

if __name__ == "__main__": main()
