from xml.dom import minidom
import pymysql
import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--dbuser', help='Database User')
parser.add_argument('-p', '--dbpassword', help='Database Password')
parser.add_argument('-s', '--host', help='Database host')
parser.add_argument('-i', '--inputxml', help='read XML data')
parser.add_argument('-t', '--targetdb', help='Target Database')
parser.add_argument('-b', '--targettable', help='Target Table')
args = parser.parse_args()
input_xml = args.inputxml
target_db = args.targetdb
target_table = args.targettable
db_user = args.dbuser
db_pass = args.dbpassword
host = args.host

xml_file = open(input_xml, 'r')
xml = minidom.parse(xml_file)
xml_file.close()
db_conn = pymysql.connect(user=db_user, passwd=db_pass, host=host,db=target_db,
                          unix_socket="/tmp/mysql.sock", charset='utf8')
cursor = db_conn.cursor()
rows = xml.documentElement.getElementsByTagName('row')


def get_field_name(rowz):
    field = rowz[0].getElementsByTagName('field')
    a = field[1].attributes["name"]
    field_name = a.value
    return field_name
field_name = get_field_name(rows)

many_args = []
for row in rows:
    fields = row.getElementsByTagName('field')
    field_id = int(fields[0].firstChild.nodeValue)
    field_text = fields[1].firstChild.nodeValue
    args = [field_text, field_id]
    many_args.append(args)

query = ('UPDATE ' + target_table + ' SET ' + 
        field_name + ' = %s WHERE id = %s')
cursor.executemany(query, many_args)
cursor.execute('COMMIT')
cursor.close()
db_conn.close()