#!/usr/bin/python

import time
import pycurl
import cStringIO
import bs4


def getLinks(page_soup):

	text = []
	links = []

	for link in page_soup.find_all('a'):
    		links.append(link.get('href'))
		text.append(link.get_text())

	return links, text

def explore(url):

	file = open("vistited_links.dat","a")

	buf = cStringIO.StringIO()

	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.CONNECTTIMEOUT, 5)
	c.setopt(c.TIMEOUT, 20)
	c.setopt(c.FAILONERROR, True)
	c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
	c.setopt(c.WRITEFUNCTION, buf.write)
	try:
    		c.perform()
	except pycurl.error, error:
    		errno, errstr = error
    		print 'An error occurred: ', errstr

	c.close()

	response = buf.getvalue()
	buf.close()

	print response

	soup = bs4.BeautifulSoup(response)
	data = getLinks(soup)
	links = data[0]
	text = data[1]

	#for link in links:
	#	if link != None:
	#		print link
	#		file.write(link+"\n")
	#		explore(link)

			#if cont[len(cont)-1] == "/":
			#	urlnew = url + cont
			#	print urlnew
			#	explore(urlnew)
			#else:
			#	temp = cont.split(".")
			#	if temp[len(temp) - 1] == "jpg":
			#		urlImg = url+cont
			#		print urlImg
			#		img = urllib2.urlopen(urlImg)
			#		f = open(cont,"wb")
			#		f.write(img.read())
			#		f.close()

def main():
	print "Start rolling..."

	baseAddress = "http://en.wikipedia.org/wiki/Main_Page"

	explore(baseAddress)	


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "Force stop"
