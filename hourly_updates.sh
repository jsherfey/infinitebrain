#! /bin/bash

# update twitter feed
cd /project/infinitebrain
python manage.py update_tweets
python manage.py show_tweets

