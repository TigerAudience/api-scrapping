

def get_musical_from_xml(musical, root):
    for db_node in root:
        info = {}
        musical_id = db_node.find('mt20id')
        info['musical_id'] = get_text(musical_id)

        name = db_node.find('prfnm')
        info['name'] = get_text(name)

        begin_date = db_node.find('prfpdfrom')
        info['begin_date'] = get_text(begin_date)

        end_date = db_node.find('prfpdto')
        info['end_date'] = get_text(end_date)

        place_name = db_node.find('fcltynm')
        info['place_name'] = get_text(place_name)

        poster_url = db_node.find('poster')
        info['poster_url'] = get_text(poster_url)

        genre = db_node.find('genrenm')
        info['genre'] = get_text(genre)

        musical_status = db_node.find('prfstate')
        info['musical_status'] = get_text(musical_status)

        musical[get_text(musical_id)] = info


def get_text(xml):
    if xml is None:
        return None
    return xml.text
