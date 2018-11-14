# country-power-plant-mapper
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/skoeb/country-power-plant-mapper/master?filepath=PowerPlantMapper.ipynb)

Click the button above to launch this application on a virtual machine. This might take a minute.

Basic Instructions:
Initialize the application by clicking on 'Cell' in the menu bar and selecting 'Run All'.
Enter the Country Name.
Choose the desired level of Simplification for resource type:
Simple breaks resources into 'Renewable', 'Fossil', and 'Nuclear'.
Mixed subdivides renewables (solar, wind, etc.) but keeps 'Fossil' together.
Complex labels every resource type.
Press the Update Plot button. Be patient, it can take a few seconds.
Drag the legend to a better location, if needed (this can be a little wonky––try clicking after moving to ).
To save the image, click the power symbol in the upper right portion of the map. Then right click on the map and select 'Save Image As'.
Advanced Instructions:
Coordinate System sets the crs used in the map projection. The default value is spherical which uses EPSG:3857. Geo can also be entered for a standard mercator projection (ESPG:4326). A custom CRS can be used by entering the EPSG integer. For example, 5940 (a crs designed for Russia) can be entered to avoid having Russia wrap around the side of the map. Visit EPSG to find custom coordinate systems. Default Value: spherical
Number of Legend Columns. Default Value: 1
Sort Legend By sorts the resources in the legend (not the size indicators) by either alphabetical or by the sum of the capacity of the resource for the selected country. Default Value: capacity
Zoom Level changes the size of the map portion of the plot. This can be useful to adjust the map for different sized screens, or to provide a bigger map for the purpose of saving. WARNING: making this value large enough to produce an image wider than the width of the console will result in erratic results! Default Value: 1.5
Island Size Thresh creates a minimum threshold (in km^2) for the geometry of islands to be included in the map. largest can also be entered to only select the largest geometry for the country. For example, plotting Canada with the default values includes a number of arctic islands that are useless for the purpose of a power plant map (sorry Baffin island). Setting Island Size Thresh to either largest or 8000000 will only display the continental portions of Canada. Default Value: 200 (km^2)
Show Populated Places can be used to draw points on the map in the location of populated cities. Data is drawn from the Natural Earth database of populated places which includes data for an astonishing number of locations. Additionally, arrows are drawn labeling the name of these points (HINT: these labels are draggable, although it doesn't work the best!). Show Populated Places can either be False (i.e. off), or an integer value which sets the minimum population threshold for a city to be included on the map. Default Value: False
Bubble Opacity is used to change the opacity of the powerplant bubbles. Setting it lower can be useful for countries with a large number of overlapping bubbles (i.e. the United States). Default Value: 0.5
Country Precursor allows you to enter a word (or series of words) to appear before the country name in the title of the plot. For instance, if you entered 'Philippines' as the Country Name but want the title to be 'Power Plants in The Philippines' you could enter "The " into Country Precursor. Default Value: None
Title On turns the title at the top on or off. Default: True
Source On turns the source at the bottom on or off. Default: True
Please email me at sam.koebrich@NREL.gov with any bugs, comments, or feature requests!
