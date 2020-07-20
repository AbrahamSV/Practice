import numpy as np
import pandas as pd
import matplotlib.pyplot as mpl
import seaborn as sb
import scipy.stats as stats

df = pd.read_excel("alftle.xlsx")

# DATA WRANGLING
#---Deleting empty columns
df.drop(["f_hippo", "s_hippo", "aeds","alf", "."], axis=1, inplace=True)
#---Replace missing values
df["female%"].replace(np.nan, df["female%"].mean(), inplace=True) #In this case, with the mean

# DESCRIPTIVE STATISTICS
#---Use ".describe() to get descriptive statistics
df.describe()
df.describe(include=["object"]) #includes only object variables
#---Use ".value_counts()" for categorical variables
df["material"].value_counts() # Only 1 variable at a time! (Pandas' series)
counts=df["material"].value_counts().to_frame()# Pass it to a dataframe
counts.index.name = "material" # Rename index header
counts.rename(columns = {"material": "value_counts"}, inplace=True) # Rename columns

#---Grouping the data by categorical variables
df_grp=df.groupby(["sample", "material"]). mean()

#---Creating a subset of the data to groupby and examine descriptive stats
df_sub=df[["sample", "material", "n"]]
df_gb=df_sub.groupby(["sample", "material"], as_index=False).mean() # We indicate that we don't want to index the variables grouped by

#---Or you can do that in one line
df[["sample","memkind","n"]].groupby(["sample","memkind"]).mean()

#---Pivot grouped data into a table
df_pivot=df_gb.pivot(index="sample", columns="material")

#---Creating a heatmap
mpl.pcolor(df_pivot, cmap='RdBu')
mpl.colorbar()
mpl.show()

fig, ax = mpl.subplots()
im = ax.pcolor(df_pivot, cmap='RdBu')

#----label names
row_labels = df_pivot.columns.levels[1]
col_labels = df_pivot.index

#----move ticks and labels to the center
ax.set_xticks(np.arange(df_pivot.shape[1]) + 0.5, minor=False)
ax.set_yticks(np.arange(df_pivot.shape[0]) + 0.5, minor=False)

#----insert labels
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(col_labels, minor=False)

#----rotate label if too long
mpl.xticks(rotation=90)

fig.colorbar(im)
mpl.show()

#CORRELATION
df.corr() # This yields a matrix wiht correlations between float or int variables
df[["age", "female%"]]. corr() # Correlation between specified variables

#---Pearson coefficient and p value
pearson_coef, p_value= stats.pearsonr(df["female%"], df["age"])
#---Regression plot (creating and exporting it as png)
gender_age= sb.lmplot(x="female%",y="age", truncate=False data=df)
gender_age.savefig("gender_age.png")
#ANOVA
#One Way ANOVA
#---Create a subset to analyse
df_anova=df[["material", "age"]]
grp_anova=df_anova.groupby("material")
#---Perform the ANOVA with scipy.stats
anova_results_1=stats.f_oneway(grp_anova.get_group("Visual")["age"],
                               grp_anova.get_group("Verbal")["age"])

anova_results_2=stats.f_oneway(grp_anova.get_group("Verbal & Visual")["age"],
                               grp_anova.get_group("Visual")["age"])
