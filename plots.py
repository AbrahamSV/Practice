import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib as mpl

#Setting up the environment
sb.set()
mpl.pyplot.ion()

#Reading a dataset with pandas
iris= pd.read_csv("iris.csv")
#Renaming ALL columns indexes
iris.columns=["ID", "slength", "swidth", "plength", "pwidth", "species"]

#Adding columns with categorical values
iris["region"]= "Asia"
iris.loc[23:54,"region"]= "Europe"
iris.loc[55:,"region"]= "Africa"
iris.loc[84:,"region"]= "America"
#Converting the variable as an actual categorical variable
iris["region"].astype("category")

#Joint plot, regression (abline included)
p= sb.jointplot(x="slength", y="plength", data=iris, kind="reg",
                        truncate=False, color="m", height=7)
p.set_axis_labels("Sepal Length (mm)", "Petal Length (mm)")

r = sb.lmplot(x="slength", y="plength", hue="species",
              truncate=False, data=iris)
r.set_axis_labels("Sepal Length (mm)", "Petal Length(mm)")

#Reading and manipulating datasests
tle= pd.read_excel("Datos 14TLE (11.2018).xlsx")
#Replacing specific values for categories
tle["Diagnóstico"]=tle["Diagnóstico"].replace(1, "TLE")
tle["Diagnóstico"]=tle["Diagnóstico"].replace(2, "Control")
tle["Diagnóstico"]= tle["Diagnóstico"].astype("category")
tle["QuejaMem"]= tle["QuejaMem"].replace(0,"No")
tle["QuejaMem"]= tle["QuejaMem"].replace(1,"Yes")
#Renaming SINGLE column indexes
tle.rename(columns={"QuejaMem":"MemComplaint"}, inplace=True)
#Replacing specific index(rows) values
tle.loc[24:27,"MemComplaint"]= "No"

#Violin plot
v= sb.catplot(x="Diagnóstico", y="StoryFR10m", hue= "MemComplaint",
           kind="violin", split=True, data=tle)
v.set_axis_labels("", "Story Forgetting Rate (10min)")

#Exporting data frames
iris.to_csv("iris_rev", index=False) #you can specify delimiter with "sep="
iris.to_excel("iris_rev.xlsx", index=False) #also to excel...
iris.to_stata("iris_rev.dta", index=False) #and stata...

#Exporting the plots
p.savefig("jointplot.png")
v.savefig("violplot.png")
r.savefig("regplot.png")

