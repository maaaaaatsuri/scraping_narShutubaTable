import urllib.request as req
from bs4 import BeautifulSoup
import re
from utils import Utils
from typing import *


class VenueCodeCreator():
    def fetch_venue_dict(self):
        url = "https://nar.netkeiba.com/racecourse/racecourse_list.html?rf=sidemenu"
        response = req.urlopen(url)
        parse_html = BeautifulSoup(response, "html.parser")
        tags_a = parse_html.find_all('a')

        venue_text = []
        venue_code = []
        for a in tags_a[21:36]:
            text = a.text
            href = a.attrs['href']
            href = re.findall("[0-9]+", str(href))
            venue_text.append(text.replace('\n', ''))
            venue_code.append(href)

        venue_code = list(Utils.flatten_2d(venue_code))

        venue_code_int = [int(i) for i in venue_code]
        venue_dict = dict(zip(venue_text, venue_code_int))
        return venue_dict