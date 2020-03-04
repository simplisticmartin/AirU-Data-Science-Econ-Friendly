#!/Users/ruoyanqin/anaconda/envs/py2/bin/python

# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import json
import re


# In[69]:

from uberpy import Uber


# In[366]:

from sklearn.feature_extraction.text import TfidfVectorizer


# In[135]:

##reviews
##listings
##listings_small
##neighbors

##get_A_B
##id_rowdix: dict k=id  val=row number


# # In[13]:

# cd /Users/tianhaolu/Documents/Playground/CornellTech


# In[591]:

def id_rowidx(listings):
    id_rowidx={listings['id'][i]:i for i in range(len(listings))}
    return id_rowdix


# In[614]:

idrowidx={listings['id'][i]:i for i in range(len(listings))}


# In[539]:

def dollar_to_int(a):
    return int(a['price'].replace('$', '').replace(',','').split(".")[0])


# In[541]:

listings['price']=listings.apply(dollar_to_int,axis=1)


# In[157]:

def strr(a):
    a=a['amenities'].split(",")
    a=map(lambda x: x.replace('{', '').replace('}', '').replace('"', ''),a)
    return a


# In[168]:

things=['TV','Wireless Internet','Air Conditioning','Kitchen','Heating']


# In[380]:

listings['description']=listings['description'].fillna('tianhao')


# In[162]:

def facilities(a):
    things=['TV','Wireless Internet','Air Conditioning','Kitchen','Heating']
    things_bool=[x in a['amenities_split'] for x in things]
    return pd.Series(things_bool)


# In[163]:

# listings['amenities_split']=listings.apply(strr,axis=1)


# In[165]:

# things_bool=listings.apply(facilities,axis=1)


# In[171]:

# ##有无家电
# for i in range(len(things)):
#     thing=things[i]
#     listings[thing]=things_bool[i]


# In[592]:

listings=pd.read_csv('listings.csv')

##listings wrangling DONE


# In[ ]:

# 1 min=0.33 mile
# 1 long=110 KM=63.58 mile


# In[593]:

#lon,lat,delta=73.9619,40.8075,0.002
#minutes=20
#price=500
#tv,wifi,ac,kit,heating,roomtype=1,0,0,0,1,'Entire home/apt'
def filt_1(a,lon,lat,delta,tv,wifi,ac,kit,heating,roomtype,price):
    pred=1
    pred*=(-a['longitude']<lon+delta and -a['longitude']>lon-delta)
    pred*=(a['latitude']<lat+delta and a['latitude']>lat-delta)
    pred*=(a['TV']>=tv)
    pred*=(a['Wireless Internet']>=wifi)
    pred*=(a['Air Conditioning']>=ac)
    pred*=(a['Kitchen']>=kit)
    pred*=(a['Heating']>=heating)
    pred*=(a['room_type']==roomtype)
    pred*=(a['price']<price)
    if pred==1:
        return True
    else:
        return False


# In[619]:

def filt_2(a,lon,lat,delta,tv,wifi,ac,kit,heating,roomtype,price,minutes):
    thresh=minutes*float(0.33)/63.58
    pred=1
    pred*=(-a['longitude']<lon+0.33/63.58 and -a['longitude']>lon-thresh)
    pred*=(a['latitude']<lat+thresh and a['latitude']>lat-thresh)
    pred*=(a['TV']>=tv)
    pred*=(a['Wireless Internet']>=wifi)
    pred*=(a['Air Conditioning']>=ac)
    pred*=(a['Kitchen']>=kit)
    pred*=(a['Heating']>=heating)
    pred*=(a['room_type']==roomtype)
    pred*=(a['price']<price)
    if pred==1:
        return True
    else:
        return False


# In[620]:

def get_A_B(listings,lon,lat,delta,tv,wifi,ac,kit,heating,roomtype,price,minutes):
    #return the json of hotels in same community, and a selection of hotels fitting that criteria
    listings['filt_1']=listings.apply(filt_1,args=(lon,lat,delta,tv,wifi,ac,kit,heating,roomtype,price),axis=1)
    listings['filt_2']=listings.apply(filt_2,args=(lon,lat,delta,tv,wifi,ac,kit,heating,roomtype,price,minutes),axis=1)
    
    A=listings[listings['filt_1']>0]
    B=listings[listings['filt_2']>0]
    A=A[['id','longitude','latitude','name','summary','price']]
    same_community = [ 
    dict([
        (colname, row[i]) 
        for i,colname in enumerate(A.columns)
    ])
    for row in A.values
    ]
    return same_community,B
    


# In[617]:

def uber_json(xid,listings,id_rowidx,B):
    xid=9062929
    xrow=idrowidx[xid]
    k=min(len(B)/10,20)
    top20=B.sort(['review_scores_value'],ascending=False).index[0:k]
    near=B.loc[top20]
    doc_id=[i for i in near.index]
    doc_id[-1]=xrow
    tfidf=vect.fit_transform(list(listings['description'][doc_id]))
    #print pd.DataFrame((tfidf * tfidf.T).A)[19]
    arr = pd.DataFrame((tfidf * tfidf.T).A)[19]
    argmax=arr.argsort()[-len(arr):][::-1]

    similar_id={}
    listings['uber']=0
    uber = Uber('uHcGyypDvCoajjhhx-cyTdcnpZzbQV9j', 'V320Y_XH3wStYXbNGaqgoUV1dGX84eYfJfaCHNXS','GxoruYkFBi_kKaCYwYnILL_45UuVE729e5ohN7wW')
    for x in argmax:

        raw_row=doc_id[x]
        lon=listings['longitude'][raw_row]
        lat=listings['latitude'][raw_row]
        end_lon =listings['longitude'][xrow]
        end_lat =listings['latitude'][xrow]
        fare_estimate = uber.get_price_estimate(lat,lon, end_lat,end_lon)
        uberfare=fare_estimate['prices'][0]['low_estimate']*2
        totalfare=listings['price'][raw_row]+uberfare
        if totalfare<price:
            similar_id[raw_row]=uberfare
            print(raw_row)
            listings['uber'][raw_row]=uberfare

        if len(similar_id)==5:
            break
    sim_id=similar_id.keys()
    temp=listings.loc[sim_id]
    ttemp=temp[['id','longitude','latitude','name','summary','price','uber']]
    dtemp= [ 
        dict([
            (colname, row[i]) 
            for i,colname in enumerate(ttemp.columns)
        ])
        for row in ttemp.values
    ]
    return dtemp

#with open('sample_filt3.json', 'w') as outfile:
#    json.dump(dtemp, outfile,indent=4)
    
    
    


# In[588]:

#similar_id


# In[566]:

#similar_id


# In[ ]:




# In[29]:

#from uber_rides.session import Session


# In[30]:

#session = Session(server_token='V320Y_XH3wStYXbNGaqgoUV1dGX84eYfJfaCHNXS')


# In[31]:

#from uber_rides.client import UberRidesClient


# In[32]:

#client = UberRidesClient(session)


# In[42]:

#client = UberRidesClient(session)
#response = client.get_products(37.77, -122.41)
#products = response.json.get('products')


# In[37]:

#product_id = products[0].get('product_id')


# In[51]:

#from uber_rides.auth import AuthorizationCodeGrant


# In[570]:

#uber = Uber('uHcGyypDvCoajjhhx-cyTdcnpZzbQV9j', 'V320Y_XH3wStYXbNGaqgoUV1dGX84eYfJfaCHNXS','GxoruYkFBi_kKaCYwYnILL_45UuVE729e5ohN7wW')


# In[ ]:




# In[ ]:


