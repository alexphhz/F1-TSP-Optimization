import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_route(df: pd.DataFrame, path, title="F1 Race Calendar"):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.LAND, color="lightgray")
    ax.add_feature(cfeature.OCEAN, color="lightblue")
    # Plot segments
    for i in range(len(path) - 1):
        a = df.iloc[path[i]]
        b = df.iloc[path[i + 1]]
        ax.plot([a["Longitude"], b["Longitude"]],
                [a["Latitude"], b["Latitude"]],
                linewidth=1, marker="o", transform=ccrs.Geodetic())
        ax.text(a["Longitude"] + 2, a["Latitude"] - 2, a["City"], fontsize=9, transform=ccrs.Geodetic())
    plt.title(title, fontsize=20)
    plt.show()
