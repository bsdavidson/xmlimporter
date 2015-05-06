from xml.dom import minidom

from xmlimporter import get_field_name, get_many_args, get_xml_rows


def test_get_field_name():
    rows = get_xml_rows('test.xml')
    field_name = get_field_name(rows)
    assert field_name == "text_test"


def test_get_many_args():
    rows = get_xml_rows('test.xml')
    args = get_many_args(rows)
    assert args == [['Test Text For Testing', 58],
                    ['Another Row For Testing', 78]]


def test_get_xml_rows():
    rows = get_xml_rows('test.xml')
    assert len(rows) == 2
    for row in rows:
        assert isinstance(row, minidom.Element)
