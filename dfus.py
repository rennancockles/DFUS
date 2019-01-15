# -*- coding: utf-8 -*-

import requests
import tldextract
import re
import sys


class DFUS(object):
    DOMAIN = ""
    NODES = dict()

    def __init__(self, main_url):
        if main_url == '':
            sys.exit(1)

        self.DOMAIN = self.get_domain(main_url)
        self.NODES[main_url] = 'white'

        self.dfus(main_url)

        if all(map(lambda v: v == 'black', self.NODES.values())):
            urls = list(self.NODES.keys())
            urls.sort()
            out = '\n'.join(urls)

            print('All nodes visited!')
            print('Total of %d nodes obtained!' % len(self.NODES))

            with open('dfus.txt', 'w') as f:
                f.write('Domain: %s \n\n' % self.DOMAIN)
                f.write(out)

    def find_neighbor_urls(self, url):
        regex = r"\bhttp[s]?://(?:\w*\.)*%s(?:/[^\s\'\"<>]*)*\b" % self.DOMAIN

        if not url.startswith('http'):
            url = 'http://' + url

        try:
            r = requests.get(url)
            if r.ok:
                matches = re.findall(regex, r.text)
                return list(set(matches))
            else:
                print("Not OK for url: %s" % url)
                return []

        except requests.exceptions.ConnectionError:
            return []

    def create_nodes(self, urls):
        for url in urls:
            if self.get_domain(url) == self.DOMAIN and not self.NODES.get(url, None):
                self.NODES[url] = 'white'

    def dfus(self, url):
        neighbor_urls = self.find_neighbor_urls(url)
        self.create_nodes(neighbor_urls)

        node_status = self.NODES.get(url, None)
        if not node_status or node_status == 'white':
            self.NODES[url] = 'gray'

        for neighbor_url in neighbor_urls:
            if self.NODES.get(neighbor_url, "") == 'white':
                self.dfus(neighbor_url)

        self.NODES[url] = 'black'

    @staticmethod
    def get_domain(url):
        return tldextract.extract(url).registered_domain


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Missing <initial_url> parameter!!")
        print("Usage: python dfus.py <initial_url>")
        sys.exit(1)

    DFUS(sys.argv[1])
