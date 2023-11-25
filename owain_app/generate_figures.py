import json
import os
import seaborn as sns
import matplotlib.pyplot as plt
from loguru import logger
from owain_app.catalog import Catalog


def load_data(catalog, rule_names, notation_type):
    data = catalog.data_load(rule_names, notation_type)
    return data["train"], data["test"]


def plot_data_distribution(train_data, test_data, rule_names, catalog):
    sns.set(style="whitegrid", font_scale=1.5)
    plt.figure(figsize=(10, 6))

    # Example plot (modify as needed for your analysis)
    feature_counts = [data.count("1") for data in train_data + test_data]
    sns.histplot(feature_counts, kde=True, color="skyblue", bins=10)
    plt.title(f"Feature Distribution for Rules {' and '.join(rule_names)}")
    plt.xlabel("Number of 1s")
    plt.ylabel("Frequency")

    fig_path = os.path.join(
        catalog.figures_path, f"distribution_rules_{'_'.join(rule_names)}.png"
    )
    plt.savefig(fig_path)
    plt.close()
    logger.info(f"Figure saved to {fig_path}")


def main():
    logger.add("generate_figures.log", rotation="10 MB")
    logger.info("Starting figure generation")

    catalog = Catalog()
    rule_names = ["rule1", "rule2"]  # Example, adjust as needed
    train_data, test_data = load_data(catalog, rule_names, "string_notation")

    plot_data_distribution(train_data, test_data, rule_names, catalog)
    logger.info("Figure generation completed")


if __name__ == "__main__":
    main()
