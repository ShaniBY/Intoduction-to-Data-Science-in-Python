
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# In[2]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    with open('university_towns.txt') as file: 
        data= []
        for line in file:
            data.append(line[:-1])
    state_town=[]    
    for place in data: 
        if place[-6:]=='[edit]':
            state=place[:-6]
        elif '(' in place:
            town = place[:place.index('(')-1]
            state_town.append([state,town])
        else: 
            town=place
            state_town.append([state,town])
    
    x=['State','RegionName']
    UniTowns_list = pd.DataFrame(state_town,columns = x)

        
        
    return UniTowns_list

get_list_of_university_towns()


# In[3]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    GDP=pd.read_excel('gdplev.xls',skiprows=5)
    GDP=GDP.drop(['GDP in billions of current dollars', 'GDP in billions of chained 2009 dollars','Unnamed: 3', 'Unnamed: 7'], axis=1)
    GDP=GDP.rename(columns={'Unnamed: 0': 'Year', 'Unnamed: 4':'Quarter','GDP in billions of current dollars.1':'GDP in billions of current dollars','GDP in billions of chained 2009 dollars.1':'GDP in billions of chained 2009 dollars'})
    GDP=GDP.drop(GDP.index[0:214]).reset_index(drop=True)
    #Need to see 2 Q down followed by 2 Q up and return first Q of resession from Quarter column 
    recessionSQ=[]

    for ind in range(0, len(GDP) - 2): 
        if (GDP['GDP in billions of chained 2009 dollars'][ind]>GDP['GDP in billions of chained 2009 dollars'][ind+1]) & (GDP['GDP in billions of chained 2009 dollars'][ind+1]>GDP['GDP in billions of chained 2009 dollars'][ind+2]):
            recessionSQ.append(GDP['Quarter'][ind+1])
    return recessionSQ[0]


get_recession_start()


# In[4]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    GDP=pd.read_excel('gdplev.xls',skiprows=5)
    GDP=GDP.drop(['GDP in billions of current dollars', 'GDP in billions of chained 2009 dollars','Unnamed: 3', 'Unnamed: 7'], axis=1)
    GDP=GDP.rename(columns={'Unnamed: 0': 'Year', 'Unnamed: 4':'Quarter','GDP in billions of current dollars.1':'GDP in billions of current dollars','GDP in billions of chained 2009 dollars.1':'GDP in billions of chained 2009 dollars'})
    GDP=GDP.drop(GDP.index[0:214]).reset_index(drop=True)
    start=get_recession_start()
    start_ind=np.asscalar(GDP[GDP['Quarter']==start].index.values)
    recessionEQ=[]
    
    for ind in range((start_ind+2),(len(GDP) - 2)):
        if (GDP['GDP in billions of chained 2009 dollars'][ind]<GDP['GDP in billions of chained 2009 dollars'][ind+1]) & (GDP['GDP in billions of chained 2009 dollars'][ind+1]<GDP['GDP in billions of chained 2009 dollars'][ind+2]):
            recessionEQ.append(GDP['Quarter'][ind+2])
    
    return recessionEQ[0]

get_recession_end()


# In[5]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    GDP=pd.read_excel('gdplev.xls',skiprows=5)
    GDP=GDP.drop(['GDP in billions of current dollars', 'GDP in billions of chained 2009 dollars','Unnamed: 3', 'Unnamed: 7'], axis=1)
    GDP=GDP.rename(columns={'Unnamed: 0': 'Year', 'Unnamed: 4':'Quarter','GDP in billions of current dollars.1':'GDP in billions of current dollars','GDP in billions of chained 2009 dollars.1':'GDP in billions of chained 2009 dollars'})
    GDP=GDP.drop(GDP.index[0:214]).reset_index(drop=True)
    start= get_recession_start()
    stop=get_recession_end()
    start_ind=np.asscalar(GDP[GDP['Quarter']==start].index.values)
    stop_ind=np.asscalar(GDP[GDP['Quarter']==stop].index.values)
    min_GDP=GDP['GDP in billions of chained 2009 dollars'][(start_ind-1):(stop_ind+1)].idxmin()
    

    return GDP['Quarter'][min_GDP]

get_recession_bottom()


# In[13]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    #import time 
    import datetime as dt
    import time as tm
    
    Housing=pd.read_csv('City_Zhvi_AllHomes.csv')
    #A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, 
    #Q3 is July through September, Q4 is October through December.
    drop_col=[]
    for col in Housing.columns: 
        if col[:2]=='20':
            continue
        elif col[:2]=='19':
            drop_col.append(col)
        else:
            continue 
    Housing=Housing.drop(drop_col, axis=1) # drop irrelevant columns
    Housing=Housing.drop(['RegionID','Metro','CountyName','SizeRank'], axis=1)

    Housing_Q=pd.DataFrame(Housing[["State","RegionName"]])

    #calculate quarter mean$
    for year in range(2000,2017):
        Housing_Q[str(year)+'q1'] = Housing[[str(year)+'-01',str(year)+'-02',str(year)+'-03']].mean(axis=1)
        Housing_Q[str(year)+'q2'] = Housing[[str(year)+'-04',str(year)+'-05',str(year)+'-06']].mean(axis=1)
        try: 
            Housing_Q[str(year)+'q3'] = Housing[[str(year)+'-07',str(year)+'-08',str(year)+'-09']].mean(axis=1)
        except: 
            Housing_Q[str(year)+'q3'] = Housing[[str(year)+'-07',str(year)+'-08']].mean(axis=1)
        try: 
            Housing_Q[str(year)+'q4'] = Housing[[str(year)+'-10',str(year)+'-11',str(year)+'-12']].mean(axis=1)
        except: 
            pass
        
    Housing_Q=Housing_Q.set_index(["State","RegionName"]) #set multi index
    Housing_Q=Housing_Q.rename(index={'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'})


    return Housing_Q

convert_housing_data_to_quarters()


# In[16]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    #Decline and growth of houseing prices between rec.start and rec.end
    #ttest comparing university and non university towns + p_value
    #return tupe (different, p, better)
    
    rec_start=get_recession_start()
    rec_end=get_recession_end()
    rec_bottom=get_recession_bottom()
    unitowns = get_list_of_university_towns()

    Housing_Data=convert_housing_data_to_quarters()    
    #bottom = get_recession_bottom()
    #start = get_recession_start()
    #hdata = convert_housing_data_to_quarters()
    bstart = Housing_Data.columns[Housing_Data.columns.get_loc(rec_start) -1]
    
    Housing_Data['ratio'] = Housing_Data[rec_bottom] - Housing_Data[rec_start]
    Housing_Data = Housing_Data[[rec_bottom,bstart,'ratio']]
    Housing_Data = Housing_Data.reset_index()
    unitowns_hdata = pd.merge(Housing_Data,unitowns,how='inner',on=['State','RegionName'])
    unitowns_hdata['uni'] = True
    hdata2 = pd.merge(Housing_Data,unitowns_hdata,how='outer',on=['State','RegionName',rec_bottom,bstart,'ratio'])
    hdata2['uni'] = hdata2['uni'].fillna(False)

    ut = hdata2[hdata2['uni'] == True]
    nut = hdata2[hdata2['uni'] == False]

    t,p = ttest_ind(ut['ratio'].dropna(),nut['ratio'].dropna())
    
    different = True if p < 0.01 else False

    better = "non-university town" if ut['ratio'].mean() < nut['ratio'].mean() else "university town"
    
    return different, p, better

run_ttest()


# In[ ]:





# In[ ]:




