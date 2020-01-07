_xml_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}


def _xml_escape(text):
    L = []
    for c in text:
        L.append(_xml_escape_table.get(c, c))
    return "".join(L)


def _xml_unescape(s):
    rules = _xml_escape_table.items()

    for x, y in rules:
        s = s.replace(y, x)

    return s
