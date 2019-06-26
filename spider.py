import re
from bs4 import BeautifulSoup
import time
import urllib.request

import config as conf


class MySpider:

    def __init__(self, base_url=conf.BASE_URL, header=conf.FAKE_HEADER, start_page=5):
        self.base_url = base_url
        self.start_page = start_page
        self.headers = header

    def fetch_book_name_list(self):
        while self.start_page < 6:
            try:
                req = urllib.request.Request(
                    self.base_url + '/index_{}'.format(self.start_page)+'.shtml', headers=self.headers)
                #req = urllib.request.Request(
                #    self.base_url + '/index_1.shtml', headers=self.headers)

                html = urllib.request.urlopen(req)
                doc = html.read().decode('utf8')
                soup = BeautifulSoup(doc,'lxml')
                #print(soup.prettify())
                links = []
                names = []

                for link in soup.find_all('a'):
                    links.append(link.get('href'))
                    names.append(link.get('title'))


                alist = []
                aname = []
                for i in range(len(links)):
                    if(links[i] is not None):
                        if (re.search('shtml', links[i]) is not None) :
                            alist.append(links[i])
                            names[i] = names[i].replace('/', '_')
                            aname.append(names[i])

######################################################################
                for i in range(len(alist)):
                    req = urllib.request.Request(self.base_url + alist[i][1:], headers=self.headers)
                    html = urllib.request.urlopen(req)
                    doc = html.read().decode('utf8')

                    soup = BeautifulSoup(doc,'lxml')

                    urls = []
                    url=''
                    for link in soup.find_all('a'):
                        urls.append(link.get('href'))
                        urls.append(link.get('oldsrc'))

                    for item in range(len(urls)):
                        if (urls[item] is not None):
                            if (re.search('pdf', urls[item]) is not None):
                                url = urls[item]

                    turl = ''
                    splist = alist[i].split('/')
                    for j in range(len(splist)-2):
                        turl += '/' + splist[j+1]
                    aurl = self.base_url + turl +'/'+ url
                    print(alist[i])
                    print(url)
                    print(aurl)
                    print(aname[i])

                    if(aurl is not None):
                        self.savepdf(aurl, aname[i])
                   # print(url)
                    #time.sleep(10)





                print('\npage {}\n'.format(self.start_page))
                time.sleep(1)
                self.start_page += 1
                #self.fetch_download_link(alist)
            except urllib.error.HTTPError as err:
                print(err.msg)
                break

    def fetch_download_link(self, alist):
        fres = open('result.txt', 'a')
        for item in alist:
            req = urllib.request.Request(item,headers=self.headers)
            html = urllib.request.urlopen(req)
            doc = html.read().decode('utf8')
            try:
                url = re.findall(conf.DOWNLOAD_LINK_PATTERN, doc)[0] # 从书的详情页面中，找到下载链接
                print('{}'.format(url))
                fres.write(url + '\n')


            except IndexError:
                ferr = open('error.txt', 'a')
                ferr.write(item + '\n')
                ferr.close
            time.sleep(3)
        fres.close()

    def run(self):
        self.fetch_book_name_list()

    def savepdf(self, url, pdfname):
        file_name = pdfname #url.split('/')[-1]
        u = urllib.request.urlopen(url)
        f = open(file_name, 'wb')
        block_sz = 8192

        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)

        f.close()
        print("Sucessful to download" + " " + file_name)





if __name__ == '__main__':
    mc = MySpider()
    mc.run()
