import pandas as pd
import numpy as np
import math

def find_closest_sales(n_closest, sales_df, property_lat, property_lon):
#  --> dataframe of n closest sales
    ################# Brute Force method iterating over each row ################
    # Time complext for this method:
    # 1. for each property, iterate through sales_df and calculate distance, it will take O(N)
    # 2. sorting and get top n_closest will take O(NlogN): it can be optimized to O(Nlog(n_closest))
    # 3. if properties have total of M values, the toal time complexity is O(MN + MNlogN)
    sales_df['distance'] = 0.0
    for i in range(len(sales_df)):
        sales_df.loc[i, 'distance']= 3963 * 2 * math.asin(math.sqrt(math.sin((math.radians(sales_df.loc[i, 'lat']) - math.radians(property_lat))/2)**2 + math.cos(math.radians(property_lat)) * math.cos(math.radians(sales_df.loc[i, 'lat'])) * math.sin((math.radians(sales_df.loc[i, 'long']) - math.radians(property_lon))/2)**2))
    return sales_df.sort_values("distance", ascending=True).head(n_closest).drop("distance", axis=1)
    ################ Use df.apply method##########################################
    # sales_df['distance'] = sales_df.apply(lambda cols: 3963 * 2 * math.asin(math.sqrt(math.sin((math.radians(cols.lat) - math.radians(property_lat))/2)**2 + math.cos(math.radians(property_lat)) * math.cos(math.radians(cols.lat)) * math.sin((math.radians(cols.long) - math.radians(property_lon))/2)**2)), axis = 1)
    # return sales_df.sort_values("distance", ascending=True).head(n_closest).drop("distance", axis=1)
    ################# Method with Numpy and vectorization#########################
    # sales_df['lat_rad'], sales_df['long_rad'] = np.radians(sales_df['lat']), np.radians(sales_df['long'])
    # sales_df['lat_diff'] = sales_df['lat_rad'] - math.radians(property_lat)
    # sales_df['long_diff'] = sales_df['long_rad'] - math.radians(property_lon)
    # sales_df['distance'] = 3963 * 2 * np.arcsin(np.sqrt(np.sin(sales_df['lat_diff']/2)**2 + math.cos(math.radians(property_lat)) * np.cos(sales_df['lat_rad']) * np.sin(sales_df['long_diff']/2)**2))
    # return sales_df.sort_values("distance", ascending=True).head(n_closest).drop(["distance", "lat_rad", "lat_diff", "long_diff", "long_rad"], axis=1)
    ################ Convert np code to one line coder##################################
    # sales_df['distance'] = 3963 * 2 * np.arcsin(np.sqrt(np.sin((np.radians(sales_df['lat']) - math.radians(property_lat))/2)**2 + math.cos(math.radians(property_lat)) * np.cos(np.radians(sales_df['lat'])) * np.sin((np.radians(sales_df['long']) - math.radians(property_lon))/2)**2))
    # return sales_df.sort_values("distance", ascending=True).head(n_closest).drop("distance", axis=1)

sales_df = pd.read_csv("sales.csv")
properties_df = pd.read_csv("properties.csv")
for index, row in properties_df.iterrows():
    print(find_closest_sales(5, sales_df, row['lat'], row['long']))
