import requests
import configparser
import xml.etree.ElementTree as ET
import musical_list_api as ml
import musical_detail_api as md
import insert_db as db
import webhook


def build_query_param(param_dict):
    query = ""
    for key, val in param_dict.items():
        query += ("&" + key + "=" + str(val))
    return query


def api_request(root_url, secret_key, query):
    url = root_url+secret_key+query
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(filenames='open-api.ini')
    secret_key = config['DEFAULT']['SECRET_KEY']

    root_url = "http://www.kopis.or.kr/openApi/restful/pblprfr?service="
    stdate = 20230801
    eddate = 20230810
    cpage = 0
    rows = 100
    shcate = "GGGA"
    list_api_param_dict = {
        'stdate': stdate,
        'eddate': eddate,
        'cpage': cpage,
        'rows': rows,
        'shcate': shcate
    }

    musical_dict = {}

    # 공연 목록 api call 후 파싱, 최대 페이지는 99페이지로 제한
    for i in range(1, 100):
        list_api_param_dict['cpage'] = i
        query = build_query_param(param_dict=list_api_param_dict)
        http_response_text = api_request(root_url=root_url, secret_key=secret_key, query=query)
        root = ET.fromstring(http_response_text)
        if root.find('db') is None:
            break
        ml.get_musical_from_xml(musical=musical_dict, root=root)


    root_url = "http://kopis.or.kr/openApi/restful/pblprfr/"
    for musical_id, val in musical_dict.items():
        child_url = root_url + musical_id + "?service="
        http_response_text = api_request(root_url=child_url, secret_key=secret_key, query="")
        root = ET.fromstring(http_response_text)
        if root.find('db') is None:
            continue
        md.get_musical_detail_from_xml(musical=musical_dict, musical_id=musical_id, root=root)

    print(len(musical_dict))
    db.db_insert(musical_dict)

    webhook.send_message_to_slack()



