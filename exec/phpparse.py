import re
import phply.phpparse as ply
import phply.phplex as lex


class Parse(object):
	def __init__(self, file):
		#self.php = [line.strip() for line in open(file, 'r')]
		with open(file, 'r') as handler:
			self.php = handler.read()

	def parse_all(self):
		defines = {}
		for line in self.php:
			line_dict = self.parse_define(line)
			confs[len(confs):] = line_dict
		return confs

	def parse_define(self, line):
		regexp = re.compile('define\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)')
		params = regexp.search(line)
		if params: 
			return {params.groups()[0] : params.groups()[1]}
		else:
			return False

	def par(self):
		saida = ply.parser.parse(self.php, lexer=lex.lexer)
		return saida



