#Tia V3API tools - snippets.
#https://github.com/bpsmith/tia
#http://nbviewer.ipython.org/github/bpsmith/tia/blob/master/examples/v3api.ipynb

#Dependencies
from tia.bbg import LocalTerminal
import pandas as pd #Pandas needs numpy

#Example code from Tia snippets. Do not run this as module!!

###########################
##Reference Data Requests##
###########################

# Single SID, Multiple Valid Fields
resp = LocalTerminal.get_reference_data('MSFT US EQUITY', ['PX_LAST', 'GICS_SECTOR_NAME', 'VOLATILITY_30D'])
resp.as_frame()

# Get the response as a dict
resp.as_map()

# Single SID, Invalid Fields
# Ability to ignore errors
resp = LocalTerminal.get_reference_data('MSFT US EQUITY', ['PX_LAST', 'GICS_SECTOR_NAME', 'BAD FIELD'], ignore_field_error=1)
resp.as_frame()

# Multiple SID, Invalid Fields
# allows for non-homogeneous security types to be batched together
resp = LocalTerminal.get_reference_data(['ED1 COMDTY', 'MSFT US EQUITY'], ['PX_LAST', 'GICS_SECTOR_NAME'], ignore_field_error=1)
resp.as_frame()

# Retrieve data without override
LocalTerminal.get_reference_data('SPX INDEX', 'CUST_TRR_RETURN_HOLDING_PER').as_frame()

# Retrieve data with override (1 month total return)
dt = pd.datetools.BDay(-21).apply(pd.datetime.now()).strftime('%Y%m%d')
LocalTerminal.get_reference_data('SPX INDEX', 'CUST_TRR_RETURN_HOLDING_PER', CUST_TRR_START_DT=dt).as_frame()

###################
##Historical Data##
###################

# Single SID, Multiple Valid Fields
resp = LocalTerminal.get_historical('MSFT US EQUITY', ['PX_OPEN', 'PX_LAST'], start='1/1/2014', end='3/1/2014')
resp.as_frame().head()

# Multiple SIDs, Multiple Valid Fields
resp = LocalTerminal.get_historical(['IBM US EQUITY', 'MSFT US EQUITY'], ['PX_OPEN', 'PX_LAST'], start='1/1/2014', end='3/1/2014')
resp.as_frame().head()

# Weekly data
resp = LocalTerminal.get_historical(['IBM US EQUITY', 'MSFT US EQUITY'], ['PX_OPEN', 'PX_LAST'], 
                                         start='1/1/2014', end='3/1/2014', period='WEEKLY')
resp.as_frame().head()

# format response as panel
resp.as_panel()

#################################
##RETRIEVING CURVES AND MEMBERS##
#################################

# Retrieve the EURUSD Forward Curve
resp = LocalTerminal.get_reference_data('eurusd curncy', 'fwd_curve')
# must retrieve a frame from the first row
resp.as_frame().ix[0, 'fwd_curve'].head()

# OR 
resp.as_map()['eurusd curncy']['fwd_curve'].head()

# Retrive the EURUSD Vol Surface
resp = LocalTerminal.get_reference_data('eurusd curncy', 'dflt_vol_surf_bid')
resp.as_frame().ix[0, 'dflt_vol_surf_bid'].head()



# More complex example
# Retrive all members of the S&P 500, then get price and vol data
resp = LocalTerminal.get_reference_data('spx index', 'indx_members')
members = resp.as_frame().ix[0, 'indx_members']
# append region + yellow key = 'US EQUITY'
members = members.icol(0).apply(lambda x: x.split()[0] + ' US EQUITY')
resp = LocalTerminal.get_reference_data(members, ['PX_LAST', 'VOLATILITY_30D'])
resp.as_frame().head()

# kind of pointless
resp.as_frame().describe()

pxs = LocalTerminal.get_historical(members, 'PX_LAST')
f = pxs.as_frame()
f.columns = f.columns.get_level_values(0)
# Show first 5 rows for last 5 days
f.iloc[:5, -5:]

#########################
##Intraday Tick Request##
#########################
import datetime
sid = 'VOD LN EQUITY'
events = ['TRADE', 'AT_TRADE']
dt = pd.datetools.BDay(-1).apply(pd.datetime.now())
start = pd.datetime.combine(dt, datetime.time(13, 30))
end = pd.datetime.combine(dt, datetime.time(13, 35))
f = LocalTerminal.get_intraday_tick(sid, events, start, end, include_condition_codes=True).as_frame()
f.head()

########################
##Intraday Bar Request##
########################
import datetime
sid = 'IBM US EQUITY'
event = 'TRADE'
dt = pd.datetools.BDay(-1).apply(pd.datetime.now())
start = pd.datetime.combine(dt, datetime.time(13, 30))
end = pd.datetime.combine(dt, datetime.time(21, 30))
f = LocalTerminal.get_intraday_bar(sid, event, start, end, interval=60).as_frame()
f.head()

