# Subreddit Classifier

- By: Robert Sarno

# Executive Summary:

### Problem:

> Reddit has one of the largest variety of question forums, entertaining or more formal. However, the challenge is that as cool as all these forums are there are a lot of similar subreddits and for new users like older generations its daunting to understand where you should post your question to.

> Currently Reddit is primarily used by younger generations. Where the older generation user base is lacking. This specific situation will cause less user traffic. Therefore, I beleive new methods need to be developed to help users understand where to post.

> My Classification model will help new users understand what simular subreddits they should post there questions to, with a goal accuracy of 70%. I will specifically be looking at subreddits r/NoStupidQuestions and r/explainlikeimfive for this problem.

> If we incorporate this model into the new user workflow. I believe it will increase reddits monthly activity substatially. Specifically targeting the older generations will only benefit sales revenue. Which will benefit Reddit as a whole. So leets make it happen.

### Data Dictionary:

`Subreddits_Data.csv`

| Field Name          | Type   | Description                           |
| ------------------- | ------ | ------------------------------------- |
| **subreddit**       | string | subreddit identifier (1,0)            |
| **selftext**        | string | self text of subreddit post           |
| **title**           | string | title text of subreddit post          |
| **corrected_title** | string | spell checked tilte of subreddit post |
| **char_count**      | int    | number of characters in title         |
| **word_count**      | int    | number of words in title              |
| **neg**             | float  | negative polarity score from nltk     |
| **neu**             | float  | neutral polarity score from nltk      |
| **pos**             | float  | positive polarity score from nltk     |
| **compound**        | float  | compound polarity score from nltk     |

### Process:

1. Scraping subreddit data.
2. EDA.
3. Adding additional features to help classification model prediction.
4. Removing stop words and Vectorizing title data.
5. Training and Testing Model.
6. Obtaining Metrics, and Graphics For Data.

### Conclusion

> In Conclusion my model preforms great but not outstanding. I reached my goal of predicting a 70% accuracy and getting a performance of a 0.86 balanced accuracy score, 0.87 f1 score, and a 0.87 roc auc score however there is still room for improvement. I believe where my model is failing is high frequency words that exist in both subreddits they are skewing my model’s classification and need to be investigated further. I would recommend using my model to help users understand where their posts should go especially for new users. Regardless, I still believe my model preforms well in making predictions and will help new users in making decisions on what subreddit to post to.

### Resources

- https://towardsdatascience.com/multi-class-text-classification-model-comparison-and-selection-5eb066197568
- https://www.kaggle.com/getting-started/42409
- https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html
