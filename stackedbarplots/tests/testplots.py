
import sys
import pandas as pd
import numpy as np

sys.path.append("../sample")
from stackedbarplots import *
from tools import *
#from stackedbarplots import basic, centered
#from tools import ColourGradient

firstcolumn = "total_deaths_per_million"
secondcolumn = "total_tests_per_thousand"

df = pd.read_csv("owid-covid-data.csv")[["location", "date", firstcolumn, secondcolumn]]
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df[firstcolumn] = pd.to_numeric(df[firstcolumn], errors="coerce")
df[secondcolumn] = pd.to_numeric(df[secondcolumn], errors="coerce")
df = df[(df['date'] >= '2021-01-01') & (df['date'] < '2022-01-01')]
df = df.dropna()


# df["total_deaths_pm_2021"] = df[firstcolumn] - df[firstcolumn].min()



#df[firstcolumn] = df[firstcolumn]/1000.0#np.log(df[firstcolumn])
#df[secondcolumn] = df[secondcolumn]/1000.0#np.log(df[secondcolumn])
df["start_deaths_per_million"] = df["total_deaths_per_million"]
df["start_tests_per_million"] = df["total_tests_per_thousand"]
#df[secondcolumn] = np.log(df[secondcolumn])#np.log(df["human_development_index"])

#print(df.head())

# Depending on the OWID data version, this field may contain either
# percentages (0-100) or fractions (0-1). Use the same percentage scale
# for both columns before grouping and plotting.
#if df[firstcolumn].max() <= 1: df[firstcolumn] *= 100
#if df["people_vaccinated_per_hundred"].max() <= 1: df["people_vaccinated_per_hundred"] *= 100

df = df.groupby("location").agg({"total_deaths_per_million": "max",
                                    "start_deaths_per_million": "min",
                                    "total_tests_per_thousand": "max",
                                    "start_tests_per_million": "min"
})

df["total_deaths_per_million_2021"] = df["total_deaths_per_million"] - df["start_deaths_per_million"]
df["total_tests_per_thousand_2021"] = df["total_tests_per_thousand"] - df["start_tests_per_million"]


#[[firstcolumn, secondcolumn]].max()
#df["people_unvaccinated"] = 100 - df["people_fully_vaccinated_per_hundred"]
df = df[["total_deaths_per_million_2021", "total_tests_per_thousand_2021"]]


result = df.apply(list, axis=1).to_dict()

EUCountries = [
"Austria",
"Belgium",
"Bulgaria",
"Croatia",
"Cyprus",
"Czechia",
"Denmark",
"Estonia",
"Finland",
"France",
"Germany",
"Greece",
"Hungary",
"Ireland",
"Italy",
"Latvia",
"Lithuania",
"Luxembourg",
"Malta",
"Netherlands",
"Poland",
"Portugal",
"Romania",
"Slovakia",
"Slovenia",
"Spain",
"Sweden",
]
subset = {k: v for k, v in result.items() if k in EUCountries}


custom_colour = ColourGradient()
custom_colour.set_colour_gradient_list([(227, 108, 85), (101, 219, 133)])

basic_plot = centered(subset, ["Total COVID-19 Deaths Per Million People in 2021", "Total COVID-19 Tests Per 1,000 People in 2021"], fig_size=(10, 8))

basic_plot.set_bar_style(bar_gradient=custom_colour)

basic_plot.set_axis_style(y_font_size=10, x_axis_show=False)
basic_plot.set_bar_style(ordered="descending")
basic_plot.set_fig_style(spine_display=(False, False, False, False))

basic_plot.set_bar_labels_style(bar_value_format="{0:.0f}", font_size=8, align="left", padd_thresh=1000, end_thresh_padd=True, padding=100)
basic_plot.set_legend_style(show=True, placement="above-horizontal", background_colour="white", border_colour="white", transform=[-.2, -.03], font_size=10)

basic_plot.set_vert_line_style(line_style="--", alpha=.9)

basic_plot.render()
basic_plot.save("COVID-Deaths-Tests-Fig.png")


#https://github.com/owid/covid-19-data/tree/master/public/data
#https://github.com/Opensourcefordatascience/Data-sets
#https://github.com/mwaskom/seaborn-data/blob/master/mpg.csv