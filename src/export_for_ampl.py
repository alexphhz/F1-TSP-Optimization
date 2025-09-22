import unicodedata, re, numpy as np, pandas as pd
from pathlib import Path
from .calculate_matrix import calculate_distance_matrix

def sanitize(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_str = "".join(c for c in nfkd if not unicodedata.combining(c))
    s = ascii_str.replace("&", "and")
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if s and s[0].isdigit(): s = "_" + s
    return s

def write_ampl_dat(df: pd.DataFrame, dist: np.ndarray, out_path: Path):
    symbols = [sanitize(c) for c in df["City"]]
    with out_path.open("w", encoding="utf-8") as f:
        f.write("set CITIES := " + " ".join(symbols) + ";\n\n")
        f.write("param name {CITIES} :=\n")
        for sym, raw in zip(symbols, df["City"]):
            f.write(f"  {sym} \"{raw}\"\n")
        f.write(";\n\n")

        alias = {
            "SAKHIR": "Sakhir",
            "JEDDAH": "Jeddah",
            "MELBOURNE": "Melbourne",
            "SHANGHAI": "Shanghai",
            "SUZUKA": "Suzuka",
            "MONACO": "Monaco",
            "SILVERSTONE": "Silverstone",
            "MONZA": "Monza",
            "SPA_FRANCORCHAMPS": "Spa-Francorchamps",
            "MONTREAL": "Montreal",
            "MIAMI": "Miami",
            "AUSTIN": "Austin",
            "MEXICO_CITY": "Mexico City",
            "SAO_PAULO": "São Paulo",
            "LAS_VEGAS": "Las Vegas",
            "SINGAPORE": "Singapore",
            "BAKU": "Baku",
            "BUDAPEST": "Budapest",
            "SPIELBERG": "Spielberg",
            "LUSAIL": "Lusail",
            "YAS_MARINA_ABU_DHABI": "Yas Marina (Abu Dhabi)",
            "IMOLA": "Imola",
        }
        for k, raw in alias.items():
            f.write(f'param {k} := {sanitize(raw)};\n')
        f.write("\n")

        f.write("param dist:\n  " + " ".join(symbols) + " :=\n")
        for i, si in enumerate(symbols):
            row = " ".join(f"{dist[i,j]:.0f}" if i!=j else "0" for j in range(len(symbols)))
            f.write(f"  {si} {row}\n")
        f.write(";\n")

if __name__ == "__main__":
    df = pd.read_excel("data/f1_tracks.xlsx")
    D = calculate_distance_matrix(df)
    out = Path("ampl/f1_tsp.dat")
    out.parent.mkdir(parents=True, exist_ok=True)
    write_ampl_dat(df, D, out)
    print(f"Wrote {out}")
