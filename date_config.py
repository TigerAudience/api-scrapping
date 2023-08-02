import datetime
from pytz import timezone
from datetime import datetime
from datetime import timedelta

start_date_api_format = ""
end_date_api_format = ""


def get_date():
    today = datetime.now(timezone('Asia/Seoul'))
    global start_date_api_format
    start_date_api_format = today.strftime("%Y%m%d")
    tomorrow = today + timedelta(days=1)
    global end_date_api_format
    end_date_api_format = tomorrow.strftime("%Y%m%d")
