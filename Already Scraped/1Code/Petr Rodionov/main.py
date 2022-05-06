from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from random import choice
from connect_manager import ConnectManager
import requests
import colorama
from colorama import Fore, Back, Style
import time
import csv
import random
import datetime
import sys
import importlib
import pandas as pd
import html2text
import json



urll = 'http://sitespy.ru/my-ip'
cm = ConnectManager()
colorama.init()
h = html2text.HTML2Text()
h.ignore_links = True


def get_html(url, useragent=None, proxy=None):
    r = None
    while r == None:
        try:
            # print(Fore.WHITE + 'Using proxy: ' + proxy['https'])
            r = requests.get(url, headers=useragent, proxies=proxy, timeout=2)
            html = str(r.text).encode('utf-8').decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            lol = str(soup.find('title').text)
            kek = str(soup.find('h1').text)
            # print('lol: ', lol)
            # print('kek: ', kek)
            if lol == 'Attention Required! | Cloudflare' or lol == 'Validate User' or kek == '403 Forbidden':
                r = None
                print(lol)
                cm.new_identity()
                proxy = cm.proxy
        except:
            # print(Fore.YELLOW + 'Timeout proxy: ' + proxy['https'])
            cm.new_identity()
            proxy = cm.proxy
            r = None
    return html


def get_json(url, useragent=None, proxy=None):
    r = None
    while r == None:
        try:
            # print(Fore.WHITE + 'Using proxy: ' + proxy['https'])
            r = requests.get(url, headers=useragent, proxies=proxy, timeout=2)
            r = r.json()
        except:
            # print(Fore.YELLOW + 'Timeout proxy: ' + proxy['https'])
            cm.new_identity()
            proxy = cm.proxy
            r = None
    return r


def get_issues(volume, number):
    issues = []
    # print(cm.proxy)
    print(f'https://academic.oup.com/qje/issue/{volume}/{number}')
    html = get_html(f'https://academic.oup.com/qje/issue/{volume}/{number}', cm.useragent, cm.proxy)
    # print(html)
    soup = BeautifulSoup(html, 'lxml')
    volume_name = soup.find_all('div', class_='issue-info-pub')
    if len(volume_name) > 0:
        articles = soup.find_all('div', class_='al-article-items')
        for a in articles:
            abstract = a.find('div', class_='abstract-link')
            if abstract:
                title = a.find('h5', class_='customLink item-title')
                id = title['data-resource-id-access']
                title = title.text

                authors = []
                al = a.find_all('span', class_='wi-fullname brand-fg')
                for l in al:
                    authors.append(l.text)

                abstract = get_json(f'https://academic.oup.com/qje/PlatformArticle/ArticleAbstractAjax?articleId={id}&layAbstract=false',
                                    cm.useragent, cm.proxy)

                # print(abstract['Html'])

                authors_dict = {'Author' + str(i + 1): authors[i] for i in range(len(authors))}
                dict_1 = {'Title': title.replace('\n', ''), 'Issue': volume_name[1].text,
                          'Abstract': h.handle(abstract['Html']).replace('\n', ' ').replace('  ', '')}
                dict_1.update(authors_dict)

                print(dict_1)

                issues.append(dict_1)

                time.sleep(random.uniform(5, 10))
    else:
        title = str(soup.find('title').text)
        print(title)
        if title != 'Not Found | The Quarterly Journal of Economics | Oxford Academic':
            print(html)
        else:
            p = 1
            ps_issues = []
            if str(number).find('Part') > 0:
                return []
            while True:
                p_issues = get_issues(volume, number=f'{number}_Part_{p}')
                if len(p_issues) > 0:
                    ps_issues += p_issues
                    p += 1
                else:
                    break
            issues += ps_issues
    return issues


def get_articles_data_from_issue(url):
    html = get_html(url, cm.useragent, cm.proxy)
    soup = BeautifulSoup(html, 'lxml')

    title = soup.find('h1', class_='wi-article-title article-title-main').text
    title = title.replace('                   ', '').replace('\r\n ', '')

    issue = soup.find('div', class_='article-issue-info').find('div', class_='volume trailing-comma').text + ', '
    issue += soup.find('div', class_='article-issue-info').find('div', class_='issue').text + ' | '
    issue += soup.find('div', class_='article-issue-info').find('div', class_='ii-pub-date').text

    issue = issue.replace('\r\n', '').replace('        ', '')

    abstract = soup.find('section', class_='abstract')
    if abstract:
        abstract = h.handle(abstract.find('p', class_='chapter-para').text)
    else:
        abstract = 'None'

    authors = []
    spans = soup.find_all('span', class_='al-author-name-more js-flyout-wrap')
    for s in spans:
        authors.append(s.find('a').text)

    authors_dict = {'Author' + str(i + 1): authors[i] for i in range(len(authors))}
    dict_1 = {'Title': title, 'Issue': issue, 'Abstract': abstract}
    dict_1.update(authors_dict)
    #
    # for d in divs:
    #
    #     if abstract:
    #         title = d.find('h5')
    #         authors = []
    #         spans = d.find_all('span', class_='hlFld-ContribAuthor')
    #         for s in spans:
    #             authors.append(s.text.replace('\xa0', ' ').replace(', and ', '').replace(' and ', '').replace(', ', ''))
    #
    #         authors_dict = {'Author'+str(i+1): authors[i] for i in range(len(authors))}
    #         dict_1 = {'Title': title.text, 'Issue': issue, 'Abstract': abstract.text}
    #         dict_1.update(authors_dict)
    #
    #         articles.append(dict_1)
    # print(dict_1)
    return dict_1


def get_data_from_page(url):
    try:
        data = {}
        html = get_html(url, cm.useragent, cm.proxy)
        soup = BeautifulSoup(html, 'lxml')
        lis = soup.find('div', class_='bc_text').find_all('li')
        for li in lis:
            li = li.text.strip().split(':')
            data.update({li[0].replace('\xa0', ''): li[1].replace('\xa0', '')})
        data.update({'Ссылка': url})
        print(Fore.WHITE + 'Success getting data from page: ' + url)
        return data
    except:
        print(Fore.RED + 'Error getting data from page: ' + url)


def main():
    start_time = datetime.datetime.now()
    issues = []

    number = 1

    for volume in range(54, 0, -1):

        while True:
            cm.new_identity()
            print(Fore.BLUE + f'{datetime.datetime.now() - start_time} | {cm.proxy["https"]} '
                              f'| processing {volume} volume {number} number')
            iss = get_issues(volume, number)
            if len(iss) > 0:
                issues += iss
                number += 1
                df = pd.DataFrame(issues).fillna('')
                df.to_csv('articles.csv', encoding='UTF-16')
            else:
                if number == 1:
                    exit()
                else:
                    break
        number = 1
    print(len(issues))
    exit()

    links = []
    links_before = 0

    with open('issues.txt', 'r') as file:
        lines = file.readlines()
        for l in lines:
            links.append(l.replace('\n', ''))

    articles = []

    cm.new_identity()

    for i in range(len(links)):
        if i < 67:
            continue
        if i % 3 == 0:
            cm.new_identity()


        articles.append(get_articles_data_from_issue(links[i]))
        print(Fore.BLUE + f'{datetime.datetime.now() - start_time} | {cm.proxy["https"]} | processing {i} issue')
        df = pd.DataFrame(articles).fillna('')
        df.to_csv('articles.csv', encoding='UTF-16')


    # with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #     fieldnames = ['Title', 'Issue', 'Abstract', 'Author1', 'Author2', 'Author3', 'Author4', 'Author5', 'Author6',
    #                   'Author7', 'Author8', 'Author9', 'Author10', 'Author11', 'Author12', 'Author13', 'Author14']
    #
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    #     writer.writeheader()
    #     datas = get_articles_data_from_volume(volumes[-1])
    #     for d in datas:
    #         try:
    #             writer.writerow({})
    #         except Exception as e:
    #             print(e)
    #             print(Fore.RED + 'Error writing data:')
    #             print(d)


# with open('data.csv', 'w', newline='') as csvfile:
        # while start_year < 2022:
        #     while start_volume < 130:
        #         while start_number < 11:
        #             cm.new_identity()
        #             print(start_year, start_volume, start_number)
        #             volumes = get_volumes(start_year, start_volume, start_number)
        #             if len(volumes) == 0:
        #                 break
        #             for vol in volumes:
        #                 links.append(vol['href'])
        #             start_number += 1
        #         start_volume += 1
        #     time.sleep(random.uniform(2, 5))
        #     start_year += 1
        # for l in links:
        #     print(l)


            # url = 'https://productcenter.ru/producers/page-'+str(p)+'?sorttype=createdate'
            # lc = 1
            # for l in get_links_from_page(url):
            #     print(Fore.BLUE + str(datetime.datetime.now()) + ' | Processing page: ' + str(p) + ' ' + str(lc)+'/48 | Collected ' + str(ic) + ' items in ' + str(datetime.datetime.now()-start_time))
            #     data = get_data_from_page('https://productcenter.ru'+l)
            #     try:
            #         writer.writerow(data)
            #     except:
            #         print(Fore.RED + 'Error writing data:')
            #         print(data)
            #     lc += 1
            #     ic += 1
            #     if lc == 24:
            #         cm.new_identity()
            #     time.sleep(random.uniform(2,5))
            # p += 1
            # cm.new_identity()

if __name__ == '__main__':
    main()