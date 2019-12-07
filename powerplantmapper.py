#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 19:59:24 2018

@author: skoebric
""" 
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import country_converter as coco
from shapely.geometry import Point, Polygon, MultiPolygon
import os

    
class CountryPowerPlantMapper(object):

    def __init__(self, countryname, zoom = 1,
                 coords = 'spherical', legend_columns = 1,
                 legend_sorting = 'capacity', precursor = '',
                 island_thresh = 200, additional_powerplants_csv = None,
                 populated_places = False, urban_areas = None,
                 bubble_opacity = 0.5, simplified = 'Mixed',
                 title = True, source = True, disputed = True):
    
        self.countryname = countryname
        self.zoom = zoom
        self.precursor = precursor
        self.coords = coords
        self.additional_powerplants_csv = additional_powerplants_csv
        self.legend_sorting = legend_sorting
        self.legend_columns = legend_columns
        self.countryiso3 = coco.convert(names=self.countryname, to='ISO3', not_found=None)
        self.island_thresh = island_thresh
        self.populated_places = populated_places
        self.urban_areas = urban_areas
        self.bubble_opacity = bubble_opacity
        self.simplified = simplified
        self.title = title
        self.source = source
        self.disputed = disputed
        
        if coords == 'spherical':
            self.crsid = {'init':'epsg:3857'}
        elif coords == 'geo':
            self.crsid = {'init':'epsg:4326'}
        else:
            self.crsid = {'init':f'epsg:{coords}'}
        
        worldshapefiles = os.path.join('geometry','world10m.geojson')
        worldshapes = gpd.read_file(worldshapefiles)
        worldshapes = worldshapes.to_crs(self.crsid)
        countryshape = worldshapes.loc[worldshapes['ADM0_A3_US'] == self.countryiso3]

        if self.disputed:
            disputedshapefile = os.path.join('geometry','ne_10m_admin_0_disputed_areas','ne_10m_admin_0_disputed_areas.shp')
            disputedshapes = gpd.read_file(disputedshapefile)
            disputedshapes = disputedshapes.to_crs(self.crsid)

            # --- Search 'NOTE_BRK' column for mapped country ---
            disputedshapes['INCLUDE'] = [self.countryname.upper() in str(i).upper() for i in list(disputedshapes['NOTE_BRK'])]
            countrydisputed = disputedshapes.loc[disputedshapes['INCLUDE'] == True]

            # --- Concat and dissolve ---
            countryshape = pd.concat([countryshape, countrydisputed], axis='rows')
            countryshape['ADM0_A3_US'] = self.countryiso3
            countryshape = countryshape.dissolve(by='ADM0_A3_US', aggfunc='sum', as_index=False)

        if len(countryshape) > 1:
            countryshape = countryshape.sort_values('POP_EST', ascending = False)
            countryshape = countryshape[0:1]
        self.countryshape = countryshape
        
        if self.populated_places == 'False':
            self.populated_places = False
        elif self.populated_places == 'True':
            self.populated_places = True
        else:
            self.populated_places = int(self.populated_places)
        
        if self.island_thresh == 'False':
            self.island_thresh = False
        elif self.island_thresh == 'largest':
            self.island_thresh = 'largest'
        else:
            self.island_thresh = int(self.island_thresh)
        
        if self.island_thresh != False:
            if type(self.countryshape['geometry'].item()) == MultiPolygon: 
                countryshape_index = self.countryshape.index[0]
                if type(self.island_thresh) == int:
                    multiout = MultiPolygon([P for P in self.countryshape['geometry'].item() if P.area > (self.island_thresh * 1000000)])
                elif self.island_thresh == 'largest':
                    largestarea = max([P.area for P in self.countryshape['geometry'].item()])
                    multiout = MultiPolygon([P for P in self.countryshape['geometry'].item() if P.area == largestarea])
                self.countryshape.at[countryshape_index,'geometry'] = multiout            

        ppdb = pd.read_csv(os.path.join('geometry','global_power_plant_database.csv'))
        ppdb = ppdb.loc[(ppdb['latitude'] > -90) & (ppdb['latitude'] < 90)]
        ppdb = ppdb.loc[(ppdb['longitude'] > -180) & (ppdb['longitude'] < 180)]
    
        #Pass a csv file with additional power plants to add columns must be 'country_long' (country name), 'name' (plant name), 'capacity_mw', 'latitude', 'longitude', 'primary_fuel'. 'estimated_generation_gwh' can also be passed. 
        if self.additional_powerplants_csv != None:
            adddb = pd.read_csv(additional_powerplants_csv)
            ppdb = pd.concat([ppdb, adddb])
        
        countryppdb = ppdb.loc[ppdb['country'] == self.countryiso3]
    
        def columnstotuplemaker(row):
            lat = row['latitude']
            long = row['longitude']
            return (long, lat)
    
        try:
            countryppdb['Decimal Coordinates'] = countryppdb.apply(columnstotuplemaker, axis = 1)
        except ValueError:
            print('there likely are no recorded power plants in this country')
            return None
    
        countryppdb['geometry'] = countryppdb['Decimal Coordinates'].apply(Point)
        countryppgdf = gpd.GeoDataFrame(countryppdb, geometry = 'geometry')
        countryppgdf.crs = {'init':'epsg:4326'}
        countryppgdf = countryppgdf.to_crs(self.crsid)
        countryppgdf['primary_fuel'] = countryppgdf['primary_fuel'].replace('Petcoke','Oil')
        
        def capacitynormalizer(row):
            MWin = row['capacity_mw']
            if MWin <= 10:
                MWout = 4
            elif MWin <= 100:
                MWout = 18
            elif MWin <= 1000:
                MWout = 75
            elif MWin >= 1000:
                MWout = 150
            return MWout

        countryppgdf['norm_cap'] = countryppgdf.apply(capacitynormalizer, axis = 1)
        
        def pointinpolygonchecker(row):
            geom = row['geometry']
            return self.countryshape.geometry.contains(geom)
        
        def polycrosseschecker(row):
            geom = row['geometry']
            inter = self.countryshape.geometry.intersects(geom)
            cont =  self.countryshape.geometry.contains(geom)
            if inter.item() == True or cont.item() == True:
                return True
            else:
                return False
        
        if island_thresh != False:
            countryppgdf['in_polygon'] = countryppgdf.apply(pointinpolygonchecker, axis = 1)
            countryppgdf = countryppgdf.loc[countryppgdf['in_polygon'] == True]
            
        self.countryppgdf = countryppgdf[['name','geometry','norm_cap','primary_fuel','capacity_mw']]
        if self.populated_places != False:
            popplaces = gpd.read_file(os.path.join('geometry','ne_50m_populated_places_simple','ne_50m_populated_places_simple.shp'))
            popplaces.crs = {'init':'epsg:4326'}
            popplaces = popplaces.to_crs(self.crsid)
            popplaces['in_polygon'] = popplaces.apply(pointinpolygonchecker, axis = 1)
            popplaces = popplaces.loc[popplaces['in_polygon'] == True]
            if self.populated_places == False:
                self.populated_places == False
            elif self.populated_places == True:
                self.popplaces = popplaces[['nameascii','pop_max','geometry']]
            else:
                popplaces = popplaces.loc[popplaces['pop_max'] > int(self.populated_places)]
                self.popplaces = popplaces[['nameascii','pop_max','geometry']]
        
        if self.urban_areas == True:
            urbanareas = gpd.read_file(os.path.join('geometry','ne_50m_urban_areas','ne_50m_urban_areas.shp'))
            urbanareas.crs = {'init':'epsg:4326'}
            urbanareas = urbanareas.to_crs(self.crsid)
            urbanareas['in_polygon'] = urbanareas.apply(polycrosseschecker, axis = 1)
            urbanareas = urbanareas.loc[urbanareas['in_polygon'] == True]
            self.urbanareas = urbanareas[['geometry','area_sqkm']]
            
        if self.simplified == 'Simple':
            otherdic = {'Coal':'Fossil',
                        'Cogeneration':'Other',
                        'Gas':'Fossil',
                        'Oil':'Fossil',
                        'Hydro':'Renewable',
                        'Biomass':'Renewable',
                        'Geothermal':'Renewable',
                        'Solar':'Renewable',
                        'Wind':'Renewable',
                        'Nuclear':'Nuclear',
                        'Other':'Other',
                        'Waste':'Other',
                        'Wave and Tidal':'Renewable',
                        'Storage':'Other'}
        elif self.simplified == 'Mixed':
            otherdic = {'Coal':'Fossil',
                        'Cogeneration':'Other',
                        'Gas':'Fossil',
                        'Oil':'Fossil',
                        'Hydro':'Hydro',
                        'Biomass':'Biomass',
                        'Geothermal':'Geothermal',
                        'Solar':'Solar',
                        'Wind':'Wind',
                        'Nuclear':'Nuclear',
                        'Other':'Other',
                        'Waste':'Other',
                        'Wave and Tidal':'Wave and Tidal',
                        'Storage':'Storage'}
        elif self.simplified == 'Complex':
            otherdic = {'Coal':'Coal',
                        'Cogeneration':'Cogeneration',
                        'Gas':'Gas',
                        'Oil':'Oil',
                        'Hydro':'Hydro',
                        'Biomass':'Biomass',
                        'Geothermal':'Geothermal',
                        'Solar':'Solar',
                        'Wind':'Wind',
                        'Nuclear':'Nuclear',
                        'Other':'Other',
                        'Waste':'Waste',
                        'Wave and Tidal':'Wave and Tidal',
                        'Storage':'Storage'}
        
        def verboseapplier(row):
            resourcein = row['primary_fuel']
            resourceout = otherdic[resourcein]
            return resourceout
        
        self.countryppgdf['primary_fuel'] = self.countryppgdf.apply(verboseapplier, axis = 1)
        self.countryppgdf = self.countryppgdf.loc[self.countryppgdf['primary_fuel'] != 'Other']
            
        cmapall = {'Coal':'#000000',
                   'Cogeneration':'#ffd8b1',
                    'Gas':'#9A6324',
                    'Oil':'#800000',
                    'Hydro':'#4363d8',
                    'Biomass':'#f58231',
                    'Geothermal':'#e6194B',
                    'Solar':'#ffde02',
                    'Wind':'#469990',
                    'Nuclear':'#f032e6',
                    'Waste':'#ffd8b1',
                    'Wave and Tidal': '#42d4f4',
                    'Storage':'#fabebe',
                    'Renewable':'#f58231',
                    'Fossil':'#000000'}
        
        smap = {'Less than 10MW':2,
                '10MW - 100MW':4,
                '100MW - 1000MW':7,
                'More than 1000MW':11}
      

        cmapalldf = pd.DataFrame.from_dict(cmapall, orient = 'index').reset_index()
        cmapalldf.columns = ['resource','color']
        resourcesset = set(self.countryppgdf['primary_fuel'])
        self.cmapcountrydf = cmapalldf.loc[cmapalldf['resource'].isin(resourcesset)]
    
    def mapper(self):
        import seaborn as sns
        sns.set_style("white")
        fig, ax = plt.subplots(dpi = 120)
        self.countryshape.plot(alpha = 1, facecolor = 'white', edgecolor = 'k', linewidth = 1, ax = ax)
        self.countryshape.plot(alpha = 0.05, facecolor = 'green', ax = ax)
        
        if self.urban_areas != None:
            self.urbanareas.plot(alpha = 0.3, facecolor = 'green', ax = ax)
        
        capacity_order_list = list(self.countryppgdf.groupby('primary_fuel')['capacity_mw'].sum().sort_values(ascending = False).index)
    
        for ctype, data in self.countryppgdf.sort_values('primary_fuel', ascending = True).groupby('primary_fuel'):
            data.plot(color=self.cmapcountrydf.loc[self.cmapcountrydf['resource'] == ctype]['color'], 
                      label = ctype,
                      ax = ax, 
                      markersize = 'norm_cap',
                      alpha = self.bubble_opacity)
        
        if self.legend_sorting == 'alphabetical':
            self.cmapcountrydf.sort_values('resource', ascending = True, inplace = True)
        if self.legend_sorting == 'capacity':
            self.cmapcountrydf.set_index('resource', inplace = True)
            self.cmapcountrydf = self.cmapcountrydf.loc[capacity_order_list]
            self.cmapcountrydf.reset_index(inplace = True)
            
        if self.populated_places != False:
            xs = [i for i in self.popplaces.geometry.x]
            ys = [i for i in self.popplaces.geometry.y]
            ns = [i for i in self.popplaces['nameascii']]
    
            for x, y, n in zip(xs,ys,ns):
                ax.annotate(s = n, xy = (x,y), xytext = (x - (x/40), y),
                            fontsize = 7,
                            arrowprops=dict(arrowstyle="->", color = 'black'))     
        
        if self.title == True:
            plt.xlabel('Data from WRI Global Power Plant Database. 2018.\nGraphic by NREL.', fontsize = 8)
        elif self.title == False:
            plt.xlabel('   ',fontsize = 8)
            
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        colormarklist = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in list(self.cmapcountrydf['color'])]
        colormarklabels = list(self.cmapcountrydf.resource)
    
        mark1 = plt.Line2D([0,0],[0,0], color="white", marker='o',markersize=2, markerfacecolor="white", markeredgecolor = 'black')
        mark10 = plt.Line2D([0,0],[0,0], color="white", marker='o',markersize=4, markerfacecolor="white", markeredgecolor = 'black')
        mark100 = plt.Line2D([0,0],[0,0], color="white", marker='o',markersize=7, markerfacecolor="white", markeredgecolor = 'black')
        mark1000 = plt.Line2D([0,0],[0,0], color="white", marker='o',markersize=11, markerfacecolor="white", markeredgecolor = 'black')
        marklist = [mark1,mark10,mark100,mark1000]
        marklabellist = ['Less than 10MW','10MW - 100MW','100MW - 1000MW','More than 1000MW']
    
        allmark = colormarklist + marklist
        allmarklabel = colormarklabels + marklabellist
    
        plt.legend(allmark,
                   allmarklabel,
                   framealpha = 0.9,
                   numpoints=1, loc='best', fontsize = 7,
                   ncol = self.legend_columns).set_draggable(True)

        if self.title == True:
            plt.title(f'Power Plants in {self.precursor}{self.countryname}')
        
        wzoom = self.zoom
        hzoom = self.zoom
        w, h = fig.get_size_inches()
        fig.set_size_inches(w * wzoom, h * hzoom)
        plt.tight_layout()