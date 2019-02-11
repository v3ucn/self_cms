
import types

def unicode2utf8(text):
    if isinstance(text, types.UnicodeType):
        return text.encode('utf-8')
    else:
        return text


def utf82unicode(text):
    if isinstance(text, types.StringType):
        return text.decode('utf-8')
    else:
        return text