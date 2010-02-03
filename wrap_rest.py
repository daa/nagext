#!/usr/bin/python
"""
wrap restructured text

usage:
	wrap_rest.py [cols] [--lines l0 l1] [--python]

cols for number of columns (default 72)

--lines l0 l1     wrap between lines l0 and l1
--python          wrap only lines which are python docstrings
                  or comments beginning with '# '
"""

import re, sys


class Wrapper:
	"""
	class to wrap lines to cols (default 72) or not to wrap
	"""

	def __init__(self, cols=72):
		self.cols = cols
		self.out_list = [] 
	
	def wrap(self, txt, ind='', first_ind=''):
		"""
		wraps txt (line of text) at cols columns
		"""
		word = ''
		col = len(first_ind)
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
					if col + len(word) <= self.cols or not line:
						line += word
						col += len(word)
					else:
						line = line.rstrip() + "\n" + ind + word
						col = len(ind + word)
					word = ""
				if char != '\n':
					line += char
					col += 1
				elif line[-1] != ' ':
					line += ' '
					col += 1
		if word:
			if col + len(word) < self.cols:
				line += word
			else:
				line = line.rstrip() + "\n" + ind + word
		if txt[-1] == '\n':
			line += "\n" 
		self.out_list.append(line)
		return line

	def nowrap(self, txt, ind=''):
		"""
		get lines of text (txt) and return them as string
		without changing
		"""
		line = ''
		line0 = ''
		for char in txt:
			if char != "\n":
				line0 += char
			elif line0:
				if line:
					line += ind + line0 + char
				else:
					line = line0 + char
				line0 = ''
			else:
				line += "\n"
		if line0:
			line += line0
		self.out_list.append(line)
		return line

class ParseWarning(Exception):
	"""
	Exception raised on bad formatting
	"""
	def __init__(self, msg, pos):
		Exception.__init__(self)
		self.msg = msg
		self.pos = pos
	
	def print_error(self):
		"""
		print error message to stderr
		"""
		sys.stderr.write("%s at %d\n" % (self.msg, self.pos))

def history(func):
	"""
	history decorator
	"""
	def histfunc(self, *args, **kw):
		"""
		save current position and run given function
		"""
		self.hist_pos.append((self.pos, self.line_pos))
		return func(self, *args, **kw)
	return histfunc

class Parser:
	"""
	Parser class to parse restructured text and wrap it
	to cols (default is specified in Wrapper class)
	"""
	indent_re = \
		re.compile('^(\s*)')
	opt_re = \
		re.compile(
			'^((--|-|/)[a-zA-Z][a-zA-Z0-9_\-=]*|<[^>]+>)(\s[^\s]+)*(  |$)')
	list_seq = \
		'([0-9]+|[a-z]|[A-Z]|[ivxlc]+|[IVXLC]+|#)'
	list_re = \
		 re.compile('^(%s\.|%s\)|\(%s\)|\-|\+|\*) ' % tuple([list_seq]*3))
	grid_sep_re = \
		re.compile('^\+(-|=)+')
	simple_table_re = \
		re.compile('^={2,}')
	transition_re = \
		re.compile('^-{4,}\n?')
	title_re = \
		re.compile("^([!\"#$%&'()*+,-./:;<=>?@\[\]\\\^_`{|}~])\\1{3,}\n?$")
	directive_re = \
		re.compile('^(\.\. .+::[ \t]*)[^\s]')
	quoted_literal_re = \
		re.compile('^([!"#$%&\'()\*\+,-\./:;<=>?@[\]^_`{|}~])\\1* ')
	line_block_re = \
		re.compile('^\|( \s*|$)')
	footnote_re = \
		re.compile('^\.\. \[[^\]]+\] ')

	

	def __init__(self, cols=None):
		if cols:
			self.wrapper = Wrapper(cols)
		else:
			self.wrapper = Wrapper()
		self.line = None
		self.lines = []
		self.pos = 0
		self.line_pos = 0
		self.hist_pos = []
	
	def parse(self, lines, ind='', first_ind=''):
		"""
		parse and wrap lines
		"""
		self.wrapper.out_list = []
		self.lines = lines
		self.pos = -1
		self.line_pos = 0
		self.hist_pos = []
		self.newline()
		while self.line.isspace():
			self.wrapper.nowrap(self.line)
			self.newline()
		try:
			self.body(ind, first_ind)
		except ParseWarning, pwe:
			pwe.print_error()
		return self.wrapper.out_list
	
	def prevline(self):
		"""
		return previous line
		"""
		try:
			return self.lines[self.pos-1]
		except IndexError:
			return None
	def nextline(self):
		"""
		return next line to proceed
		"""
		try:
			return self.lines[self.pos+1]
		except IndexError:
			return None

	def oldpos(self):
		"""
		rollback one position change (next line or remove indent)
		"""
		try:
			self.pos, self.line_pos = self.hist_pos.pop()
			self.line = self.lines[self.pos][self.line_pos:]
		except IndexError:
			self.line = None
		return self.line

	@history
	def newline(self):
		"""
		_newline with history decoration
		"""
		self._newline()

	def _newline(self):
		"""
		move to next line to proceed
		"""
		self.pos += 1
		self.line_pos = 0
		try:
			self.line = self.lines[self.pos]
		except IndexError:
			self.line = None
		return self.line

	@history
	def remove_indent(self, ind=None):
		"""
		remove indent from line
		"""
		if ind is None:
			ind = self.indent()
		self.line_pos += len(ind)
		self.line = self.line[len(ind):]

	def indent(self, line=None):
		"""
		return indentation of line
		"""
		if line is None:
			line = self.line
		return self.indent_re.findall(line)[0]

	def continue_indent(self, elem, ind):
		"""
		continue elem function if indentaion of line
		coincides with given ind
		"""
		if self.line and not self.line.isspace():
			if self.indent() >= ind:
				self.remove_indent(ind)
				self.wrapper.nowrap(ind)
				elem(ind)
			else:
				if self.prevline() and self.prevline().isspace():
					self.oldpos()
		return False

	def body(self, ind='', first_ind=None):
		"""
		sequence of elements divided by blank lines
		"""
		if first_ind is None or first_ind < ind:
			first_ind = ind
		correct = self.element(ind, first_ind)
		while self.line and self.line.isspace():
			blanks = self.blank()
			if self.line:
				if self.indent() >= ind:
					self.wrapper.nowrap(blanks)
					self.remove_indent(ind)
					self.wrapper.nowrap(ind)
					self.element(ind, first_ind)
				else:
					if self.prevline() and self.prevline().isspace():
						self.oldpos()
					break
			else:
				self.wrapper.nowrap(blanks)
		return correct

	@history
	def blank(self):
		"""
		skip blank lines
		"""
		correct = False
		txt = ''
		while self.line and self.line.isspace():
			correct = True
			txt += self.line
			self._newline()
		if self.line and not correct:
			raise ParseWarning(
				"Incorrect indentation %s" % repr(self.line), self.pos)
		return txt

	def blockquote(self, ind, first_ind=''):
		"""
		Indented block quote
		"""
		if self.line:
			ind0 = self.indent()
			if ind0 >= ' ':
				self.wrapper.nowrap(ind0)
				self.remove_indent()
				self.body(ind + ind0)#, first_ind)
				return True
		return False

	def element(self, ind, first_ind=''):
		"""
		determine body element beginning from current line
		"""
		correct = False
		for func in [self.blockquote, self.line_block, \
		self.opt_list, self.field_list, self.list1, \
		self.title, self.simple_table, self.grid, self.def_list, self.doctest, \
		self.transition, self.double_dot, self.quoted_literal, \
		self.paragraph]:
			if func(ind, first_ind):
				correct = True
				break
		return correct

	def paragraph_r(self, ind):
		"""
		recursively collect lines to paragraph and return them
		"""
		if self.line:
			if not self.line.isspace():
				txt = self.line
				self.newline()
				if self.line and self.indent() == ind:
					self.remove_indent()
					txt += self.paragraph_r(ind)
				return txt
		return ''

	def paragraph(self, ind, first_ind='', nowrap=False):
		"""
		paragraph of text
		"""
		txt = self.paragraph_r(ind)
		if txt != '':
			if nowrap:
				self.wrapper.nowrap(txt, ind)
			else:
				self.wrapper.wrap(txt, ind, first_ind)
			if txt.rstrip().endswith('::'):
				blanks = self.blank()
				if not self.line or self.indent() > ind:
					self.wrapper.nowrap(blanks)
					self.continue_indent(self.literal_block, ind+' ')
			return True
		else:
			return False

	def line_block(self, ind, first_ind=''):
		"""
		line block

		| example
		  of it
		"""
		if self.line:
			lbm = self.line_block_re.match(self.line)
			if lbm:
				self.wrapper.nowrap(self.line)
				ind0 = ind + ' '*len(lbm.group())
				self.newline()
				if self.line and not self.line.isspace():
					if self.indent() == ind0:
						self.remove_indent()
						self.wrapper.nowrap(ind0)
						self.paragraph(ind0, first_ind, nowrap=True)
					self.continue_indent(self.line_block, ind)
				return True
		return False

	def literal_paragraph(self, ind, first_ind=''):
		"""
		not wrapped paragraph
		"""
		if self.line and not self.line.isspace():
			self.wrapper.nowrap(self.line)
			self.newline()
			self.continue_indent(self.literal_paragraph, ind)
			return True
		return False

	def literal_block(self, ind, first_ind=''):
		"""
		literal block
		"""
		if self.line:
			self.literal_paragraph(ind, first_ind)
			if self.line:
				if self.line.isspace():
					blanks = self.blank()
					if not self.line or self.indent() >= ind:
						self.wrapper.nowrap(blanks)
				self.continue_indent(self.literal_block, ind)
		return True

	def quoted_literal_r(self, ind, quote):
		"""
		recursively collect lines to quoted literal block
		"""
		if self.line:
			if self.line.startswith(quote):
				txt = self.line
				self.newline()
				if self.line and self.indent() == ind:
					txt += self.indent()
					self.remove_indent()
					txt += self.quoted_literal_r(ind, quote)
				return txt
		return ''
		
	def quoted_literal(self, ind, first_ind=''):
		"""
		quoted literal block
		
		> here it is
		"""
		if self.line:
			qlm = self.quoted_literal_re.match(self.line)
			if qlm:
				quote = qlm.group(1)
				if not qlm.group() == '::':
					txt = self.quoted_literal_r(ind, quote)
					self.wrapper.nowrap(txt)
					return True
			return False

	def opt_list(self, ind, first_ind=''):
		"""
		options list
		"""
		if self.line:
			opt_match = self.opt_re.match(self.line)
			if opt_match:
				self.remove_indent(opt_match.group())
				txt = opt_match.group()
				#self.wrapper.nowrap(ind)
				self.wrapper.nowrap(txt, ind)
				ind0 = None
				if not self.line.isspace():
					ind0 = ind + ' '*len(opt_match.group()) + self.indent()
					self.wrapper.nowrap(self.indent())
				elif self.nextline() and not self.opt_re.match(self.nextline()):
					self.newline()
					ind0 = self.indent()
					self.wrapper.nowrap("\n")
					self.wrapper.nowrap(ind0)
				else:
					raise ParseWarning(
						"Incorrect option definition %s" % self.line, self.pos)
				if ind0:
					self.remove_indent()
					self.body(ind0, ind0)
				else:
					self.newline()
				self.continue_indent(self.opt_list, ind)
				return True
		return False

	def field_name(self, line):
		"""
		check whether line represents field name and return it, None otherwise
		"""
		if line and line[0] == ':' and len(line) > 2:
			fname = line[0:2]
			for char in line[2:]:
				if fname[-2] != "\\" and fname[-1] == ':':
					if char.isspace() and len(fname) > 2:
						return fname
					else:
						return None
				fname += char
		return None

	def field_list(self, ind, first_ind=''):
		"""
		field list
		"""
		if self.line:
			fname = self.field_name(self.line)
			if fname:
				self.remove_indent(fname)
				next_l = self.nextline()
				if next_l and not self.field_name(next_l.lstrip()):
					if not next_l.isspace():
						ind0 = self.indent(next_l)
					else:
						ind0 = ind + ' '*len(fname)
				else:
					ind0 = None
				self.wrapper.nowrap(fname, ind)
				if not self.line.isspace():
					ind1 = self.indent()
					self.remove_indent()
					self.wrapper.nowrap(ind1)
					first_ind = ' '*(len(ind) + len(fname) + len(ind1))
				if ind0:
					self.body(ind0, first_ind)
				else:
					self.wrapper.wrap(self.line, first_ind, first_ind)
					self.newline()
				self.continue_indent(self.field_list, ind)
				return True
		return False
	
	def list_item(self, ind, first_ind):
		"""
		list item
		"""
		return self.body(ind, first_ind)

	def list1(self, ind, first_ind=''):
		"""
		bullet or enumerated list
		"""
		if self.line:
			list_match = self.list_re.match(self.line)
			if list_match:
				txt = list_match.group()
				self.remove_indent(list_match.group())
				ind0 = ind + ' '*len(list_match.group()) + self.indent()
				self.remove_indent()
				self.wrapper.wrap(txt, ind, first_ind)
				first_ind = ind0
				self.list_item(ind0, first_ind)
				self.continue_indent(self.list1, ind)
				return True
		return False

	def def_list(self, ind, first_ind=''):
		"""
		definition list
		"""
		if self.line \
		and not self.line.isspace() \
		and not self.line.startswith('.. '):
			txt = self.line
			self.newline()
			if self.line:
				ind0 = self.indent()
				if not self.line.isspace() and ind0 > ind:
					self.wrapper.nowrap(txt, ind)
					self.remove_indent()
					self.wrapper.nowrap(ind0)
					self.body(ind0)
					self.continue_indent(self.def_list, ind)
					return True
			self.oldpos()
		return False

	def doctest(self, ind, first_ind=''):
		"""
		doctest strings
		(they start from >>>)
		"""
		if self.line and self.line.startswith('>>>'):
			self.wrapper.nowrap('>>>', ind)
			self.remove_indent('>>>')
			return self.literal_paragraph(ind)

	def grid(self, ind, first_ind=''):
		"""
		grid table
		+------+-------+
		| grid | table |
		+------+-------+
		"""
		if self.line and self.grid_sep_re.match(self.line):
			self.wrapper.nowrap(self.line, ind)
			self.newline()
			if self.line and not self.line.isspace():
				self.remove_indent(ind)
				self.wrapper.nowrap(ind)
				if not self.grid_row(ind):
					raise ParseWarning("Row expected", self.pos)
					#return False
				if self.line:
					if self.grid(ind):
						return True
				raise ParseWarning("Row separator expected", self.pos)
				#return False
			return True
		return False
	
	def grid_row(self, ind, first_ind=''):
		"""
		row of grid table
		"""
		if self.line and self.line[0] == '|':
			self.wrapper.nowrap(self.line, ind)
			self.newline()
			if self.line and not self.line.isspace():
				self.remove_indent(ind)
				self.wrapper.nowrap(ind)
				self.grid_row(ind)
			return True
		return False

	def simple_table(self, ind, first_ind=''):
		"""
		simple table
		========  =======
		 simple    table
		========  =======
		example
		========  =======
		"""
		if self.line and self.simple_table_re.match(self.line):
			self.wrapper.nowrap(self.line, ind)
			self.newline()
			if self.line and not self.line.isspace():
				self.remove_indent(ind)
				self.wrapper.nowrap(ind)
				self.simple_table_row(ind)
				if self.line:
					if self.simple_table(ind):
						return True
				raise ParseWarning("Simple table is not finished", self.pos)
				#return False
			return True
		return False

	def simple_table_row(self, ind, first_ind=''):
		"""
		row of simple table
		"""
		if self.line and not self.simple_table_re.match(self.line):
			self.wrapper.nowrap(self.line, ind)
			self.newline()
			if self.line:
				self.remove_indent(ind)
				self.wrapper.nowrap(ind)
				self.simple_table_row(ind)
			return True
		return False

	def transition(self, ind, first_ind=''):
		"""
		transition
		--------

		"""
		if self.line and self.transition_re.match(self.line):
			self.wrapper.nowrap(self.line, ind)
			self.newline()
			return True
		return False

	def double_dot(self, ind, first_ind=''):
		"""
		double dot (comments, citations, hyperlinks, directives, footnotes, ...)
		"""
		if self.line and self.line.startswith('.. '):
			if not self.directive(ind, first_ind) \
			and not self.footnote(ind, first_ind):
				self.wrapper.nowrap('.. ', ind)
				self.remove_indent('.. ')
				ind0 = ind + ' '*len('.. ')
				if self.line.rstrip().endswith('::'):
					self.wrapper.wrap(self.line, ind0, ind0)
					self.newline()
					self.literal_block(ind0)
				else:
					self.body(ind0)
			self.continue_indent(self.double_dot, ind)
			return True
		return False

	def footnote(self, ind, first_ind=''):
		"""
		footnote or citation
		"""
		if self.line:
			fnm = self.footnote_re.match(self.line)
			if fnm:
				self.wrapper.nowrap(fnm.group())
				self.remove_indent(fnm.group())
				ind0 = ind + ' '*len(fnm.group())
				if not self.line.isspace():
					self.body(ind + ' '*len('.. '), ind0)
				return True
		return False

	def directive(self, ind, first_ind=''):
		"""
		reStructuredText directives

		.. directive_type:: directive argument
		                    directive argument 2
		   :directive option: q
		   :option: 2

		   block
		"""
		if self.line:
			drm = self.directive_re.match(self.line)
			if drm:
				ind0 = ind + ' '*len('.. ')
				self.wrapper.nowrap(drm.group(1), ind)
				self.remove_indent(drm.group(1))
				self.literal_paragraph(ind + ' '*len(drm.group(1)))
				if self.line and self.indent() >= ind0:
					ind0 = self.indent()
					self.wrapper.nowrap(ind0)
					self.remove_indent()
					if self.field_list(ind0):
						self.continue_indent(self.body, ind0)
					else:
						self.body(ind0)
				return True
		return False
			
	def title(self, ind, first_ind=''):
		"""
		title

		=======
		 Title
		=======
		"""
		if self.line:
			title_match = self.title_re.match(self.line)
			title_start = None
			title_ind = ind
			if title_match:
				title_start = title_match.group()
				self.newline()
				if self.line:
					title_ind = self.indent()
					self.remove_indent()
			if self.line:
				txt = self.line
				self.newline()
				if self.line and self.indent() == ind:
					self.remove_indent()
					title_match = self.title_re.match(self.line)
					if title_match:
						if title_start:
							self.wrapper.nowrap(title_start, ind)
							self.wrapper.nowrap(title_ind)
						self.wrapper.nowrap(txt, title_ind)
						self.wrapper.nowrap(ind)
						self.wrapper.nowrap(title_match.group(), ind)
						self.newline()
						if self.line and self.indent() == ind:
							self.remove_indent()
							self.wrapper.nowrap(ind)
							self.body(ind)
						return True
					self.oldpos()
				self.oldpos()
			if title_start:
				self.oldpos()
				self.oldpos()
		return False


# type of proceeding text (matters in case of parsing python code)
CODE = 0
DOCSTRING = 1
COMMENT = 2

class MainParser:
	"""
	Main parser and wrapper. Has ability to wrap only given lines and python
	comments and docstrings.
	"""

	# helper regular expressions
	docstring_start_re = re.compile('^(\s*""")')
	docstring_end_re = re.compile('(.*)"""\s*$')
	comment_re = re.compile('^(\s*#)\s')

	def __init__(self, cols=None, line0=None, line1=None, python_lines = False):
		self.parser = Parser(cols=cols)
		self.line0 = line0
		self.line1 = line1
		self.python_lines = python_lines

	def wrap_comments(self, wrap, comment_part):
		"""
		parse and wrap lines and then make them python comments
		"""
		w2c = re.compile('^\s{%d}' % len(comment_part), re.MULTILINE)
		return [ w2c.sub(comment_part, \
			''.join(self.parser.parse(wrap)))]

	def parse(self, in_lines):
		"""
		get lines of text and return string of this text wrapped to given columns
		"""
		out_lines = []
		# parse in_lines and wrap everything needed
		p_state = CODE
		i = 1
		wrap = []
		nowrap = []
		comment_indent = [None, None]
		ind = first_ind = ''
		for line in in_lines:
			if self.line0 is not None and self.line1 is not None \
			and (i < self.line0 or i > self.line1):
				if wrap:
					out_lines += self.parser.parse(wrap)
					wrap = []
				nowrap.append(line)
			elif not self.python_lines:
				if nowrap:
					out_lines += nowrap
				nowrap = []
				wrap.append(line)
			elif p_state == CODE:
				if self.docstring_start_re.match(line):
					p_state = DOCSTRING
					dsm = self.docstring_start_re.match(line)
					nowrap.append(dsm.group())
					out_lines += nowrap
					nowrap = []
					ind = line[0:len(dsm.group())-3]
					first_ind = ' '*len(dsm.group())
					line = line[len(dsm.group()):]
					wrap.append(line)
					if self.docstring_end_re.match(line):
						p_state = CODE
						out_lines += self.parser.parse(wrap, ind, first_ind)
						wrap = []
				elif self.comment_re.match(line):
					p_state = COMMENT
					out_lines += nowrap
					nowrap = []
					cmm = self.comment_re.match(line)
					comment_indent[0] = cmm.group(1)
					comment_indent[1] = cmm.group(1)
					wrap.append(' '*len(comment_indent[0]) + \
						line[len(comment_indent[0]):])
					ind = first_ind = ' '*len(comment_indent[0])
				else:
					nowrap.append(line)
			elif p_state == DOCSTRING:
				dsm = self.docstring_end_re.match(line)
				if dsm:
					p_state = CODE
					if not dsm.group(1).isspace():
						wrap.append(dsm.group(1))
					else:
						nowrap.append(dsm.group(1))
					out_lines += self.parser.parse(wrap, '', first_ind)
					wrap = []
					nowrap.append(line[len(dsm.group(1)):])
				else:
					wrap.append(line)
			elif p_state == COMMENT:
				cmm = self.comment_re.match(line)
				if cmm:
					comment_indent[0] = cmm.group(1)
					if comment_indent[0][-1] == "\n":
						comment_indent[0] = comment_indent[0][:-1] + ' '
					if comment_indent[1] \
					and comment_indent[0] != comment_indent[1]:
						out_lines += self.wrap_comments(wrap, comment_indent[1])
						wrap = []
						comment_indent[1] = comment_indent[0]
					wrap.append(' '*len(comment_indent[0]) \
						+ line[len(comment_indent[0]):])
				else:
					p_state = CODE
					out_lines += self.wrap_comments(wrap, comment_indent[0])
					comment_indent = [None, None]
					wrap = []
					nowrap.append(line)
			i += 1

		if nowrap:
			out_lines += nowrap
		if wrap:
			if p_state == COMMENT:
				out_lines += self.wrap_comments(wrap, comment_indent[1])
			else:
				out_lines += self.parser.parse(wrap, ind, first_ind)
		return ''.join(out_lines)


def main():
	"""
	main function
	parse command-line arguments, read lines from stdin run parser and write result to stdout
	"""
	python_lines = False
	line0 = line1 = None
	cols = None
	i = 1
	# here we parse command line arguments
	if i < len(sys.argv) and sys.argv[i].isdigit():
		cols = int(sys.argv[i])
		i += 1
	while i < len(sys.argv):
		if sys.argv[i] == '--lines' and i < len(sys.argv) - 2:
			line0 = int(sys.argv[i+1])
			line1 = int(sys.argv[i+2])
			i += 3
		elif sys.argv[i] == '--python':
			python_lines = True
			i += 1
		else:
			sys.stderr.write("Wrong command line argument '%s'\n" % sys.argv[i])
			sys.exit(1)
	parser = MainParser(cols, line0, line1, python_lines)
	sys.stdout.write(parser.parse(sys.stdin.readlines()))


if __name__ == '__main__':
	main()

