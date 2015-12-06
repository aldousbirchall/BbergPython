##This uses 'tia' package bloomberg api wrapper and utils from https://github.com/bpsmith/tia
##Installed at C:\Python27\Lib\site-packages


##essential imports for simple daily data query
from tia.bbg import LocalTerminal
import pandas as pd
##Import dict to map bberg tenors to months
from TenorsDictionary import Tenors_dict

# Multiple SID, Invalid Fields
# allows for non-homogeneous security types to be batched together
#These tickers are hard coded from the "USD ISDA CDS Fixing SWAP CURVE"
#To get Tenors need to use bberg field "SECURITY_TENOR_ONE" on money market instruments and
#"SECURITY_TENOR_TWO" on swap instruments. So run two queries and append data frame
resp = LocalTerminal.get_reference_data(['USLFD1M  ISCF Curncy',
                                        'USLFD2M  ISCF Curncy',
                                        'USLFD3M  ISCF Curncy',
                                        'USLFD6M  ISCF Curncy',
                                        'USLFD12M  ISCF Curncy'],
                                        ['LAST_UPDATE_DT','SECURITY_TENOR_ONE',
                                        'SECURITY_TYP','PX_LAST'],
                                        ignore_field_error=1)
df=resp.as_frame()

#Rename Tenor column for consistency with Swap data fram before appending
df.rename(columns={'SECURITY_TENOR_ONE': 'Tenor'}, inplace=True)

resp = LocalTerminal.get_reference_data(['USSWAP2  Curncy',
                                        'USSWAP3  Curncy',
                                        'USSWAP4  Curncy',
                                        'USSWAP5  Curncy',
                                        'USSWAP6  Curncy',
                                        'USSWAP7  Curncy',
                                        'USSWAP8  Curncy',
                                        'USSWAP9  Curncy',
                                        'USSWAP10 Curncy',
                                        'USSWAP12 Curncy',
                                        'USSWAP15 Curncy',
                                        'USSWAP20 Curncy',
                                        'USSWAP25 Curncy',
                                        'USSWAP30 Curncy'],
                                        ['LAST_UPDATE_DT','SECURITY_TENOR_TWO',
                                        'SECURITY_TYP','PX_LAST'],
                                        ignore_field_error=1)

#Store swap market data in "MM_frame"
df2=resp.as_frame()
df2.rename(columns={'SECURITY_TENOR_TWO': 'Tenor'}, inplace=True)

#Append swaps to money market data
df = df.append(df2)

####################################
#Perform formatting for Strata tool#
####################################
#Tenors must be in ascending order


#Covert rates into decimals
df[['PX_LAST']] = df[['PX_LAST']]/100

#Replace 'DEPOSIT' with 'M' and 'SWAP' with 'S'
df = df.replace(['DEPOSIT','SWAP'],['M','S'])

#Rename columns
df.rename(columns={'LAST_UPDATE_DT': 'Valuation Date',
                    'SECURITY_TYP':'Instrument Type',
                   'PX_LAST':'Rate',}, inplace=True)

#Add column on right with curve convention
df['Curve Convention'] = 'ISDA_USD'

#Add temp column on right with tenor in months for sorting
df['Tenor_Months'] = df[['Tenor']] #Copy tenor column
df = df.replace({"Tenor_Months": Tenors_dict}) #Replace with dictionary values

#sort by Tenor_Months
df = df.sort_values('Tenor_Months', ascending=1)

#Remove Tenor_Months column (axis=1 for column)
df = df.drop('Tenor_Months', 1)

#To csv (remove index as this is bberg tickers)
#df.to_csv('C:\Program Files\StrataStack\Bberg_Python_out\USD_CDS_Yield_curve.csv', index = False)
#df.to_csv('C:\Program Files\StrataStack\bbg-marketdata\credit\2014-01-22\cds.yieldCurves.csv', index = False)
#df.to_csv('C:\Program Files\StrataStack\bbg_marketdata\credit\2014_01_22\cds_yieldCurves.csv', index = False)
df.to_csv(r'C:\Program Files\StrataStack\bbg_marketdata\credit\2014-01-22\cds.yieldCurves.csv', index = False)

