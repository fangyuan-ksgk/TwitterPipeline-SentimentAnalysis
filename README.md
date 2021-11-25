# TwitterPipeline-SentimentAnalysis

1. Created End-to-End Twitter Pipeline using Tweepy API (v2.0) (academic account). Allowed for scraping tweets & user informations from scratch, mining, cleaning the data and put them into a .csv file using Pandas etc. I built this since many prexisting version of twitter pipeline online is outdated and not useful.
2. The Pipeline allows for extracting any number of relevant tweets in a specified time range, and write the result into a csv file. I uses academic account for Tweepy API v2, the 'search_all_tweets' are disabled and 'search_recent_tweets' capped number of tweets extracted each time to 100. This pipeline overcomes this issue through caching the posted time for the last extracted tweets, and recursively channel the data into a csv file. 
3. For implementation, check the 'illustration' notebook file.
4. (TBD) Conducted Sentiment Analysis on COVID vaccines, conducted analysis comparing Pfizer and AstraZeneca.
