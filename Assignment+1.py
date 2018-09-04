
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 1
# 
# In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data. 
# 
# Each line of the `dates.txt` file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.
# 
# The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates. 
# 
# Here is a list of some of the variants you might encounter in this dataset:
# * 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# * Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
# * 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# * Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# * Feb 2009; Sep 2009; Oct 2010
# * 6/2008; 12/2009
# * 2009; 2010
# 
# Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:
# * Assume all dates in xx/xx/xx format are mm/dd/yy
# * Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
# * If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
# * If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
# * Watch out for potential typos as this is a raw, real-life derived dataset.
# 
# With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.
# 
# For example if the original series was this:
# 
#     0    1999
#     1    2010
#     2    1978
#     3    2015
#     4    1985
# 
# Your function should return this:
# 
#     0    2
#     1    4
#     2    0
#     3    1
#     4    3
# 
# Your score will be calculated using [Kendall's tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient), a correlation measure for ordinal data.
# 
# *This function should return a Series of length 500 and dtype int.*

# In[2]:

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


# In[ ]:




# In[307]:




# In[308]:




# In[309]:




# In[310]:




# In[311]:




# In[ ]:




# In[ ]:




# In[312]:




# In[313]:




# In[314]:




# In[315]:




# In[316]:




# In[302]:




# In[318]:




# In[233]:




# In[234]:




# In[235]:




# In[236]:




# In[237]:




# In[238]:




# In[239]:




# In[240]:




# In[241]:




# In[242]:




# In[243]:




# In[ ]:



