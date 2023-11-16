import requests
import re
from bs4 import BeautifulSoup
from .models import Website
from urllib.parse import urlparse


def is_common_web_format(path):
    common_formats = ['.php', '.svg', '.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.pdf']
    return any(path.endswith(format) for format in common_formats)


def is_special_link(path):
    special_chars=['?', '#']
    return path[0] in special_chars


def is_full_url(path):
    return "https://" in path


def check_for_vpn_use(user, user_site_domain):
    try:
        Website.objects.get(user=user, url=user_site_domain)
        print('Found website')
        return True
    except Website.DoesNotExist:
        return False


def replace_internal_links(content, user, website_domain, sub_url):
    soup = BeautifulSoup(content, 'html.parser')
    for tag in soup.find_all(['a'], href=True):
        original_link = tag.get('href')
        parsed_link = urlparse(original_link)
        if not original_link:
            continue
        if parsed_link.netloc == urlparse(f'https://{website_domain}').netloc or not is_full_url(original_link):
            if check_for_vpn_use(user, parsed_link) or is_common_web_format(original_link) or not is_full_url(original_link):
                
                if not is_full_url(original_link):
                    new_link = f'/vpn/{website_domain}{original_link}'
                    if is_special_link(original_link):
                        new_link = f'/vpn/{website_domain}{sub_url}{original_link}'
                else:   
                    new_link = original_link
                if tag.has_attr('href'):
                    tag['href'] = new_link
                elif tag.has_attr('src'):
                    tag['src'] = new_link

    modified_content = str(soup)
    return modified_content


def make_proxy_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Proxy request failed: {e}")
        return b""
