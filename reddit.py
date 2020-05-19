import praw
import pandas as pd

from config import RedditConfig


class RedditData:
    reddit = None
    subreddit = None
    limit = 5

    def __init__(self):
        # create a reddit connection
        self.reddit = praw.Reddit(client_id=RedditConfig.client_id(),
                                  client_secret=RedditConfig.client_secret(),
                                  user_agent=RedditConfig.user_agent())

    def set_sub(self, name, limit=5):
        self.subreddit = self.reddit.subreddit(name).new(limit=limit)
        return self.subreddit

    def rd_df(self, subreddit_name):
        # list for df conversion
        posts = []
        # return 100 new posts from 'thenetherlands'
        # self.set_sub('thenetherlands', limit=100)
        self.set_sub(subreddit_name, limit=100)
        # return the important attributes
        for post in self.subreddit:
            posts.append([post.title,
                          post.score,
                          post.num_comments,
                          post.selftext,
                          post.created,
                          post.pinned,
                          post.total_awards_received])
        # create a dataframe
        posts = pd.DataFrame(posts, columns=['title', 'score', 'comments', 'post', 'created', 'pinned', 'total awards'])
        return posts

    def pr_df(self):
        for post in self.subreddit:
            print({
                'title': post.title,                                    # Returns post title.
                'score': post.score,                                    # Returns number of up-votes or down-votes.
                'num_comments': post.num_comments,                      # Returns the number of comments on the thread.
                'selftext': post.selftext,                              # Returns the body of the post.
                'created': post.created,                                # Returns a timestamp for the post.
                'pinned': post.pinned,                                  # Indicates whether the thread was pinned.
                'total_awards_received': post.total_awards_received,    # Returns number of awards received by the post.
            })



# single subreddit new 5
# subreddit = reddit.subreddit('news').new(limit=5)
# multiple subreddits top 5
# subreddit = reddit.subreddit('news' + 'datascience').top(limit=5)


# # list for df conversion
# posts = []
# # return 100 new posts from wallstreetbets
# new_bets = reddit.subreddit('wallstreetbets').new(limit=100)
# # return the important attributes
# for post in new_bets:
#     posts.append([post.title, post.score, post.num_comments, post.selftext, post.created, post.pinned,
#                   post.total_awards_received])
# # create a dataframe
# posts = pd.DataFrame(posts, columns=['title', 'score', 'comments', 'post', 'created', 'pinned', 'total awards'])
# # return top 3 df rows
# posts.head(3)
# # https://medium.com/swlh/dashboards-in-python-using-dash-creating-a-data-table-using-data-from-reddit-1d6c0cecb4bd