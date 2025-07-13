# eda_core/plots/plot_utils.py
import matplotlib.pyplot as plt
import os
from eda_core.io.save_output import get_output_subfolder


def plot_numeric_hist(series, column_name, source_filename: str = "") -> str:

    plot_dir = get_output_subfolder(source_filename, "plots")
    os.makedirs(plot_dir, exist_ok=True)
    path = os.path.join(plot_dir, f"{column_name}_hist.png")    

    plt.figure()
    series.dropna().hist(bins=30, edgecolor='black')
    plt.title(f"Histogram – {column_name}")
    plt.xlabel(column_name)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path

def plot_box(series, column_name, source_filename: str = "") -> str:

    plot_dir = get_output_subfolder(source_filename, "plots")
    os.makedirs(plot_dir, exist_ok=True)
    path = os.path.join(plot_dir, f"{column_name}_box.png")    

    plt.figure()
    plt.boxplot(series.dropna(), vert=False)
    plt.title(f"Box Plot – {column_name}")
    plt.xlabel(column_name)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path
