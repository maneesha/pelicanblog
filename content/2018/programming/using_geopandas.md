Title: Python and GeoPandas
Date: 2018-06-22
Category: Programming
Tags: python, pandas

I recently worked on a [report](https://github.com/carpentries/assessment/tree/master/programmatic-assessment/workshops) documenting instructor and workshop activities for [The Carpentries](https://www.carpentries.org).  Much of it was built using [Pandas](https://pandas.pydata.org/), a tool I am relatively familiar with. I also included some geospatial visualizations, using [GeoPandas](http://geopandas.org) for the first time.

The Python GeoPandas library works much like Pandas, but for geographical data.  See [installation instructions](http://geopandas.org/install.html).

It comes with a [few datasets](https://github.com/geopandas/geopandas/tree/master/geopandas/datasets) to plot country maps (polygons), city maps (points), and New York City boroughs (polygons).

I used the `countries` dataset merged with my own data to plot a choropleth map of my country data.  The `countries` dataset is a GeoDataFrame that includes columns for population, continent, country name, 3 character country code, GDP, and geometry (polygon).

I started by importing all the things.

```
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
```

I read the `countries` data set into a variable called world and see the columns it includes.

```
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.columns

```

Output:
```
Index(['pop_est', 'continent', 'name', 'iso_a3', 'gdp_md_est', 'geometry'], dtype='object')
```

I also have my own dataset, as a Pandas dataframe, called `country_data`

```
country_data
```

Output:
```
id  date    country
4251    2016-02-03  US
6269    2016-02-03  NZ
7995    2016-02-03  US
1701    2016-02-04  GB
8221    2016-03-16  AU
# ...
```

However, my data had all countries stored as two digit character codes, not three as the GeoPandas data uses.  To fix this I used `pycountry`.  I wrote a function that takes the two digit code, gets the related country, and returns its three digit code. That function is then applied to the dataframe.



```
import pycountry

def get_country_name(alpha_code):
    return pycountry.countries.get(alpha_2=alpha_code).alpha_3

country_data['country'] = country_data['country'].apply(get_country_name)
```
Output:

```
id  date    country
4251    2016-02-03  USA
6269    2016-02-03  NZL
7995    2016-02-03  USA
1701    2016-02-04  GBR
8221    2016-03-16  AUS
# ...
```





I then plotted the GeoPandas map, using the `plot()` function, much as you would with a typical Pandas plot.

```
world.plot()
```
I then did a [Pandas merge](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.merge.html) on the two data sets as follows.

```
# Sample code:
# pd.merge(frame_1, frame_2, how = 'left', left_on = 'county_ID', right_on = 'countyid')


world_merged = pd.merge(world, country_data, how='left', left_on = 'name' , right_on = 'country' )
```

Since I only have data for a few countries, values for all other countries got set to `NaN` in the merge.  I transformed all the `NaN` values to zero.

```
world_merged.fillna(0, inplace=True)
```

Now I can plot the merged data.
I plotted the original world data.  I changed my data set to exclude countries where `count` was zero.

```
world2 = world2[world2['count'] != 0]
```




Use Yellow-Orange-Red color scale.  Color scales can be sequential, diverging, or discrete.  See https://python-graph-gallery.com/197-available-color-palettes-with-matplotlib/ for examples.

```
fig, ax = plt.subplots()


# I didn't want the countries with count=0 to show in the legend or color scale so I dropped them from the dataframe. 
world2 = world2[world2['count'] != 0] 

# Plotted the original `world` data set, with black outlines and gray fill on the axes already defined.  Without this, only the countries with values greater than zero would plot.
world.plot(ax=ax, color='#DCDCDC', edgecolor='black')

# Over that plot my data, on the same axes.  

world2.plot(ax=ax, column='count', categorical=True, legend=True, cmap="YlOrRd", edgecolor = 'black')

# Display the map

# plt.show()

```

The initial plot will be small.  To make it bigger and keep it to scale I got the figure size, looked at the  height and width proportion, and used it to set a new figure size.  

```
size = fig.get_size_inches()*fig.dpi 
```

It was a ratio of 1.5:1 so I set the new figure size, back above where I set up the original `fig, ax`.  It has to be set here - it didn't work when I tried to set `figsize` anywhere else.

```
fig, ax = plt.subplots(figsize=(18,12)) 
```

The plot includes x and y axis ticks by default, which are useful for most charts and graphs but not for a map like this. Here's a shorthand way of hiding them (before calling `plt.show()` above):

```
plt.xticks([], [])
plt.yticks([], [])
```
Lastly, all the numeric values are floats, but I needed them to be ints since they represent counts. Turns out Pandas coerces new numeric values to floats by default.


Since my data represents counts, and Pandas defaults to all numeric data types as floats, I had to transform them to `int`.

```
world_merged['count'] = world_merged['count'].astype(int) 
```

I also wanted to give my map a title. This isn't assigned like most Pandas plots. Box plots also do it this way -- I don't know why.

```
title = "MY MAP"
ax.set_title(title)
ax.get_figure().suptitle("")
```


So the final code to draw the map looks like this:

```
fig, ax = plt.subplots(figsize=(18,12)) 

title = "MY MAP"
ax.set_title(title)
ax.get_figure().suptitle("")

# I didn't want the countries with count=0 to show in the legend or color scale so I dropped them from the dataframe.
world_merged = world_merged[world_merged['date'] != 0] 

# Plotted the original `world` data set, with black outlines and gray fill on the axes already defined
world.plot(ax=ax, color='#DCDCDC', edgecolor='black')

# Over that plot my data, on the same axes.  

world_merged.plot(ax=ax, column='date', categorical=True, legend=True, cmap="YlOrRd", edgecolor = 'black')


plt.xticks([], [])
plt.yticks([], [])
# Display the map

plt.show()
```





The geopandas documentation makes you think you have to use the `scheme` option to manipulate this more. For simple categorial maps the `scheme` option is not necessary.