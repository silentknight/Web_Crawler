#!/usr/bin/python

import time
from HTMLParser import HTMLParser
import pycurl
import cStringIO
import bs4

class MyHTMLParser(HTMLParser):

	def __init__(self):
    		HTMLParser.__init__(self)
    		self.recording = 0 
    		self.data = []
		self.links = []

  	def handle_starttag(self, tag, attrs):
    		if tag == 'a':
          		self.recording = 1

			for attr in attrs:
				if attr[0] == "href":
            				self.links.append(attr[1])

  	def handle_endtag(self, tag):
    		if tag == 'a':
      			self.recording -=1 

  	def handle_data(self, data):
    		if self.recording:
      			self.data.append(data)

def explore(url):

	parser = MyHTMLParser()
 
	buf = cStringIO.StringIO()

	c = pycurl.Curl()
	c.setopt(c.URL, 'en.wikipedia.org/wiki/Main_Page')
	c.setopt(c.CONNECTTIMEOUT, 5)
	c.setopt(c.TIMEOUT, 20)
	c.setopt(c.FAILONERROR, True)
	c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
	#c.setopt(c.VERBOSE, True)
	c.setopt(c.WRITEFUNCTION, buf.write)
	try:
    		c.perform()
	except pycurl.error, error:
    		errno, errstr = error
    		print 'An error occurred: ', errstr

	c.close()

	response = buf.getvalue()
	buf.close()

	parser.feed(response)

	print len(parser.data)
	print parser.data
	print len(parser.links)
	print parser.links

	#for cont in parser.data:
	#	cont = cont.strip()
		
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

	baseAddress = "http://www.linuxquestions.org/"

	explore(baseAddress)	


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "Force stop"
