from datetime import datetime, timedelta

now = datetime.today()
yesterday = datetime.today() - timedelta(days=1)
two_days = datetime.today() - timedelta(days=2)
week = datetime.today() - timedelta(days=7)
two_week = datetime.today() - timedelta(days=14)
month = datetime.today() - timedelta(days=30)
two_month = datetime.today() - timedelta(days=60)
