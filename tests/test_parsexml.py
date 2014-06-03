def test_xml_file():
    xml = get_xml('test.xml')


def test_xml_rows():
    xml_data = get_xml('test.xml')
    rows = get_rows(xml_data)
    assert len(rows) == 2
