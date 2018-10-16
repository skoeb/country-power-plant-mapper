#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 22:04:54 2018

@author: skoebric
"""
import ipywidgets as widgets
import powerplantmapper as ppm
import matplotlib.pyplot as plt

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
                value=1.3,
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
                        value='200',
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
    
def showbasicwidgets():
    global countrynamewidget, simplifiedwidget
    display(countrynamewidget)
    display(simplifiedwidget)
    
def showadvancedwidgets():
    global precursorwidget, coordswidget, legendcolumnswidget, legendsortingwidget, zoomwidget, islandthreshwidget, popplaceswidget, bubbleopacitywidget
    display(precursorwidget)
    display(coordswidget)
    display(legendcolumnswidget)
    display(legendsortingwidget)
    display(zoomwidget)
    display(islandthreshwidget)
    display(popplaceswidget)
    display(bubbleopacitywidget)
    
    
def createplot():
    initial = ppm.CountryPowerPlantMapper(countryname = countrynamewidget.value, zoom = zoomwidget.value,
                 coords = coordswidget.value, legend_columns = legendcolumnswidget.value,
                 legend_sorting = legendsortingwidget.value, precursor = precursorwidget.value,
                 island_thresh = islandthreshwidget.value, additional_powerplants_csv = None,
                 populated_places = popplaceswidget.value, urban_areas = None,
                 bubble_opacity = bubbleopacitywidget.value, simplified = simplifiedwidget.value)
    initial.mapper()

def updateplot():
    from IPython.display import clear_output
    createplot()
    
    mapwidget = widgets.Button(
                    description='Update Plot',
                    disabled=False,
                    button_style='', # 'success', 'info', 'warning', 'danger' or ''
                    tooltip='Update Plot',
                    icon='check',
                    layout=widgets.Layout(width='70%', height='80px'))
    
    def on_button_clicked(b):
        clear_output()
        u = ppm.CountryPowerPlantMapper(countryname = countrynamewidget.value, zoom = zoomwidget.value,
                     coords = coordswidget.value, legend_columns = legendcolumnswidget.value,
                     legend_sorting = legendsortingwidget.value, precursor = precursorwidget.value,
                     island_thresh = islandthreshwidget.value, additional_powerplants_csv = None,
                     populated_places = popplaceswidget.value, urban_areas = None,
                     bubble_opacity = bubbleopacitywidget.value, simplified = simplifiedwidget.value)
        u.mapper()
        display(mapwidget)
        
    mapwidget.on_click(on_button_clicked)
    display(mapwidget)

def saveplot():
    display(pathwidget)
    display(dpiwidget)
    savewidget = widgets.Button(
                    description='Save Plot',
                    disabled=False,
                    button_style='', # 'success', 'info', 'warning', 'danger' or ''
                    tooltip='Save Plot',
                    icon='check',
                    layout=widgets.Layout(width='70%', height='80px'))
    def on_button_clicked(b):
        plt.savefig(pathwidget.value, dpi = dpiwidget.value)
    savewidget.on_click(on_button_clicked)
    display(savewidget)
    
    