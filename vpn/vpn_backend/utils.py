import requests
import re
from bs4 import BeautifulSoup
from .models import Website
from urllib.parse import urlparse


def replace_internal_links(content, website, user):
    soup = BeautifulSoup(content, 'html.parser')
    for tag in soup.find_all(['a', 'link', 'script'], href=True):
        original_link = tag.get('href') or tag.get('src')
        parsed_link = urlparse(original_link)
        if parsed_link.netloc == urlparse(website.url).netloc:
            if check_for_vpn_use(user, original_link):
                new_link = f'/vpn/{website.url}{parsed_link.path}'
                if tag.has_attr('href'):
                    tag['href'] = new_link

    modified_content = str(soup)
    return modified_content


def check_for_vpn_use(user, user_site_domain):
    try:
        Website.objects.get(user=user, url=user_site_domain)
        print('Found website')
        return True
    except Website.DoesNotExist:
        return True


def make_proxy_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Proxy request failed: {e}")
        return b""