# -*- coding: utf-8 -*-
import os
import re

from bs4 import BeautifulSoup
from urllib import urlopen


class MySoup(object):
    def __init__(self, url, path=False):
        self.base_path = os.path.abspath(os.path.curdir)
        self.page_path = os.path.join(self.base_path, 'pages')

        if not os.path.exists(self.page_path):
            self.create_path(self.page_path)

        file_url = re.sub(r'/', '_', url) + '.html'

        # create path for pages
        if path:
            custom_path = self.create_path(path)
            file_path = os.path.join(custom_path, file_url)
        else:
            file_path = os.path.join(self.page_path, file_url)

        # soup from page
        if os.path.exists(file_path):
            self.soup = BeautifulSoup(open(file_path, 'r'), "html.parser")
        else:
            response = urlopen(url).read().decode('utf-8', 'ignore')
            self.soup = BeautifulSoup(response, "html.parser")
            self.save_page(file_path, self.soup)

    def create_path(self, path):
        c_path = os.path.join(self.page_path, path)
        if not os.path.isdir(path):
            os.makedirs(path)
        return c_path

    @staticmethod
    def mk_dir(directory):
        try:
            os.mkdir(directory, 0o755)
        except OSError as e:
            print(e.errno)
            print(e.filename)
            print(e.strerror)
            exit(0)

    @staticmethod
    def save_page(path_to_file, data):
        with open(path_to_file, 'wb') as f:
            f.write(data.prettify(encoding='utf-8'))

    def save_img(self, path, link):
        if not os.path.isdir(path):
            self.create_path(path)
        filename = self.__path_pages + re.sub(
            '/', '', path) + '/' + re.split('/', link).pop()
        resource = urlopen(link).read()

        with open(filename, 'wb') as f:
            f.write(resource)


# usage  = MySoup('http://url')
