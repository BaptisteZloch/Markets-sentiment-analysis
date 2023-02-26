import re
import os
from tweepy import Client
import pandas as pd


twitter_token = os.getenv("TWITTER_BEARER_TOKEN")


def fetch_tweets(query: str, clean: bool = True, count: int = 100) -> pd.DataFrame:
    """Function that query the twitter API.

    Args:
        query (str): The query is the twitter language.
        clean (bool): If the dataframe needs to be cleaned of not. Default to True.

    Returns:
        pd.DataFrame: The data fetched in a tabluar format, with only one column : text.
    """
    assert (
        count >= 5 and count <= 100
    ), "Wrong count parameter, it should be between 5 and 100."

    client = Client(bearer_token=twitter_token)

    raw_tweets = client.search_recent_tweets(query, max_results=count)

    raw_tweets_df = pd.DataFrame([tweet.data for tweet in raw_tweets.data]).drop(
        columns=["id", "edit_history_tweet_ids"]
    )

    if clean is True:
        return clean_tweet_dataframe(raw_tweets_df)

    return raw_tweets_df


def clean_tweet_dataframe(raw_df: pd.DataFrame, column: str = "text") -> pd.DataFrame:
    """Function that will clean an entire column of a dataframe.

    Args:
        raw_df (pd.DataFrame): The dataframe to clean.
        column (str): The column containing the tweets. Default to text.

    Returns:
        pd.DataFrame: _description_
    """

    def clean_tweet(txt: str) -> str:
        """This function takes a string as input and returns a cleaned version of the
        string by removing hashtags, newlines, URLs, @ symbols, and emojis. It also
        converts the string to lowercase.

        Args:
            txt (str): The input string to be cleaned.

        Returns:
            str: The cleaned version of the input string.
        """
        txt = str(txt)
        txt = re.sub(r"#", "", txt)
        txt = re.sub(r"\n", "", txt)
        txt = re.sub(r"https?:\/\/\S+", "", txt)
        txt = re.sub(r"@", "", txt)
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002500-\U00002BEF"  # chinese char
            "\U00002702-\U000027B0"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\ufe0f"  # dingbats
            "\u3030"
            "]+",
            flags=re.UNICODE,
        )

        return emoji_pattern.sub(r"", txt).lower()

    raw_df[column] = raw_df[column].apply(clean_tweet)
    return raw_df
