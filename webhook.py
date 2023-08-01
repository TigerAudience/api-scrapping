import configparser
import requests

db_insert_result = {
    'total data count': 0,
    'total success': 0,
    'total failure': 0,
    'exception_list': []
}


def text_builder():
    result_text = f"가져온 데이터의 총 개수는 {db_insert_result['total data count']}입니다.\n" \
                  f"데이터베이스에 입력된 데이터 개수 : {db_insert_result['total success']}\n" \
                  f"데이터베이스 입력에 실패한 데이터 개수 : {db_insert_result['total failure']}\n"
    exception_list = db_insert_result['exception_list']
    max_cnt = 10
    cnt = 0
    for exception_info in exception_list:
        if cnt >= max_cnt:
            break
        result_text += (f"\n에러 메세지 : {exception_info['message']}, "
                      f"공연 정보 [공연 id : {exception_info['musical_info']['musical_id']}, "
                      f"공연 이름 : {exception_info['musical_info']['name']}]\n")
        cnt += 1
    return result_text


def send_message_to_slack():
    config = configparser.ConfigParser()
    config.read(filenames='open-api.ini')
    url = config['WEBHOOK']['URL']
    text = text_builder()
    payload = {
        "text": text
    }

    requests.post(url, json=payload)
