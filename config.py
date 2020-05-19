import os
import sys


class RedditConfig:
    @staticmethod
    def _get_env(var_name):
        try:
            return os.environ[var_name]
        except KeyError:
            print(f'Please set the environment variable {var_name}')
            sys.exit(1)

    @staticmethod
    def client_id():
        return RedditConfig._get_env('client_id')

    @staticmethod
    def client_secret():
        return RedditConfig._get_env('client_secret')

    @staticmethod
    def user_agent():
        return RedditConfig._get_env('user_agent')
