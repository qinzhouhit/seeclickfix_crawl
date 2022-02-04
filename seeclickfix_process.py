#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 17:03:48 2020
@author: Zhou
""" 

import requests
import urllib
import json
import shutil
import time
from bs4 import BeautifulSoup

def issues_crawl():
	"""
	# TODO: crawl the issues first,
	entry example:
	{"id": 8934715,
	"status": "Open",
	"summary": "Animal Complaint",
	"description": "PLease inspect Animal Training facility mistreating animals, cages are to small.",
	"lat": 40.7229781057267,
	"lng": -74.1427038348732,
	"address": "200 Avenue L Newark, NJ, 07105, USA",
	"created_at": "2020-11-18T11:45:21-05:00",
	"acknowledged_at": null,
	"closed_at": null,pip3 install requests
	"url": "https://seeclickfix.com/api/v2/issues/8934715",
	"media": {
		"video_url": null,
		"image_full": null,
		"image_square_100x100": null,
		"representative_image_url": "https://seeclickfix.com/assets/categories_trans/no-image-af3faf07f478451d4ca455f92af96dd763f686e943607309ed059ef4fe13be21.png"}
	"""
	# 1) One can find the url below via web inspector & by path
	# 2) Each page shows 20 issues, there is a request limit!!! Do 20 pages each time! one can add a timer to control
	for page_num in range(21, 301):
		# url = "https://seeclickfix.com/api/v2/issues?page=" + str(page_num) # for all US data
		url = "https://seeclickfix.com/api/v2/issues?min_lat=40.650439623283525&min_lng=-74.52987670898439&max_lat=40.83044709712594&max_lng=-73.75877380371095&status=open%2Cacknowledged%2Cclosed%2Carchived&fields%5Bissue%5D=id%2Csummary%2Cdescription%2Cstatus%2Clat%2Clng%2Caddress%2Cmedia%2Ccreated_at%2Cacknowledged_at%2Cclosed_at&page=" + str(page_num)
	# 	path = urllib.parse.urlparse(url).path
	# 	r = requests.get(url, allow_redirects=True)
	# 	print (r.content)
		time.sleep(20)
		response = urllib.request.urlopen(url)
		data = json.loads(response.read())
		print (f"Crawling page {page_num} now.")
		json.dump(data, open("./issues/issue_entry" + str(page_num) + ".json", "w"))


def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match


def entry_comments_helper(url):
	"""
	crawl comments
	"""
	
	# url = "https://seeclickfix.com/issues/8936511"
	html = urllib.request.urlopen(url).read()
	text = BeautifulSoup(html, "html.parser")
	res = []
	# print (text.find("div", {"id": "comments"}))
	# print (text.find("div", {"class": "expandable"}))
	# print (text.findAll(match_class("expandable")))
	comments = text.findAll("div", class_="expandable")
	for comment in comments:
		parts = comment.text.split("\n")
		for part in parts:
			if part:
				tmp = part.strip()
				res.append(tmp)
	while '' in res:
		res.remove('')
	return res


def entry_comments():
	"""
	crawl the comments of each entry
	"""
	
	import collections
	# page_num = 1 # use issue_entry1.json as example
	for page_num in range(21, 301):
		data = json.load(open("./issues/issue_entry" + str(page_num) + ".json"))
		id_comments = collections.defaultdict(list)
		for entry in data['issues']:
			id = ""; comments = []; url = ""
			for k, v in entry.items():
				if k == "id":
					print (f"Processing id {v}.")
					id = v
				if k == "url":
					url = v
					new_url = url.replace("api/v2/", "") # url with comments
					comments = entry_comments_helper(new_url)
			id_comments[id] = comments
		json.dump(id_comments, open("./issues_comments/issue_entry" + str(page_num) + "_id_comments.json", "w"))


def entry_peek():
	"""
	data peek, better understand each entry
	# one can do any post-processing based on this
	# notice that one has to filter by NJ since there are data across US.
	"""
	
	data = json.load(open("issue_entry1.json"))
	for entry in data['issues']:
		for k, v in entry.items():
			# k will be features like lng, lat, time, etc
			# v will be corresponding values
			print (k, v)


if __name__ == "__main__":
	# issues_crawl()
	entry_comments()
	# entry_peek()
