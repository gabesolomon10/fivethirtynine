Gabriel Solomon
Naomi Pohl
Noah Hindes
Pedro Peterson

<strong>CIS550 Political Calendar Project</strong>

a. Motivation for the idea:

Our project is predicated on the idea that we are often inundated with short-term updates on political events and 
sentiments (e.g. President/Congress approval rating changed by x percentage points in response to new bill/proposal), 
but that the drivers of long-term trends can be much more difficult to identify. The impetus for our project is the 
desire for users to explore correlations between economic data, major news developments and prominent social media 
trends in order to investigate more holistic understanding of political sentiment (not contingent on day-to-day changes).

b. Description of the complementary sources you intend to use for data, and how you intend to ingest the data into your 
database:

We plan to use the following datasets: 

Trendogate (trending hashtags)
Daily top national headlines from Google News API
New York Times Daily Archives
Fivethirtyeight daily presidential approval ratings (.csv)
Fivethirtyeight daily generic ballot polls (.csv)
Historical stock prices from Federal Reserve(.csv)

In order to ingest the data into the database, we will transfer the .csv data files into a mySQL or noSQL database using 
sqlizer.io, and use databasing techniques (joins) to combine the stock pricing indices into one table.  Then we will use 
Trendogate and Google News API to generate JSON objects with the appropriate data that we require, and use MongoDB to 
parse this data and query over it as appropriate.  Finally, we will combine these tables in a MongoDB database and use 
that to create the calendar application.
 

c. Proposed relational schema:
 
Twitter{tweet_id, date, hashtag}
News{date, popularity_rank, headline, URL}
President Approval Ratings{poll_id, startdate, enddate, pollster, approval_estimate, disapprove_estimate}
Generic Ballot Polls {poll_id, startdate, enddate, dem_estimate, rep_estimate, pollster_grade}
Stock Prices [merging multiple .CSVs] {date, DowClose, SP_CLose, NASDAQ_Close}

d. Features that will definitely be implemented in the application 

i) Front-end calendar display with daily measures news headlines, trending tweets,
economic markers, presidential approval, and generic congressional ballot 

ii) Pop-up functionality for each day with top Twitter trends, news content and links

iii)Ability to view events and news headline sby those that occurred on the days with the
largest changes in presidential approval

iv)Ability to organize data by weeks/months and view trends across these time
periods

v)Users can organize by keywords (e.g: “hurricane”) and view how presidential
approval changed the last time this keyword was mentioned as a top news headline or
trended on twitter

e. Features that might implemented in the application, given enough time
 
i) AWS hosting of our database (rather than local)

ii) Live feed of one or more data source (rather than static, retroactive grab)

iii)Tweet sentiment analysis


f. Technology and tools to be used 

Flask/Python (application), 
postgresSQL and/or MySQL, 
Heroku, 
Buckets and/or Amazon RDS (MySQL)
Twitter API, 
Google News API
MongoDB
NoSQL

g. Member responsibility for project components 

Gabe:  backend connection/NodeJS, support Flask


Naomi: Flask, Twitter/Google API retrieval, web scraping, support NodeJS

Noah: All querying (basics + complex what-ifs), HTML/CSS, Presentation

Pedro: AWS, cleaning and formatting data, populating database, other front-end functionalities


