import pymysql
import configparser
import webhook


def db_insert(musical_dict):

    preprocessing(musical_dict)
    exception_list = []

    config = configparser.ConfigParser()
    config.read(filenames='open-api.ini')
    host = config['DATABASE']['HOST']
    user = config['DATABASE']['USER']
    password = config['DATABASE']['PASSWORD']
    db = config['DATABASE']['DB']
    conn = pymysql.connect(
        host=host, user=user, password=password, db=db
    )
    cursor = conn.cursor()

    deleted_musical_dict = {
    }
    deleted_musical_query = "SELECT id from musical_deleted"
    cursor.execute(deleted_musical_query)
    deleted_musical_list = cursor.fetchall()
    for deleted_musical in deleted_musical_list:
        deleted_musical_dict[deleted_musical[0]] = 1
    webhook.db_insert_result['deleted forever'] = len(deleted_musical_list)
    for key, musical in musical_dict.items():
        if musical['musical_id'] in deleted_musical_dict:
            continue
        data = [musical['musical_id'], musical['begin_date'], musical['end_date'], musical['casting'],
                musical['genre'], musical['musical_status'], musical['name'], musical['place_name'],
                musical['poster_url'], musical['running_time']]
        query = "INSERT INTO musical (id,begin_date,end_date,casting," \
                "genre,musical_status,name,place_name,poster_url,running_time) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        webhook.db_insert_result['total data count'] += 1
        try:
            cursor.execute(query, data)
            conn.commit()
            webhook.db_insert_result['total success'] += 1
        except Exception as e:
            conn.rollback()
            print(f'예외가 발생했습니다. 예외 메세지 : {e}')
            exception_detail = {
                'message': e,
                'musical_info': musical
            }
            exception_list.append(exception_detail)
            webhook.db_insert_result['total failure'] += 1
    conn.close()
    webhook.db_insert_result['exception_list'] = exception_list


def preprocessing(musical_dict):
    for musical in musical_dict.values():
        if musical['casting'] == ' ':
            musical['casting'] = None
