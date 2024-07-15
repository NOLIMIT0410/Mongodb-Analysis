# AirBnB MongoDB Analysis

## Original data
- [listings.csv](https://data.insideairbnb.com/spain/comunidad-de-madrid/madrid/2023-12-15/data/listings.csv.gz)comes from website [inside_Airbnb](http://insideairbnb.com/get-the-data.html). Basically it is a website that shows you information of rentals in a city where Airbnb is functioning and you are interested in, so that you can book your hotels. The city I choose to analysis is Madrid, where the most recent Valorant tournament takes place.

- The file is in csv form.

## Some raw data of the original data set:
| id                 | listing_url                                       | scrape_id     | last_scraped | source      | name                                       | description                           | neighborhood_overview | picture_url                                                                                        | host_id   | host_url                                  | host_name | host_since | host_location     | host_about                                                                                                                                                                                                                                                                                                                                                                    | host_response_time  | host_response_rate | host_acceptance_rate | host_is_superhost | host_thumbnail_url                                                                                           |
|--------------------|--------------------------------------------------|---------------|--------------|-------------|--------------------------------------------|-------------------------------------|-----------------------|----------------------------------------------------------------------------------------------------|-----------|------------------------------------------|-----------|------------|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|---------------------|----------------------|-------------------|-------------------------------------------------------------------------------------------------------------|
| 1046255434342767173 | https://www.airbnb.com/rooms/1046255434342767173 | 20231215032748 | 2023-12-15   | city scrape | Rental unit in Madrid · ★New · 1 bedroom · 3 beds · 1.5 baths |                                     |                       | https://a0.muscache.com/pictures/prohost-api/Hosting-1046255434342767173/original/37dd6576-8ecc-4157-b621-469636d3c56c.jpeg | 529402573 | https://www.airbnb.com/users/show/529402573 | Sara      | 2023-08-02 |                    |                                                                                                                                                                                                                                                                                                                                                                               | within an hour      | 100%                | 100%                 | f                 | https://a0.muscache.com/im/pictures/user/f38ff89d-45d3-4229-b14a-c44bd8904c9c.jpg?aki_policy=profile_small |
| 1046239141714406672 | https://www.airbnb.com/rooms/1046239141714406672 | 20231215032748 | 2023-12-15   | city scrape | Rental unit in Madrid · ★New · 2 bedrooms · 4 beds · 1 bath |                                     |                       | https://a0.muscache.com/pictures/prohost-api/Hosting-1046239141714406672/original/8ddb043a-0757-47b7-887b-64089c2ba366.jpeg | 346367515 | https://www.airbnb.com/users/show/346367515 | Ukio      | 2020-05-15 | Barcelona, Spain  | Ukio's mission is to empower individuals to live where and when they want.  We do this by disrupting the traditional residential real estate market by providing high quality and furnished apartments for stays of one month or more.  We remove all the frustration around finding a rental with no long-term contracts, moving/buying furniture, security deposits, broker fees, etc. All you have to do is show up and start living. | within a few hours | 96%                 | 99%                  | f                 | https://a0.muscache.com/im/pictures/user/f790e9f4-a54f-4132-83d8-f71b8c9e3760.jpg?aki_policy=profile_small |

**Only a part of the original data is shown here because there are 70+colunms and lots of empty cells or extremly long cells. I don't want to make this table look insanly long.**

## Data scrubbing:
As I have mentioned above, the original data contains too many colunms which are completely useless to data analysis that we are about to do. So the best solution is just deleting all of those. This will also make results of our mongodb queries more tidy and readable. Part of the code is shown below:

``` python
import pandas
import pandas as pd
df = pd.read_csv("data/listings.csv")

column_to_delete = ['latitude','longitude','minimum_nights','maximum_nights','minimum_minimum_nights','maximum_minimum_nights','minimum_maximum_nights','maximum_maximum_nights','minimum_nights_avg_ntm','maximum_nights_avg_ntm']
df.drop(column_to_delete, axis=1, inplace=True)

df.to_csv('data/listings_clean.csv', index=False)
```

## **Analysis**
Queries:
- show exactly two documents from the listings collection in any order
```mongodb
#query:use find function and limit the result to 2
test> db.listings.find().limit(2)
#example result:
[
  {
    _id: ObjectId('660c9fea15e68b553413bc40'),
    id: 6369,
    listing_url: 'https://www.airbnb.com/rooms/6369',
    scrape_id: Long('20231215032748'),
    last_scraped: '2023-12-15',
    source: 'city scrape',
    name: 'Rental unit in Madrid · ★4.88 · 1 bedroom · 1 bed · 1 private bath',
    description: '',
    neighborhood_overview: '',
    picture_url: 'https://a0.muscache.com/pictures/683224/4cc318c4_original.jpg',
    host_id: 13660,
    host_url: 'https://www.airbnb.com/users/show/13660',
    host_name: 'Simon',
    host_since: '2009-04-16',
    host_location: 'Madrid, Spain',
    host_about: 'Gay couple, heterofriendly, enjoy having guests home. I am  contemporary dancer specialized in dance therapy and my partner works in interantional marketing.\n' +
      'Fluent in several languages: spanish, english, german, russian..',
    host_response_time: 'within an hour',
    host_response_rate: '100%',
    host_acceptance_rate: '78%',
    host_is_superhost: 't',
    host_thumbnail_url: 'https://a0.muscache.com/im/pictures/user/79a6352b-7137-4566-aa5e-994a921d12c2.jpg?aki_policy=profile_small',
    host_picture_url: 'https://a0.muscache.com/im/pictures/user/79a6352b-7137-4566-aa5e-994a921d12c2.jpg?aki_policy=profile_x_medium',
    host_neighbourhood: 'Hispanoamérica',
    host_listings_count: 1,
    host_total_listings_count: 1,
    host_verifications: "['email', 'phone']",
    host_has_profile_pic: 't',
    host_identity_verified: 't',
    neighbourhood: '',
    neighbourhood_cleansed: 'Hispanoamérica',
    neighbourhood_group_cleansed: 'Chamartín',
    property_type: 'Private room in rental unit',
    room_type: 'Private room',
    accommodates: 2,
    bathrooms: '',
    bathrooms_text: '1 private bath',
    bedrooms: '',
    beds: 1,
    amenities: '[]'}
]
```
- show exactly 10 documents in any order, but "prettyprint" in easier to read format, using the pretty() function.
```mongodb
#query:use find function again, limit the result to 10 and reformat using pretty function
test> db.listings.find().limit(10).pretty()
#example result:
[
  {
    _id: ObjectId('660c9fea15e68b553413bc40'),
    id: 6369,
    listing_url: 'https://www.airbnb.com/rooms/6369',
    scrape_id: Long('20231215032748'),
    last_scraped: '2023-12-15',
    source: 'city scrape',
    name: 'Rental unit in Madrid · ★4.88 · 1 bedroom · 1 bed · 1 private bath',
    description: '',
    neighborhood_overview: '',
    picture_url: 'https://a0.muscache.com/pictures/683224/4cc318c4_original.jpg',
    host_id: 13660,
    host_url: 'https://www.airbnb.com/users/show/13660',
    host_name: 'Simon',
    host_since: '2009-04-16',
    host_location: 'Madrid, Spain',
    host_about: 'Gay couple, heterofriendly, enjoy having guests home. I am  contemporary dancer specialized in dance therapy and my partner works in interantional marketing.\n' +
      'Fluent in several languages: spanish, english, german, russian..',
    host_response_time: 'within an hour',
    host_response_rate: '100%',
    host_acceptance_rate: '78%',
    host_is_superhost: 't',
    host_thumbnail_url: 'https://a0.muscache.com/im/pictures/user/79a6352b-7137-4566-aa5e-994a921d12c2.jpg?aki_policy=profile_small',
    host_picture_url: 'https://a0.muscache.com/im/pictures/user/79a6352b-7137-4566-aa5e-994a921d12c2.jpg?aki_policy=profile_x_medium',
    host_neighbourhood: 'Hispanoamérica',
    host_listings_count: 1,
    host_total_listings_count: 1,
    host_verifications: "['email', 'phone']",
    host_has_profile_pic: 't',
    host_identity_verified: 't',
    neighbourhood: '',
    neighbourhood_cleansed: 'Hispanoamérica',
    neighbourhood_group_cleansed: 'Chamartín',
    property_type: 'Private room in rental unit',
    room_type: 'Private room',
    accommodates: 2,
    bathrooms: '',
    bathrooms_text: '1 private bath',
    bedrooms: '',
    beds: 1}
]
```
- choose two hosts who are superhosts, and show all of the listings offered by both of the two hosts only show the name, price, neighbourhood, host_name, and host_is_superhost for each result
```mongodb
#query: use match order to test crtiticals and group the result using group function, and limit the result to 2
test> db.listings.aggregate([ { $match: { host_is_superhost: 't' } }, { $group: { _id: "$host_id",  listings: { $push: "$$ROOT" } } }, { $limit: 2  }] )
#example result:
[
  {
    _id: 13660,
    listings: [
      {
        _id: ObjectId('660c9fea15e68b553413bc40'),
        id: 6369,
        listing_url: 'https://www.airbnb.com/rooms/6369',
        scrape_id: Long('20231215032748'),
        last_scraped: '2023-12-15',
        source: 'city scrape',
        name: 'Rental unit in Madrid · ★4.88 · 1 bedroom · 1 bed · 1 private bath',
        description: '',
        neighborhood_overview: '',
        picture_url: 'https://a0.muscache.com/pictures/683224/4cc318c4_original.jpg',
        host_id: 13660,
        host_url: 'https://www.airbnb.com/users/show/13660',
        host_name: 'Simon',
        host_since: '2009-04-16',
        host_location: 'Madrid, Spain',
        host_about: 'Gay couple, heterofriendly, enjoy having guests home. I am  contemporary dancer specialized in dance therapy and my partner works in interantional marketing.\n' +
          'Fluent in several languages: spanish, english, german, russian..',
        host_response_time: 'within an hour',
        host_response_rate: '100%',
        host_acceptance_rate: '78%',
        host_is_superhost: 't',
        host_thumbnail_url: 'https://a0.muscache.com/im/pictures/user/79a6352b-7137-4566-aa5e-994a921d12c2.jpg?aki_policy=profile_small',
        host_picture_url: 'https://a0.muscache.com/im/pictures/user/79a6352b-7137-4566-aa5e-994a921d12c2.jpg?aki_policy=profile_x_medium',
        host_neighbourhood: 'Hispanoamérica',
        host_listings_count: 1,
        host_total_listings_count: 1,
        host_verifications: "['email', 'phone']",
        host_has_profile_pic: 't',
        host_identity_verified: 't',
        neighbourhood: '',
        neighbourhood_cleansed: 'Hispanoamérica',
        neighbourhood_group_cleansed: 'Chamartín',
        property_type: 'Private room in rental unit',
        room_type: 'Private room',
        accommodates: 2,
        bathrooms: '',
        bathrooms_text: '1 private bath',
        bedrooms: '',
        beds: 1
        }
    ]
  }
]
```
- find all the unique host_name values
```mongodb
#query: use distinct function
test> db.listings.distinct('host_name')
#example result:
[
  '',                       '(Mateo )',              '4 Bears',
  '60 Balconies',           'A',                     'A Leonor',
  'A Va',                   'ALEjandro',             'ANA Rita',
]
```

- find all of the places that have more than 2 beds in a neighborhood of your choice, ordered by review_scores_rating descending only show the name, beds, review_scores_rating, and price
```mongodb
#query: use **and** order to test for multiple criticals, choose the order using sort function
test> db.listings.find({ $and: [ { beds: { $gt: 2 } }, { neighbourhood_group_cleansed:'Latina' }, { review_scores_rating: { $ne: null } }] }, { name: 1, beds: 1, review_scores_rating: 1, price: 1 }).sort({ review_scores_rating: -1}) 
#example result:
[
  {
    _id: ObjectId('660c9fea15e68b553413c5b9'),
    name: 'Home in Madrid · 3 bedrooms · 4 beds · 1 bath',
    beds: 4,
    price: '',
    review_scores_rating: ''
  },
  {
    _id: ObjectId('660c9fea15e68b553413c693'),
    name: 'Rental unit in Madrid · 3 bedrooms · 3 beds · 1 bath',
    beds: 3,
    price: '$51.00',
    review_scores_rating: ''
  },
  {
    _id: ObjectId('660c9feb15e68b553413d04c'),
    name: 'Rental unit in Madrid · 3 bedrooms · 5 beds · 2 baths',
    beds: 5,
    price: '',
    review_scores_rating: ''
  }
]
```
- show the number of listings per host
```mongodb
#query: use aggregate function
db.listings.aggregate([ { $group: { _id: "$host_id", listingCount: { $sum: 1 } } }] )
#example result:
[
  { _id: 158306838, listingCount: 1 },
  { _id: 217783972, listingCount: 1 },
  { _id: 26340878, listingCount: 1 },
]
```
- find the average review_scores_rating per neighborhood, and only show those that are 4 or above, sorted in descending order of rating (see the docs)
```mongodb
#query: use match function to pick those with 4 or above review scores, use group function to group neighbourhood and avgrating. Lastly, use sort function to determine order
test> db.listings.aggregate([ { $match: { review_scores_rating: { $gte: 4 } } }, { $group: { _id: "$neighbourhood", avgRating: { $avg: "$review_scores_rating" } } }, { $match: { avgRating: { $ne: null } } }, { $sort: { avgRating: -1 } }] )
#example result
[
  { _id: 'Madrid, Centro Madrid, Spain', avgRating: 5 },
  { _id: 'Spain', avgRating: 5 },
  { _id: 'Madrid, Madrid , Spain', avgRating: 5 },
]
```

## Insights:
for example:
- there are 4273+ distinct host name in Madrid offering rental services. Which is a huge amount.
- there are 20 listings that have more than two beds in the neighbourhood named "Latina"
- the listing that offers most beds in Latina offers 5 beds, which is good for family trip, but the price is also relatively higher than others
- host_id 4347030 is the one with most listings.

