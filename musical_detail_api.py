

def get_musical_detail_from_xml(musical, musical_id, root):
    for db_node in root:
        musical_info_dict = musical[musical_id]

        casting = db_node.find('prfcast')
        musical_info_dict['casting'] = get_text(casting)

        running_time = db_node.find('prfruntime')
        musical_info_dict['running_time'] = get_text(running_time)

        #db_node는 무조건 한개인것이 정상
        break


def get_text(xml):
    return xml.text