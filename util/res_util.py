#  标题正则
import re


def get_title(s):
    if not s:
        False
    title = re.search(r'title[\s\S]*[,][\n]', s).group()[9:-2]
    return title.replace("/","#").replace(":"," ").replace("\\",'#')


def get_pdf_url(s):
    if not s:
        False
    data = re.search(r'location[.]href[\s\S]*[.]pdf[?][\s\S]*download=true', s)
    if not data:
        return False
    pdf_url = data.group()[15:]
    if not pdf_url.startswith("http"):
        pdf_url = "https:" + pdf_url

    return pdf_url
