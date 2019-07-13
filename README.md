# 5AM Bot

Telegram bot for groups waking up at 5am.

Deploy to gcloud:

'''bash
gcloud beta functions deploy webhook --runtime python37 --trigger-http --set-env-vars "GCLOUD=TRUE"
'''
