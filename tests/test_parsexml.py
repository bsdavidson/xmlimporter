from xml.dom import minidom
from parsexml import get_rows, get_xml, get_many_args, get_field_name


def test_xml_file():
    xml = get_xml('test.xml')


def test_xml_rows():
    xml_data = get_xml('test.xml')
    rows = get_rows(xml_data)
    assert len(rows) == 2
    for row in rows:
        assert isinstance(row, minidom.Element)

def test_get_fieldname():
    xml_data = get_xml('test.xml')
    rows = get_rows(xml_data)
    field_name = get_field_name(rows)
    assert field_name == "text_test"


def test_get_args():
    xml_data = get_xml('test.xml')
    rows = get_rows(xml_data)
    args = get_many_args(rows)
    assert args == [['Test Text For Testing', 58],
                    ['Another Row For Testing', 78]]
