#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 22:04:54 2018

@author: skoebric
"""
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import ipywidgets as widgets
import powerplantmapper as ppm
import matplotlib.pyplot as plt

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:85% !important; }</style>"))

style = {'description_width': 'initial'}
    
countrynamewidget = widgets.Text(
                    value='India',
                    placeholder='Type a country name',
                    description='Country Name:',
                    disabled=False,
                    style = style
                )

simplifiedwidget = widgets.ToggleButtons(
                    options=['Simple', 'Mixed', 'Complex'],
                    value = 'Mixed',
                    description='Simplification Level:',
                    disabled=False,
                    button_style='',
                    tooltips=['Renewables, Fossil, and Nuclear',
                              'Solar, Wind, Hydro, Geothermal,Biomass, Wave and Tidal,\n Storage, Fossil, Nuclear',
                              'Solar, Wind, Hydro, Geothermal,Biomass, Wave and Tidal,\n Storage, Fossil, Nuclear, Coal, Gas, Oil, Waste, Cogeneration'],
                              style = style)

precursorwidget = widgets.Text(
                    value='',
                    placeholder='Precursor to Country Name',
                    description='Country Precursor:',
                    disabled=False,
                    style = style
                )
    
coordswidget = widgets.Text(
                value='spherical',
                placeholder='Type something',
                description='Coordinate System:',
                disabled=False,
                style = style
            )

legendcolumnswidget = widgets.IntSlider(
                        value=1,
                        min=1,
                        max=3,
                        step=1,
                        description='Number of Legend Columns:',
                        disabled=False,
                        continuous_update=False,
                        orientation='horizontal',
                        readout=True,
                        readout_format='d',
                        style = style
                )

legendsortingwidget = widgets.Dropdown(
                        options=['capacity', 'alphabetical'],
                        value='capacity',
                        description='Sort Legend By:',
                        disabled=False,
                        style = style
                    )

zoomwidget = widgets.FloatSlider(
                value=1,
                min=0.5,
                max=3,
                step=0.1,
                description='Zoom Level:',
                disabled=False,
                continuous_update=False,
                orientation='horizontal',
                readout=True,
                readout_format='.1f',
                style = style
            )


islandthreshwidget = widgets.Text(
                        value='5000',
                        placeholder='Type a island thresh',
                        description='Island Size Thresh:',
                        disabled=False,
                        style = style
                    )


popplaceswidget = widgets.Text(
                    value='False',
                    placeholder='Type something',
                    description='Show Populated Places:',
                    disabled=False,
                    style = style
                )

bubbleopacitywidget = widgets.FloatSlider(
                        value=0.5,
                        min=0,
                        max=1,
                        step=0.1,
                        description='Bubble Opacity:',
                        disabled=False,
                        continuous_update=False,
                        orientation='horizontal',
                        readout=True,
                        readout_format='.1f',
                        style = style
                    )

pathwidget = widgets.Text(
                    value='/Users/skoebric/Downloads/XYZ.png',
                    placeholder='Type the complete path to save to',
                    description='Path to save to:',
                    disabled=False,
                    style = style
                )

dpiwidget = widgets.IntSlider(
                        value=300,
                        min=100,
                        max=500,
                        step=1,
                        description='DPI (resolution):',
                        disabled=False,
                        continuous_update=False,
                        orientation='horizontal',
                        readout=True,
                        readout_format='d',
                        style = style
                )

dpiwidget = widgets.IntSlider(
                        value=300,
                        min=100,
                        max=500,
                        step=1,
                        description='DPI (resolution):',
                        disabled=False,
                        continuous_update=False,
                        orientation='horizontal',
                        readout=True,
                        readout_format='d',
                        style = style
            )

titlewidget = widgets.RadioButtons(
                options=[True, False],
                value= True,
                description='Title On:',
                disabled=False
            )

sourcewidget = widgets.RadioButtons(
                options=[True, False],
                value= True,
                description='Source On:',
                disabled=False
            )

disputedwidget = widgets.RadioButtons(
                options=[True, False],
                value= True,
                description='Include Disputed Territories:',
                disabled=False
            )
    
def showbasicwidgets():
    global countrynamewidget, simplifiedwidget
    display(countrynamewidget)
    display(simplifiedwidget)
    
def showadvancedwidgets():
    global precursorwidget, coordswidget, legendcolumnswidget, legendsortingwidget, zoomwidget, islandthreshwidget, popplaceswidget, bubbleopacitywidget
    display(coordswidget)
    display(legendcolumnswidget)
    display(legendsortingwidget)
    display(zoomwidget)
    display(islandthreshwidget)
    display(popplaceswidget)
    display(bubbleopacitywidget)
    display(precursorwidget)
    display(titlewidget)
    display(sourcewidget)
    display(disputedwidget)
    
    
def createplot():
    initial = ppm.CountryPowerPlantMapper(countryname = countrynamewidget.value, zoom = zoomwidget.value,
                 coords = coordswidget.value, legend_columns = legendcolumnswidget.value,
                 legend_sorting = legendsortingwidget.value, precursor = precursorwidget.value,
                 island_thresh = islandthreshwidget.value, additional_powerplants_csv = None,
                 populated_places = popplaceswidget.value, urban_areas = None,
                 bubble_opacity = bubbleopacitywidget.value, simplified = simplifiedwidget.value,
                 title = titlewidget.value, source = sourcewidget.value, disputed = disputedwidget.value)
    initial.mapper()

def updateplot():
    from IPython.display import clear_output
    
    mapwidget = widgets.Button(
                    description='Update Plot',
                    disabled=False,
                    button_style='', # 'success', 'info', 'warning', 'danger' or ''
                    tooltip='Update Plot',
                    icon='check',
                    layout=widgets.Layout(width='70%', height='80px'))
    
    def on_button_clicked(b):
        clear_output()
        display(mapwidget)
        u = ppm.CountryPowerPlantMapper(countryname = countrynamewidget.value, zoom = zoomwidget.value,
                     coords = coordswidget.value, legend_columns = legendcolumnswidget.value,
                     legend_sorting = legendsortingwidget.value, precursor = precursorwidget.value,
                     island_thresh = islandthreshwidget.value, additional_powerplants_csv = None,
                     populated_places = popplaceswidget.value, urban_areas = None,
                     bubble_opacity = bubbleopacitywidget.value, simplified = simplifiedwidget.value,
                     title = titlewidget.value, source = sourcewidget.value, disputed = disputedwidget.value)
        u.mapper()
 
    mapwidget.on_click(on_button_clicked)
    display(mapwidget)
    createplot()
    
    