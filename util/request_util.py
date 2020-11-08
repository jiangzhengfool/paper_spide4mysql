import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import os
from util import res_util

__all__ = ['IEEE_search_by_key', 'search_by_key']


def search_by_key(conf, key, site_type):
    return globals()[site_type + '_search_by_key'](conf, key, site_type)


def IEEE_search_by_key(conf, key, site_type):
    headers = conf['headers']
    headers['User-Agent'] = UserAgent().random
    url = conf['url']
    params = conf['params']
    params['queryText'] = key
    params = json.dumps(params)
    r = requests.post(url, data=params, headers=headers)
    doi_new = []
    if r.status_code != 200:
        return False
    print(r.json())

    for rec in r.json()['records']:
        doi = rec.get("doi", None)
        if doi:
            doi_new.append((doi, site_type))

    return doi_new


def acm_search_by_key(conf, key, site_type):
    site_type = 'acm'
    headers = conf['headers']
    headers['User-Agent'] = UserAgent().random
    url = conf['url']
    params = conf['params']
    key.replace(' ', '+')
    params = json.dumps(params)
    try:
        r = requests.post('https://dl.acm.org/action/doSearch?AllField=%s' % key, headers=headers,timeout=10)
    except requests.exceptions.RequestException as e:
        return False
    soup = BeautifulSoup(r.content, 'html.parser')
    doi_new = []

    for link in soup.find_all('a'):
        if link.get('href').startswith('https://doi.org/'):
            doi_new.append(((link.get('href')[16:]), site_type))

    return doi_new


def download_cite_byDOI(doi):
    with open('conf/doi2bib.json', mode='r') as f:
        data = json.load(f)
        url = data['url']
        headers = data['headers']
        headers['User-Agent'] = UserAgent().random
        params = {'id': doi}
        try:
            res = requests.get(url, params, headers=headers,timeout=10)
        except requests.exceptions.RequestException as e:
            return False
        print(res.text)
        title = res_util.get_title(res.text)
        print(title)
        if res.status_code != 200:
            return False
        data = {
            'doi': doi,
            'bib': res.text,
            'title': title[:150]
        }
        return data


def download_pdf_byDOI_sci(doi, filename='demo.pdf'):
    with open('conf/sci_hub.json', mode='r') as f:
        data = json.load(f)
        url = data['url']
        headers = data['headers']
        headers['User-Agent'] = UserAgent().random
        try:
            res = requests.get(url + doi,timeout=10)
        except requests.exceptions.RequestException as e:
            return False
        if res.status_code != 200 or res.text == '':
            return False

        pdf_url = res_util.get_pdf_url(res.text)
        if not pdf_url:
            return False
        # 按照type分别请求
        pdf_flag = download(pdf_url, filename + '.pdf')
        data = {
            'doi': doi,
            'pdf_flag': pdf_flag
        }

        return data


def download(pdf_url, filename):
    try:
        r = requests.get(pdf_url,timeout=10)
    except requests.exceptions.RequestException as e:
        return False
    filepath = os.path.join('pdf', filename.replace("/","#").replace(":"," ").replace("\\",'#'))
    f_pdf = open(filepath, "wb")
    f_pdf.write(r.content)
    f_pdf.close()
    print('文件下载成功')
    return r.status_code == 200


if __name__ == '__main__':
    download_cite_byDOI('10.1109/CIFEr.2012.6327783')
