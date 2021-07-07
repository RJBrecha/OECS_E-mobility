#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import matplotlib.pyplot as plt
from ipywidgets import FloatSlider
from ipywidgets import IntSlider
from ipywidgets import interact
import ipywidgets as widgets
from ipywidgets import HBox, Label
import streamlit as st

cost_per_kW= st.sidebar.slider("Cost per kW [US$]",500, 2000,1000)
interest_rate=st.sidebar.slider("Interest rate [%]",1, 10, 5)
loan_term= st.sidebar.slider("PV Loan term [years]",5, 30, 10)
electric_cost = st.sidebar.slider("Electricity cost [US$/kWh]", 0.1, 0.5, 0.35)
system_size = st.sidebar.slider('System size [kW]', 1.0,10.0,3.0)
efficiency = st.sidebar.slider('Efficiency [kWh/kW$_p$/year]',1000, 2000, 1500)
yearly_residential_electricity_consumption = st.sidebar.slider('Residential Electricity consumption [kWh/year]', 1000, 10000, 2500)


#def pv(cost_per_kW, interest_rate, loan_term, electric_cost, system_size, efficiency,yearly_residential_electricity_consumption):
interest_rate = interest_rate/100
discount_rate = 0.1
PV_yearly_payment = (cost_per_kW * system_size * interest_rate)/(1-(1+interest_rate)**(-loan_term))
PV_monthly_payment = PV_yearly_payment/12
total_payment = PV_yearly_payment*loan_term
value_of_electricity_per_year = system_size * efficiency * electric_cost
system_lifetime = 25
value_of_electricity_lifetime = value_of_electricity_per_year * ((1+discount_rate)**system_lifetime - 1)/(discount_rate * (1+ discount_rate) ** system_lifetime)
p_a = ((1+discount_rate) ** system_lifetime -1)/(discount_rate * (1+discount_rate) ** system_lifetime)
cost_of_system = cost_per_kW * system_size + (1/p_a)
yearly_electricity_generated = system_size * efficiency 



ICEV_cost = st.sidebar.slider('ICEV cost', 10000, 50000, 20000 )
ICEV_downpayment = st.sidebar.slider('ICEV downpayment', 1000, 20000,5000)
ICEV_loan_interest_rate = st.sidebar.slider('ICEV Loan Interest Rate, %',1, 10,5)
ICEV_loan_term = st.sidebar.slider('ICEV Loan Term (in years)', 3, 6, 4 )
EV_cost = st.sidebar.slider('ÊV cost', 10000, 50000, 30000)
EV_downpayment = st.sidebar.slider('EV downpayment', 1000, 20000, 7000)
EV_loan_interest_rate = st.sidebar.slider('EV Loan Interest Rate, %', 1, 10,5)
EV_loan_term = st.sidebar.slider('EV Loan Term (in years)', 1, 6, 4)
#electric_cost = st.sidebar.slider('Electricity cost, US$/kWh', 0.1, 0.5, 0.05)
                  


#def EV(ICEV_cost,ICEV_downpayment, ICEV_loan_interest_rate, ICEV_loan_term, EV_cost,EV_downpayment, EV_loan_interest_rate,EV_loan_term, electric_cost):
ICEV_loan_interest_rate = ICEV_loan_interest_rate/100
EV_loan_interest_rate = EV_loan_interest_rate/100
ICEV_efficiency = 8
EV_efficiency = 6
gasoline_cost = 1.00
monthly_km_driven = 1000
#Maintenance cost per mile
ICEV_maintenance = 0.10
EV_maintenance = 0.06
monthly_electricity_EV = monthly_km_driven/EV_efficiency 
monthly_gasoline_ICEV = monthly_km_driven * ICEV_efficiency/100 
monthly_EV_payments = ((EV_cost - EV_downpayment)* EV_loan_interest_rate/(1-(1+EV_loan_interest_rate)**(-EV_loan_term)))/12
yearly_EV_payments = monthly_EV_payments * 12
monthly_ICEV_payments = ((ICEV_cost - ICEV_downpayment)*ICEV_loan_interest_rate/(1-(1+ICEV_loan_interest_rate)**(-ICEV_loan_term)))/12
yearly_ICEV_payments = monthly_ICEV_payments*12
monthly_cost_EV_fuel = electric_cost * monthly_electricity_EV
monthly_cost_ICEV_fuel = monthly_gasoline_ICEV * gasoline_cost
monthly_cost_ICEV_maintenance = monthly_km_driven * ICEV_maintenance/1.61
monthly_cost_EV_maintenance = monthly_km_driven * EV_maintenance/1.61
yearly_home_elec_cost = yearly_residential_electricity_consumption*electric_cost
yearly_ICEV_cost_with_loan = yearly_ICEV_payments + monthly_cost_ICEV_fuel*12 + monthly_cost_ICEV_maintenance*12
yearly_ICEV_cost_without_loan = monthly_cost_ICEV_fuel*12 + monthly_cost_ICEV_maintenance*12
yearly_EV_cost_with_loan = yearly_EV_payments + monthly_cost_EV_fuel*12 + monthly_cost_EV_maintenance*12
yearly_EV_cost_without_loan = monthly_cost_EV_fuel*12 + monthly_cost_EV_maintenance*12
yearly_home_elec_cost_with_PV = (yearly_residential_electricity_consumption + monthly_electricity_EV*12 - yearly_electricity_generated)*electric_cost
 

"Summary - Yearly costs for ICEV + home electricity"  

ICEV_plus_home_elec = []
EV_plus_PV_plus_home_elec = []
EV_pmt = []
ICEV_pmt = []
EV_maint = []
ICEV_maint = []
EV_fuel = []
ICEV_fuel = []
Home_elec_no_PV = []
Home_elec_with_PV = []
PV_pmt = []



years = range(1,25,1)

#years

for i in years:
    if i <= ICEV_loan_term:
        ICEV_plus_home_elec.append(yearly_home_elec_cost + yearly_ICEV_cost_with_loan)
        ICEV_pmt.append(yearly_ICEV_payments)
        ICEV_maint.append(monthly_cost_ICEV_maintenance*12)
        ICEV_fuel.append(monthly_cost_ICEV_fuel*12)
        Home_elec_no_PV.append(yearly_home_elec_cost)
    else:
        ICEV_plus_home_elec.append(yearly_home_elec_cost + yearly_ICEV_cost_without_loan)
        ICEV_pmt.append(0)
        ICEV_maint.append(monthly_cost_ICEV_maintenance*12)
        ICEV_fuel.append(monthly_cost_ICEV_fuel*12)
        Home_elec_no_PV.append(yearly_home_elec_cost)
        
#ICEV_plus_home_elec

for i in years:
    if i <= EV_loan_term:
        EV_plus_PV_plus_home_elec.append(yearly_home_elec_cost_with_PV + PV_yearly_payment + yearly_EV_cost_with_loan)
        EV_pmt.append(yearly_EV_payments)
        EV_maint.append(monthly_cost_EV_maintenance*12)
        EV_fuel.append(monthly_cost_EV_fuel*12)
        Home_elec_with_PV.append(yearly_home_elec_cost_with_PV)
        PV_pmt.append(PV_yearly_payment)
    else:
        EV_plus_PV_plus_home_elec.append(yearly_home_elec_cost_with_PV + PV_yearly_payment + yearly_EV_cost_without_loan)
        EV_pmt.append(0)
        EV_maint.append(monthly_cost_EV_maintenance*12)
        EV_fuel.append(monthly_cost_EV_fuel*12)
        Home_elec_with_PV.append(yearly_home_elec_cost_with_PV)
        PV_pmt.append(PV_yearly_payment)
#EV_plus_PV_plus_home_elec
if yearly_electricity_generated > yearly_residential_electricity_consumption + monthly_electricity_EV*12:
    "Warning: PV system size too large for your electricity needs.  Choose a smaller capacity"

#width =0.3
#plt.bar(years, ICEV_plus_home_elec, width=width)
#plt.bar(years + width, EV_plus_PV_plus_home_elec, width=width)
X = np.arange(24)
offset = 0.3

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(X - offset/2, Home_elec_no_PV, color = 'red', width = offset)
ax.bar(X - offset/2, ICEV_pmt, color = 'orange', bottom = Home_elec_no_PV, width = offset)
ax.bar(X - offset/2, ICEV_maint, color = 'green', bottom = [sum(i) for i in zip(Home_elec_no_PV, ICEV_pmt)], width = offset)
ax.bar(X - offset/2, ICEV_fuel, color = 'blue', bottom = [sum(i) for i in zip(Home_elec_no_PV, ICEV_pmt, ICEV_maint)], width = offset)
ax.bar(X + offset/2, Home_elec_with_PV, color = 'maroon', width = offset)
ax.bar(X + offset/2, PV_pmt, color = 'magenta', bottom = Home_elec_with_PV, width = offset)
ax.bar(X + offset/2, EV_pmt, color = 'gold', bottom = [sum(i) for i in zip(Home_elec_with_PV, PV_pmt)],width = offset)
ax.bar(X + offset/2, EV_maint, color = 'lime', bottom = [sum(i) for i in zip(Home_elec_with_PV, PV_pmt, EV_pmt)], width = offset)
ax.bar(X + offset/2, EV_fuel, color = 'aqua', bottom = [sum(i) for i in zip(Home_elec_with_PV, PV_pmt, EV_pmt, EV_maint)],width = offset)
ax.legend(labels = ('Home elec', 'ICEV pmt', 'ICEV maint', 'ICEV fuel','Home elec (PV)','PV pmt', 'EV pmt', 'EV maint', 'EV fuel'),loc=1)
ax.set_title("Transport and Household")
ax.set_xlabel('Year', size=12)
ax.set_ylabel('Yearly cost [USD/year]', size=12)
#chart_data = pd.DataFrame(years,[EV_total, ICEV_total])    
st.pyplot(fig)   


"Electricity consumed(kWh/year)         :  ", yearly_residential_electricity_consumption
"Lifetime of the system                 :  ", system_lifetime
"Yearly payment($)                      :  ", PV_yearly_payment
"Monthly payment($)                     :  ", PV_monthly_payment
"Total payment($)                       :  ", total_payment
"Value of electricity (per year)        :  ", value_of_electricity_per_year
"Cost of system ($)                     :  ", cost_of_system
"Electricity generated (kWh/year)       :  ", yearly_electricity_generated

"Upfront Cost of ICEV                   :  $", ICEV_cost
"Downpayment for the ICEV               :  $", ICEV_downpayment
"Monthly loan payment for ICEV loan     :  $", monthly_ICEV_payments
"Yearly loan payment for ICEV loan      :  $", yearly_ICEV_payments 
"Monthly ICEV cost (gasoline cost)      :  $", monthly_cost_ICEV_fuel 
"Upfront Cost of EV                     :  $", EV_cost
"Downpayment for the EV                 :  $", EV_downpayment
"Monthly loan payment for EV loan       :  $", monthly_EV_payments
"Yearly loan payment for EV loan        :  $", yearly_EV_payments 
"Monthly EV cost (electricity cost)     :  $", monthly_cost_EV_fuel




