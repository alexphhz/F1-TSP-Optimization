import unicodedata, re, pandas as pd
from .tsp_visualization import plot_route

def sanitize(s:str):
    nfkd = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in nfkd if not unicodedata.combining(c))
    s = s.replace("&", "and")
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if s and s[0].isdigit(): s = "_" + s
    return s

if __name__ == "__main__":
    df = pd.read_excel("data/f1_tracks.xlsx")
    amap = { sanitize(c): c for c in df["City"] }

    sch = pd.read_csv("data/schedule_order.csv")  # CitySymbol,Round
    sch = sch.sort_values("Round")
    order_cities = [amap[sym] for sym in sch["CitySymbol"].tolist()]
    idx = {c: i for i, c in enumerate(df["City"])}
    path = [idx[c] for c in order_cities] + [idx[order_cities[0]]]
    plot_route(df, path, title="AMPL Optimized Schedule")
