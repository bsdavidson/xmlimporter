import argparse
import os
from xml.dom import minidom

import pymysql

from ._version import __version__  # noqa -- flake8 should ignore this line


def get_xml_rows(xml_filename):
    """Return the row elements from the given XML file.

    :param str xml_filename: File to parse.
    :returns: list of xml.dom.minidom.Element
    """
    if not os.path.exists(xml_filename):
        raise ValueError('XML file {!r} does not exist'.format(xml_filename))
    with open(xml_filename, 'r') as xml_file:
        xml = minidom.parse(xml_file)
        return xml.documentElement.getElementsByTagName('row')


def get_field_name(xml_rows):
    """Return the "name" property from one of the rows.

    :param list xml_rows: A list of row XML elements.
    :returns: str
    """
    field = xml_rows[0].getElementsByTagName('field')
    return field[1].attributes['name'].value


def get_many_args(xml_rows):
    """Transform the given XML rows into args to be inserted into the database.

    :param list xml_rows: A list of row XML elements.
    :returns: list of tuples to be passed to update_db.
    """
    many_args = []
    for row in xml_rows:
        fields = row.getElementsByTagName('field')
        field_id = int(fields[0].firstChild.nodeValue)
        field_text = fields[1].firstChild.nodeValue
        many_args.append([field_text, field_id])
    return many_args


def get_db_conn(target_db, db_user, db_pass, host):
    """Connect to a MySQL database,

    :param str target_db: Name of the database.
    :param str db_user: Database username.
    :param str db_pass: Database password.
    :param str host: Database host.
    :returns: pymysql.Connection
    """
    db_conn = pymysql.connect(user=db_user, passwd=db_pass, host=host,
                              db=target_db, unix_socket='/tmp/mysql.sock',
                              charset='utf8')
    cursor = db_conn.cursor()
    return cursor


def update_db(db_conn, target_table, field_name, many_args):
    """Update the given database table with arguments parsed from XML.

    :param pymysql.Connection db_conn: Database connection.
    :param str target_table: Table to update.
    :param str field_name: Field to update.
    :param list many_args: List of tuples, where each tuple is a field value
        and row ID to update.
    """
    query = 'UPDATE {table} SET {field} = %s WHERE id = %s'.format(
        table=target_table, field=field_name)
    db_conn.executemany(query, many_args)
    db_conn.execute('COMMIT')
    db_conn.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--db-user', help='Database username')
    parser.add_argument('-p', '--db-password', help='Database password')
    parser.add_argument('-s', '--host', help='Database host to connect to')
    parser.add_argument('-t', '--target-db', help='Database to update')
    parser.add_argument('-b', '--target-table', help='Table to update')
    parser.add_argument('input_xml_filename', help='XML file to read')
    return parser.parse_args()


def main():
    args = parse_args()
    xml_rows = get_xml_rows(args.input_xml_filename)
    field_name = get_field_name(xml_rows)
    many_args = get_many_args(xml_rows)
    db_conn = get_db_conn(args.target_db, args.db_user, args.db_password,
                          args.host)
    update_db(db_conn, args.target_table, field_name, many_args)
    db_conn.close()


if __name__ == "__main__":
    main()
