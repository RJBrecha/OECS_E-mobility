#!/usr/bin/env python
# coding: utf-8


import numpy as np
from scipy.ndimage import shift
import pandas as pd
from matplotlib import pyplot as plt

import streamlit as st

#from importlib.metadata import version
#version('numpy')


#Read in the data on starting vintages "years old, from 0-30", your survival rate function, initial distribution of vehicle vintages
df = pd.read_excel("US_LDV_stock_and_turnover.xlsx",sheet_name = ['Python_input_data'])
df.keys()
#vintage = np.array(df['Python_input_data'].Vintage)
vintage = np.linspace(0, 30, 31).astype(int)
survival = np.array(df['Python_input_data'].survival_rate)
scrappage = np.array(df['Python_input_data'].survival_rate_delta)
vehicle_distribution = np.array(df['Python_input_data'].initial_distribution)
EV_distribution = np.array(df['Python_input_data'].initial_EV_distribution)
#print("Total number of vehicles",vehicle_distribution.sum())
#plt.plot(vintage,vehicle_distribution)
#plt.xlabel('Years old', size=12)
#plt.ylabel('Stock of vehicles', size=12)

scen = 'SSP2'+'_pop'
df1 = pd.read_excel("US_LDV_stock_and_turnover.xlsx",sheet_name = ['SSP_pop_data'])
population_projected = np.array(df1['SSP_pop_data'].SSP2_pop)
year = np.array(df1['SSP_pop_data'].Year)
df2 = pd.DataFrame({'Years':year,'pop':population_projected})
df2 = df2.interpolate()
population_projected = df2['pop']
#df1.keys()
#vehicles_per_1000_people = df1['AB'].Vehicles_per_1000_people
#GDP_per_capita = df1['AB'].GDP_per_capita
vehicles_per_1000_people = np.linspace(750,800,31)

#df2 = pd.read_excel("US_LDV_stock_and_turnover.xlsx",sheet_name = ['Pop_scen_data'])
#df2.keys()
#GDP_per_capita_projected = (df2['AB_projected'].GDP_per_capita)*1000
#population_projected = (df2['Pop_scen_data'].scen)

projected_vehicle_stocks = vehicles_per_1000_people*population_projected/1000


#projected_vehicle_stocks.round(decimals=0)


# Interactive Streamlit elements, like these sliders, return their value.
# This gives you an extremely simple interaction model.
EV_sales_fraction_2030 = st.sidebar.slider("EV sales fraction in 2030", 0.0, 1.0, .1)
EV_sales_fraction_2040 = st.sidebar.slider("EV sales fraction in 2040", 0.0, 1.0, .15)
EV_sales_fraction_2050 = st.sidebar.slider("EV sales fraction in 2050", 0.0, 1.0, 0.2)
#EV_sales_fraction_2030 = 0.33
#EV_sales_fraction_2040 = 0.67
#EV_sales_fraction_2050 = 1.0
#sales_oldest_vintage=1

#def plot(EV_sales_fraction_2030,EV_sales_fraction_2040, EV_sales_fraction_2050, sales_oldest_vintage):
    #Define the function that represents the progression of sales of EVs over time; here it is a three-part function
    #with three input values for 2030, 2040 and 2050 taken from above (again, ideally with sliders)
sales1 = np.linspace(0.05,EV_sales_fraction_2030,10)
sales2 = np.linspace(EV_sales_fraction_2030+(EV_sales_fraction_2040-EV_sales_fraction_2030)/10,EV_sales_fraction_2040,10)
sales3 = np.linspace(EV_sales_fraction_2040+(EV_sales_fraction_2050-EV_sales_fraction_2040)/10,EV_sales_fraction_2050,10)
EV_sales_fraction = np.concatenate((sales1,sales2,sales3))
    #Define a vector of years for use later
years = np.linspace(2020, 2050, 31).astype(int)
    #Initialize the arrays (will be added to by concatenation later)
EV_sales=[0.2]
ICEV_sales=[16.2]
    #Define a loop variable to count through the years over which we are interested in running the program.
x = range(len(years)-1)
    #Assume above initial distributions for all vehicles; initialized the array of EV distribution with zeros
ICEV_distribution = vehicle_distribution - EV_distribution
#EV_distribution = [0]*len(vehicle_distribution)
EV_total = [EV_distribution.sum()]
ICEV_total = [ICEV_distribution.sum()]
for i in x:
        #Use the survival profile to "scrap" cars of different vintages with a given probability, both ICEVs and EVs
        ICEV_scrap_by_vintage = (ICEV_distribution*(scrappage))
        EV_scrap_by_vintage = (EV_distribution*(scrappage))
        
        #ICEV_scrap_by_vintage = (ICEV_distribution*(1-survival))
        #EV_scrap_by_vintage = (EV_distribution*(1-survival))
        
        #Here's what's left of each vintage after the scrapping is done each year
        ICEV_remaining_by_vintage = (ICEV_distribution - ICEV_scrap_by_vintage) 
        EV_remaining_by_vintage = (EV_distribution - EV_scrap_by_vintage) 
        
        #Total scrappage distribution by vintage
        scrap_by_vintage = ICEV_scrap_by_vintage + EV_scrap_by_vintage 
        scrap_by_vintage.sum() 
        ##Total sales is just equal to total scrappage plus change in expected stock
        
        vehicle_sales_total = projected_vehicle_stocks[i+1] - projected_vehicle_stocks[i] + scrap_by_vintage.sum()
            
            
        #Count the total sales for EVs and ICEVs each time through the loop
        EV_sales.append(((vehicle_sales_total*EV_sales_fraction[i])).sum()) 
        ICEV_sales.append(((vehicle_sales_total*(1-EV_sales_fraction[i]))).sum())
        
        #Assume a uniform distribution of sales over different vintages; this could be changed, but we don't have
        #particularly good reason to know how the vintage distribution of sold vehicles will look
        #sales_by_vintage = vehicle_sales_total/(sales_oldest_vintage)
        
        #Divide sales between EVs and ICEVs, and by vintage; 
        #Create an array of sales by vintage for EVs and ICEVs vehicle_sales_total/(sales_oldest_vintage+1)
        #EV_sales = (vehicle_sales_total*EV_sales_fraction[i]).round(decimals=0)
        #ICEV_sales = (vehicle_sales_total*(1-EV_sales_fraction[i])).round(decimals=0)
        #EV_sales_vintage_distribution = [EV_sales_by_vintage.round(decimals=0)]*(sales_oldest_vintage+1)+[0]*(len(vehicle_distribution)-(sales_oldest_vintage+1))
        #ICEV_sales_vintage_distribution = [ICEV_sales_by_vintage.round(decimals=0)]*(sales_oldest_vintage+1)+[0]*(len(vehicle_distribution)-(sales_oldest_vintage+1))
        
        # Create the new distribution array before going through the loop again
        # Now the cars that were 0 years old will be 1 year old, etc.  The zero-year-old cars in the stock for the next 
        #are that fraction of the sales that were of new cars
        EV_distribution = shift(EV_remaining_by_vintage, 1, cval=(vehicle_sales_total*EV_sales_fraction[i]).sum())
        ICEV_distribution = shift(ICEV_remaining_by_vintage, 1, cval=(vehicle_sales_total*(1-EV_sales_fraction[i])).sum())
        
        
        #Continue building the array of EV stock and ICEV stock; will be used for plotting as a function of time.
        EV_total.append(EV_distribution.sum())
        ICEV_total.append(ICEV_distribution.sum())
        #print(population_projected[i])
      
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.stackplot(years, [EV_total, ICEV_total]) 
ax.legend(labels = ('EV Stock', 'ICEV Stock'),loc=2)
ax.set_title("Vehicle stocks")
ax.set_xlabel('Year', size=12)
ax.set_ylabel('Stock of vehicles', size=12)
plt.show()
#chart_data = pd.DataFrame(years,[EV_total, ICEV_total])    
st.pyplot(fig)   
#st.area_chart(chart_data)
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
#st.button("Re-run")

fig2 = plt.figure()
ax = fig2.add_axes([0,0,1,1])
ax.stackplot(years, [EV_sales, ICEV_sales]) 
ax.legend(labels = ('EV sales', 'ICEV sales'),loc=2)
ax.set_title("Vehicle sales")
ax.set_xlabel('Year', size=12)
ax.set_ylabel('Sales of vehicles', size=12)
plt.show()




