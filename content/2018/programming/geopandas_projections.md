Title: Maps and projections in Geopandas
Date: 2018-11-16
Category: Programming
Tags: python, pandas, geospatial

No map is perfect.  It's impossible to accurately represent a three dimensional object (planet Earth) in two dimensions (a map on paper or on a screen).  Every map representation comes with physical and political biases.  That's why it is important to have a range of options for map projections, to be able to identify the map with the least problematic biases.

I went through a **lot** of pain trying to change the map projection in a report I was creating using Geopandas.  The official documentation makes it look like there are only two projections, WGS84 and Mercator.  It does start by saying that any reputable data source should have projection information included -- but that doesn't account for all the times we come across messy data sources, or that we are generating our own data sets.

There are actually many projections available for Geopandas to use.  I found this out by reading [this guide](https://ramiro.org/notebook/geopandas-choropleth/) which uses the Robinson projections and got me thinking that there must be others.  But what are the others?  They are included in [Basemap's documentation](https://matplotlib.org/basemap/users/), but as it turns out, they can also be used in Geopandas.  




