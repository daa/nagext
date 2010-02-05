#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib2
import re, htmlentitydefs

def unescape(text):
	"""
	Removes HTML or XML character references 
	and entities from a text string.
	keep &amp;, &gt;, &lt; in the source code.
	from Fredrik Lundh
	http://effbot.org/zone/re-sub.htm#unescape-html
	slightly modified
	"""
	def fixup(m):
		text = m.group(0)
		if text[:2] == "&#":
			# character reference
			try:
				if text[:3] == "&#x":
					return unichr(int(text[3:-1], 16))
				else:
					return unichr(int(text[2:-1]))
			except ValueError:
				#print "erreur de valeur"
				pass
		else:
			# named entity
			try:
				#print text[1:-1]
				text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
			except KeyError:
				#print "keyerror"
				pass
		return text # leave as is
	return re.sub("&#?\w+;", fixup, text)

def wrap(txt, cols=80):
	"""
	wraps txt (line of text) at cols columns
	"""
	word = ''
	col = 0
	line = ''
	char = ''
	if txt[-1] == "\n":
		txt2 = txt[0:-1]
	else:
		txt2 = txt
	for char in txt2:
		if not char.isspace():
			word += char
		else:
			if word:
				if col + len(word) <= cols or not line:
					line += word
					col += len(word)
				else:
					line = line.rstrip() + "\n" + word
					col = len(word)
				word = ""
			if char != '\n':
				line += char
				col += 1
			elif line[-1] != ' ':
				line += ' '
				col += 1
	if word:
		if col + len(word) < cols:
			line += word
		else:
			line = line.rstrip() + "\n" + word
	if txt[-1] == '\n':
		line += "\n" 
	return line

def cmd2py(cmd, descr):
	cmd = cmd.strip().replace('<', '').replace('>', '')
	descr = descr.strip()
	c = cmd.split(';')
	name = c[0].lower()
	args = ', '.join(c[1:])
	method = "\tdef %s(self, %s):\n" % (name, args) + \
		'\t\t"""\n' + \
		'\t\t%s\n' % wrap(descr) + \
		'\t\t"""\n' + \
		"\t\tself.run('%s', %s)\n" % (c[0], args)
	return method

if __name__ == '__main__':
	root_url = 'http://old.nagios.org/developerinfo/externalcommands/'

	f = urllib2.urlopen(root_url + 'commandlist.php')

	soup = BeautifulSoup(f.read())

	f.close()

	content_table = soup.find('table', { 'class' : 'Content' })
	hrefs = content_table.findAll('a')[4:]

	for a in hrefs:
		#print a['href']
		#print a.string
		f = urllib2.urlopen(root_url + a['href'])
		s = BeautifulSoup(f.read())
		t = s.find('table', { 'class': 'Content' })
		tds = t.findAll('td')
		p = False
		cmd = ''
		descr = ''
		set_cmd = set_descr = False
		for td in tds:
			if set_cmd:
				cmd = unescape(td.string.decode())
				set_cmd = False
			elif set_descr:
				descr = unescape(td.string.decode())
				set_descr = False
			if td.string == 'Command Format:':
				set_cmd = True
			elif td.string == 'Description:':
				set_descr = True
			if cmd and descr:
				break
		if cmd and descr:
			print cmd2py(cmd, descr)
		f.close()

