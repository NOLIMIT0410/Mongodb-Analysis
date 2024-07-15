import pandas
import pandas as pd
df = pd.read_csv("data/listings.csv")

column_to_delete = ['latitude','longitude','minimum_nights','maximum_nights','minimum_minimum_nights','maximum_minimum_nights','minimum_maximum_nights','maximum_maximum_nights','minimum_nights_avg_ntm','maximum_nights_avg_ntm']
df.drop(column_to_delete, axis=1, inplace=True)

df.to_csv('data/listings_clean.csv', index=False)