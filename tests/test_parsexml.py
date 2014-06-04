from parsexml import get_rows, get_xml, get_many_args


def test_xml_file():
    xml = get_xml('test.xml')


def test_xml_rows():
    xml_data = get_xml('test.xml')
    rows = get_rows(xml_data)
    assert len(rows) == 2


def get_field_name(rows):
    field = rows[0].getElementsByTagName('field')
    a = field[1].attributes["name"]
    field_name = a.value
    return field_name


def test_get_fieldnames():
    xml_data = get_xml('test.xml')
    rows = get_rows(xml_data)
    field_name = get_field_name(rows)
    assert field_name == "text_test"


def test_get_args():
    xml_data = get_xml('test.xml')
    rows = get_rows(xml_data)
    args = get_many_args(rows)
    assert len(args) == 2

    