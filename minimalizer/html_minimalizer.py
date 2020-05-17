import re


def squeeze(html_text) :
    res = re.sub(r' +', ' ', html_text)
    return re.sub(r'[\n\t]+', '', res)
