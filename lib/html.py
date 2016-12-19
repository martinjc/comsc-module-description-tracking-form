from html.parser import HTMLParser

#
# Some simple code for parsing HTML I stole from
# http://stackoverflow.com/questions/11061058/using-htmlparser-in-python-3-2
#
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    """
    Remove all tags from HTML and return the
    text contents
    """
    s = MLStripper()
    s.feed(html)
    data = s.get_data()
    lines = data.split('\n')
    data = ''
    # don't include any empty lines
    for line in lines:
        if line.strip():
            data += '%s\n' % line
    return data
