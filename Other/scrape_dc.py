from spellchecker import SpellChecker
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import time
import requests
import datetime
import string


def get_subreddit_df(subreddit, max_size=1000):
    '''
    give function a subreddit string returns df of all 
    '''
    # base url
    base_url = 'https://api.pushshift.io/reddit/search/'
    # return df
    df = pd.DataFrame()
    # initial params
    params = {
        'subreddit' : subreddit, # /r page
        'size' : 500, # get max size
        'over_18': 'false', # remove nsfw posts
        'before': 1650603966, # start date
        'after': 1648875966, # end date
        'is_video': False
    }
    # loop to get df of elements
    while df.shape[0] < max_size:
        res = requests.get(base_url + 'submission/', params = params)
        # check if request cant pull
        if res.status_code != 200:
            print(f'Issue Pulling Data :: status code :: {res.status_code}')
            return df
        # make current timefram df
        current_df = pd.DataFrame(res.json()['data'])[['subreddit', 'selftext', 'title']]
        current_df['title'] = current_df['title']
        # add current df to historical df
        df = pd.concat([df, current_df], axis=0)
        # decrese start time - 20 days
        before_dt_time = datetime.datetime.fromtimestamp(params['before'])
        new_dt_b = before_dt_time - datetime.timedelta(days=20)
        params['before'] = int(new_dt_b.strftime('%s'))
        # decrease end time - 20 days
        after_dt_time = datetime.datetime.fromtimestamp(params['after'])
        new_dt_a = after_dt_time - datetime.timedelta(days=20)
        params['after'] = int(new_dt_a.strftime('%s'))
        # added sleep to not cause 429 error :: to mant pulls
        time.sleep(3)
    return df

def clean_df(df, col=''):

    copy_df = df.copy()
    # corrected col issues/spelling (things I found when looking at the data)
    copy_df[col] = copy_df[col].str.lower()
    copy_df[col] = copy_df[col].str.replace('eli5', '')
    copy_df[col] = copy_df[col].str.replace('https', '')
    copy_df[col] = copy_df[col].str.replace(':', '')
    spell = SpellChecker()
    copy_df[f'corrected_{col}'] = [' '.join(spell.split_words(sentence)) for sentence in copy_df[col]] 
    # [removed]
    # remove the numeric
    copy_df = copy_df[~copy_df[col].str.contains('\d')]
    # correct the spelling of sentences
    # ' '.join(spell.split_words(sentence.translate(str.maketrans('', '', string.punctuation)).lower()))
    # get character count for each post title 
    copy_df['char_count'] = [len(sentence.translate(str.maketrans('', '', string.punctuation))) for sentence in copy_df[col]]
    # get word count for each post title
    copy_df['word_count'] = [len(sentence.split()) for sentence in copy_df[col]]
    # get sentiment analysis of corrected title columns 
    copy_df['tone'] = [SentimentIntensityAnalyzer().polarity_scores(sentence) for sentence in copy_df[f'corrected_{col}']]
    copy_df = copy_df.join(pd.DataFrame(copy_df.pop('tone').values.tolist()))

    return copy_df

def main():
    try:
        # check if csv has historical data
        df_history = pd.read_csv('../data/Subreddits_Data.csv', usecols = ['subreddit','selftext', 'title', 'corrected_title', 'char_count', 'word_count', 'neg', 'neu', 'pos', 'compound'])
    except:
        # else make empty csv (not to cause error on concat)
        df_history = pd.DataFrame()
    print('Starting Shape:', df_history.shape)
    # pull subreddit posts for explainlikeimfive
    explain_like_im_five_df = get_subreddit_df('explainlikeimfive', max_size=7000)
    explain_like_im_five_df['subreddit'] = 1
    # pull subreddit posts for NoStupidQuestions
    shower_thoughts = get_subreddit_df('NoStupidQuestions', max_size=7000)
    shower_thoughts['subreddit'] = 0
    # concat new post data from NoStupidQuestions, explainlikeimfive subreddits
    subredt_joined_df = pd.concat([clean_df(explain_like_im_five_df, col='title'), clean_df(shower_thoughts, col='title')], axis=0)
    # concat new historical data and new data from NoStupidQuestions, explainlikeimfive subreddits and remove duplicates
    joined_df = pd.concat([df_history, subredt_joined_df], axis=0).drop_duplicates(keep='first')
    # write to csv new data
    joined_df.to_csv('../data/Subreddits_Data.csv', index=True)
    print('Ending Shape:', joined_df.shape)

if __name__ == '__main__':
    main()