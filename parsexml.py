from xml.dom import minidom
import pymysql
import sys, argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--dbuser', help='Database User')
    parser.add_argument('-p', '--dbpassword', help='Database Password')
    parser.add_argument('-s', '--host', help='Database host')
    parser.add_argument('-i', '--inputxml', help='read XML data')
    parser.add_argument('-t', '--targetdb', help='Target Database')
    parser.add_argument('-b', '--targettable', help='Target Table')
    return parser.parse_args()

def get_xml(args):
    input_xml = args.inputxml
    xml_file = open(input_xml, 'r')
    xml = minidom.parse(xml_file)
    xml_file.close()
    return xml

def get_rows(xml):
    rows = xml.documentElement.getElementsByTagName('row')
    return rows

def get_field_name(rows):
    field = rows[0].getElementsByTagName('field')
    a = field[1].attributes["name"]
    field_name = a.value
    return field_name

def get_many_args(rows):
    many_args = []
    for row in rows:
        fields = row.getElementsByTagName('field')
        field_id = int(fields[0].firstChild.nodeValue)
        field_text = fields[1].firstChild.nodeValue
        args = [field_text, field_id]
        many_args.append(args)
    return many_args


def get_db_conn(args):
    target_db = args.targetdb
    db_user = args.dbuser
    db_pass = args.dbpassword
    host = args.host
    db_conn = pymysql.connect(user=db_user, passwd=db_pass, host=host,db=target_db,
                              unix_socket="/tmp/mysql.sock", charset='utf8')
    cursor = db_conn.cursor()
    return cursor


def update_db(db_conn, target_table, field_name, many_args):
    query = ('UPDATE ' + target_table + ' SET ' + 
            field_name + ' = %s WHERE id = %s')
    db_conn.executemany(query, many_args)
    db_conn.execute('COMMIT')
    db_conn.close()

def main():
    args = parse_args()
    xml = get_xml(args)
    rows = get_rows(xml)
    field_name = get_field_name(rows)
    many_args = get_many_args(rows)
    db_conn = get_db_conn(args)
    target_table = args.targettable
    update_db(db_conn, target_table, field_name, many_args)
    db_conn.close()    

if __name__ == "__main__":
    main()