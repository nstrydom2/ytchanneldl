import requests
import lxml
import urllib
import json
import re

from pytube import YouTube
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from driver import Driver


def download_link(title, youtube_link, output_path):
    youtube = YouTube(youtube_link)
    vid = youtube.streams.get_highest_resolution()

    try:
        vid.download(output_path=output_path, filename=title)
    except Exception as ex:
        print(f'[*] Error -- {str(ex)}')


def get_video_links(channel_link):
    youtube_baseurl = 'https://www.youtube.com'

    links = {}

    driver = Driver()
    try:
        driver.open_url(channel_link)
        driver.wait(10)
        scroll_to_bottom(driver.web_driver)

        soup = BeautifulSoup(driver.web_driver.page_source, 'html.parser')
        a_tags = soup.find_all('a', {'id': 'video-title'})

        for tag in a_tags:
            try:
                title = ''.join(e for e in tag.text if e.isalnum() or e in (' ', '-', '_'))
                links[title] = youtube_baseurl + tag.attrs['href']
            except Exception:
                print('[*] Unknown link found and discarded')
    finally:
        driver.close()

    return links


def scroll_to_bottom(driver):
    # Get scroll height
    last_height = driver.execute_script("return window.pageYOffset")

    count = 0
    while True:
        # Scroll down to bottom
        body = driver.find_element_by_tag_name('body')
        body.send_keys(Keys.PAGE_DOWN)

        __import__('time').sleep(0.5)

        new_height = driver.execute_script("return window.pageYOffset")

        if new_height == last_height:
            break

        last_height = new_height


def main():
	to_download = {
		'InsiderPhD': 'https://www.youtube.com/c/InsiderPhD/videos',
		'Stok': 'https://www.youtube.com/c/STOKfredrik/videos',
		'Mr. Turvey': 'https://www.youtube.com/c/MrTurvey/videos',
		'Farah Hawa': 'https://www.youtube.com/c/FarahHawa/videos',
		'Nahamsec' : 'https://www.youtube.com/c/Nahamsec/videos',
		'The Cyber Mentor': 'https://www.youtube.com/c/TheCyberMentor/videos',
		'John Hammond': 'https://www.youtube.com/c/JohnHammond010/videos'
	}

	for name, url in to_download.items():
		print(f'[*] Scraping video links from the channel -- {name}')
		channel_link = url
		output_path = rf'H:\{name}'

		vids = get_video_links(channel_link)
		for title, link in vids.items():
			download_link(title, link, output_path)
			__import__('time').sleep(2.5)

main()

