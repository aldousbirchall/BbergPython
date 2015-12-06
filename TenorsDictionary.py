#Create dict (lookup table) for Bberg Tenors into number fo months


Tenors_Bbg = ['1M',
'2M',
'3M',
'6M',
'1Y',
'2Y',
'3Y',
'4Y',
'5Y',
'6Y',
'7Y',
'8Y',
'9Y',
'10Y',
'12Y',
'15Y',
'20Y',
'25Y',
'30Y',
'12M'
]
Tenors_Months = [1,
2,
3,
6,
12,
24,
36,
48,
60,
72,
84,
96,
108,
120,
144,
180,
240,
300,
360,
12
]

Tenors_dict = dict(zip(Tenors_Bbg, Tenors_Months))
