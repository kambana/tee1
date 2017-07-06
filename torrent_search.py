import requests
from bs4 import BeautifulSoup
import subprocess


def define_soup_obj(url):
    request_obj = requests.get(url)
    plain_code = request_obj.text
    soup_obj = BeautifulSoup(plain_code, "lxml")
    return soup_obj


def search_page(search_item):
    # generating url for search
    url = "https://proxyspotting.in/s/?q=" + "+".join(search_item.split()) + "&page=1"
    soup_obj = define_soup_obj(url)
    # index for choosing download
    no = 1
    # dictionary of torrents
    torrents = {}
    for links in soup_obj.findAll('td', {'class': 'vertTh'}):
        link = "https://proxyspotting.in" + links.findNext('a', {'class': 'detLink'})['href']
        name = links.findNext('a', {'class': 'detLink'}).string
        desc = links.findNext('td').findNext('font').contents[0][:-10]
        seeds = links.findNext('td').findNext('td').string
        leechers = links.findNext('td').findNext('td').findNext('td').string
        torrents[no] = {'Name': str(name), 'Description': str(desc), 'Seeds': str(seeds), 'Leechers': str(leechers), 'Link': str(link)}
        print("No : " + str(no) + "\nName : " + str(name) + "\nDescription : " + str(desc) + "\nSeeds : " + str(seeds) + "\tLeechers : " + str(leechers) + "\nLink : " + str(link) + "\n")
        # print(torrents[no])
        # print()
        no += 1
    if not bool(torrents):
        print("No Search Results Found. Please try with different search phrase")
        ask_search()
    return torrents


def get_magnet_link(torrent_dict):
    soup_obj = define_soup_obj(torrent_dict['Link'])
    a_tag = soup_obj.find('a', {'title': 'Get this torrent'})
    return a_tag['href']


def download_torrent(torrent_dict, magnet_link):
    print("Downloading : " + torrent_dict['Name'])
    subprocess.call(['xdg-open', magnet_link])


def ask_search():
    search_item = input("What are you looking for : ")
    torrents = search_page(search_item)
    print("\nEnter Your Choice : ")
    while True:
        try:
            choice = int(input())
            break
        except Exception as e:
            raise e
    magnet = get_magnet_link(torrents[choice])
    download_torrent(torrents[choice], magnet)


def main():
    ask_search()


if __name__ == '__main__':
    main()
