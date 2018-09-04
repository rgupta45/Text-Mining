# Text-Mining
Messy medical data text-mine


import pandas as pd

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
df.head(10)


# In[1]:

def date_sorter():
    #variant 1
    ex_1_1 =df.str.extractall(r'(?P<Month>\d{1,2})[/-](?P<Day>\d{1,2})[/-](?P<Year>\d{2})\b')
    ex_1_2 =df.str.extractall(r'(?P<Month>\d{1,2})[/-](?P<Day>\d{1,2})[/-](?P<Year>\d{4})\b')
    ex_1 = pd.concat([ex_1_1,ex_1_2])
    ex_1.reset_index(inplace=True)
    ex_1_pointer = ex_1['level_0']
    #Variant 2
    ex_2 = df.str.extractall(r'(?P<Month>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)[-.]* (?P<Day>\d{1,2})[, -]*(?P<Year>\d{4})')
    ex_2.reset_index(inplace=True)
    ex_2_pointer = ex_2['level_0']
    #Variant 3 & 5
    ex_3_5= df.str.extractall(r'(?P<Day>\d{1,2} )?(?P<Month>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)[. ,]*(?P<Year>\d{4})')
    ex_3_5.reset_index(inplace=True)
    ex_3_5_pointer = ex_3_5['level_0']
    #variant 6
    import numpy as np
    ex_6 = df.str.extractall(r'(?P<Month>\d{1,2})[/](?P<Year>\d{4})')
    ex_6.reset_index(inplace=True)
    ex_6_pointer = ex_6['level_0']
    temp=[]
    for i in ex_6_pointer:
        if not(i in ex_1_pointer.values):
            temp.append(i)
    temp= np.asarray(temp)
    ex_6=ex_6[ex_6['level_0'].isin(temp)]
    #variant 7
    part_1= df.str.extractall(r'[a-z]?\D(?P<Year>\d{4})\D')
    part_2= df.str.extractall(r'^(?P<Year>\d{4})\D')
    ex_7= pd.concat([part_1,part_2])
    ex_7.reset_index(inplace=True)
    ex_7_pointer = ex_7['level_0']
    temp=[]
    for i in ex_7_pointer:
        if not((i in ex_2_pointer.values) |(i in ex_3_5_pointer.values)|(i in ex_6_pointer.values)):
            temp.append(i)
    temp= np.asarray(temp)
    ex_7=ex_7[ex_7['level_0'].isin(temp)]
    cols = ex_3_5.columns.tolist()
    cols =cols[:2]+ cols[3:4] + cols[2:3] +cols[4:]
    ex_3_5= ex_3_5[cols]
    ex_3_5['Day']=ex_3_5['Day'].fillna(1)
    ex_6['Day']=1
    cols = ex_6.columns.tolist()
    cols =cols[:3]+cols[4:]+cols[3:4]
    ex_6= ex_6[cols]
    ex_7['Day']=1
    ex_7['Month']=1
    cols = ex_7.columns.tolist()
    cols=cols[:2]+cols[4:]+cols[3:4]+cols[2:3]
    ex_7=ex_7[cols]
    join = [ex_1,ex_2,ex_3_5,ex_6,ex_7]
    prac_1=pd.concat(join)
    prac_1.sort_values(by=['level_0'],ascending=True,inplace=True)
    prac_1.set_index('level_0',inplace=True)
    prac_1.drop('match',axis=1,inplace=True)
    prac_1['Year']=prac_1['Year'].apply(lambda x: str(x))
    prac_1['Year']=prac_1['Year'].apply(lambda x: '19'+x if(len(x)==2) else x)
    prac_1['Month']=prac_1['Month'].apply(lambda x: str(x))
    prac_1['Day']=prac_1['Day'].apply(lambda x: str(x))
    prac_1['Month']=prac_1['Month'].apply(lambda x: x[0:3] if len(x)>2 else x)
    prac_1['Month']=prac_1['Month'].apply(lambda x: '0'+x if len(x)<2 else x)
    prac_1['Day']=prac_1['Day'].apply(lambda x: '0'+x if len(x)<2 else x)
    prac_1['Month'][251:]
    month_dict = dict({'Jan': 1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12})
    prac_1.replace({"Month": month_dict},inplace=True)
    prac_1['Month']=prac_1['Month'].apply(lambda x: str(x))
    prac_1['Month']=prac_1['Month'].apply(lambda x: '0'+x if len(x)<2 else x)
    prac_1['Date'] = prac_1['Month']+'/'+prac_1['Day']+'/'+prac_1['Year']
    prac_1['Date']=pd.to_datetime(prac_1['Date'])
    abc= prac_1.sort_values(by='Date')
    abc['Value']= np.arange(500)
    abc.drop(['Month','Day','Year'],axis=1,inplace=True)
   # result= pd.concat([prac_1, abc], axis=1, join='inner',keys='Date')
    #ans = pd.Series(result['a']['Value'])
    Full_Date = prac_1['Date']
    x = []
    for i in sorted(enumerate(Full_Date), key=lambda x: x[1]):
        x.append(i[0])

    ans=pd.Series(x)
    return (ans)

