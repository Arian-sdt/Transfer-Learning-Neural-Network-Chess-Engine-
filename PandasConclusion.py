import sys
import pandas as pd 
from scipy import stats
from statsmodels.stats import multicomp
import statsmodels.api as sm
import matplotlib.pyplot as plt

def main():

    model1 = pd.read_csv("original.csv")
    model2 = pd.read_csv("weighted.csv")
    model3 = pd.read_csv("morelayers.csv")
    model4 = pd.read_csv("lichess.csv")
    model5 = pd.read_csv("TL1.csv")
    model6 = pd.read_csv("TL2.csv")
    
    
    # Accuracy Tukey
    accuracy_df = pd.DataFrame({
        "Model 1": model1["accuracy%"],
        "Model 2": model2["accuracy%"],
        "Model 3": model3["accuracy%"],
        "Model 4": model4["accuracy%"],
        "Model 5": model5["accuracy%"],
        "Model 6": model6["accuracy%"]
    })
    accuracy_melt = accuracy_df.melt()
    tukey_accuracy = multicomp.pairwise_tukeyhsd(
        accuracy_melt['value'], accuracy_melt['variable'], alpha=0.05
    )
    print(tukey_accuracy)

    fig = tukey_accuracy.plot_simultaneous()
    ax = fig.axes[0]
    ax.set_title("Accuracy Percentage Confidence Intervals")
    plt.show()
    
    
    # AvgSPLoss Tukey
    AvgSPLoss_df = pd.DataFrame({
        "Model 1": model1["AvgSPLoss"],
        "Model 2": model2["AvgSPLoss"],
        "Model 3": model3["AvgSPLoss"],
        "Model 4": model4["AvgSPLoss"],
        "Model 5": model5["AvgSPLoss"],
        "Model 6": model6["AvgSPLoss"]

    })
    AvgSPLoss_melt = AvgSPLoss_df.melt()
    tukey_sploss = multicomp.pairwise_tukeyhsd(
        AvgSPLoss_melt['value'], AvgSPLoss_melt['variable'], alpha=0.05
    )
    print(tukey_sploss)

    fig = tukey_sploss.plot_simultaneous()
    ax = fig.axes[0]
    ax.set_title("Average Centipawn Loss Confidence Intervals")
    plt.show()


if __name__ == '__main__':
    main()


