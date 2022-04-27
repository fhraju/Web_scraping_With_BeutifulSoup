import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

download_directory = 'downloaded'
base_url = 'https://pythonscraping.com'

def getAbsoluteUrl(base_url, source):
    if source.startswith('http://www.'):
        url = 'http://{}'.format(source[11:])
    elif source.startswith('http://'):
        url = source
    elif source.startswith('www.'):
        url = source[4:]
        url = 'http://{}'.format(source)
    else:
        url = '{}/{}'.format(base_url, source)
    if base_url not in url:
        return None
    return url

def getDownloadPath(base_url, absolute_url, download_dir):
    path = absolute_url.replace('www.', '')
    path = path.replace(base_url, '')
    path = download_dir + path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return path

html = urlopen('https://pythonscraping.com')
bs = BeautifulSoup(html, 'html.parser')
download_list = bs.find_all(src=True)

for download in download_list:
    file_url = getAbsoluteUrl(base_url, download['src'])
    if file_url is not None:
        print(file_url)

urlretrieve(file_url, getDownloadPath(base_url, file_url, download_directory))