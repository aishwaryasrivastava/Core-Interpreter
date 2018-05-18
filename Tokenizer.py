from TokenKind import TokenKind

# Tokenizer for Core Interpreter project.
# Author:	Aishwarya Srivastava
# Date:		03/03/2018

class Tokenizer:
	
	# Constructor for tokenizer. 
	# itString is a list of non-whitespace strings from which the tokens are to be extracted.
	def __init__(self, itString):
		self.tail = itString
		if len(self.tail)>0:
			self.head = self.tail[0]
		else:
			self.head = ""
		self.token = ""
	
	# Returns the current token
	def getTokenName(self):
		return self.token;

	# Skips the first token in self.head
	def skipToken(self):
		# Taking away the token from the head
		self.head = self.head[len(self.token):]
		# If nothing left, then move on to the next item in the tail
		if self.head == "":
			if len(self.tail) > 0:
				self.tail.pop(0)
				if len(self.tail) > 0:
					self.head = self.tail[0]

	# Sets self.token to the first legal token found in self.head and returns it's kind
	def getToken(self):
		self.token = ""
		# LC
		if self.head[0].islower():
			i = 0
			while i < len(self.head) and self.head[i].islower():
				self.token = self.token + self.head[i]
				i = i+1
			if i < len(self.head):
				if self.head[i].isupper() or self.head[i].isdigit():
					return TokenKind.ERROR
			
			if self.token == "program":
				return TokenKind.KEYWORD_PROGRAM
			elif self.token == "begin":
				return TokenKind.KEYWORD_BEGIN
			elif self.token == "end":
				return TokenKind.KEYWORD_END
			elif self.token == "int":
				return TokenKind.KEYWORD_INT
			elif self.token == "if":
				return TokenKind.KEYWORD_IF
			elif self.token == "then":
				return TokenKind.KEYWORD_THEN
			elif self.token == "else":
				return TokenKind.KEYWORD_ELSE
			elif self.token == "while":
				return TokenKind.KEYWORD_WHILE
			elif self.token == "loop":
				return TokenKind.KEYWORD_LOOP
			elif self.token == "read":
				return TokenKind.KEYWORD_READ
			elif self.token == "write":
				return TokenKind.KEYWORD_WRITE
			else:
				return TokenKind.ERROR
		# UC
		elif self.head[0].isupper():
			i = 0
			containsDigits = False
			# Gathering UC
			while i < len(self.head) and self.head[i].isupper():
				self.token = self.token + self.head[i]
				i = i+1
			# Gathering Digits
			while i < len(self.head) and self.head[i].isdigit():
				containsDigits = True
				self.token = self.token + self.head[i]
				i = i + 1
			if i < len(self.head) and (containsDigits and self.head[i].isupper() or self.head[i].islower()):
				return TokenKind.ERROR
			return TokenKind.IDENTIFIER
		# Digit
		elif self.head[0].isdigit():
			i = 0
			while i < len(self.head) and self.head[i].isdigit():
				self.token = self.token + self.head[i];
				i = i + 1
			if i < len(self.head) and self.head[i].isalpha():
				return TokenKind.ERROR
			return TokenKind.INTEGER_CONSTANT
		
		# End of file
		elif self.head == "":
			return TokenKind.EOF
		# ;
		elif self.head[0] == ';':
			self.token = ";"
			return TokenKind.SEMICOLON
		# ,
		elif self.head[0] == ',':
			self.token = ","
			return TokenKind.COMMA
		# =
		elif self.head[0] == '=':
			if len(self.head) > 1 and self.head[1] == "=":
				self.token = "=="
				return TokenKind.EQUALITY_TEST
			else:
				self.token = "="
				return TokenKind.ASSIGNMENT_OPERATOR
		# !
		elif self.head[0] == '!':
			if len(self.head) > 1 and self.head[1] == "=":
				self.token = "!="
				return TokenKind.INEQUALITY_TEST
			else:
				self.token = "!"
				return TokenKind.NOT_OPERATOR
		# [
		elif self.head[0] == "[":
			self.token = "["
			return TokenKind.OPEN_SQUARE
		# ]
		elif self.head[0] == "]":
			self.token = "]"
			return TokenKind.CLOSED_SQUARE
		# &
		elif self.head[0] == '&':
			if len(self.head) > 1 and self.head[1] == "&":
				self.token = "&&"
				return TokenKind.AND_OPERATOR
			else:
				return TokenKind.ERROR
		# |
		elif self.head[0] == "|":
			if len(self.head) > 1 and self.head[1] == "|":
				self.token = "||"
				return TokenKind.OR_OPERATOR
			else:
				return TokenKind.ERROR

		# (
		elif self.head[0] == "(":
			self.token = "("
			return TokenKind.OPEN_PAREN
		# )
		elif self.head[0] == ")":
			self.token = ")"
			return TokenKind.CLOSED_PAREN

		# +
		elif self.head[0] == "+":
			self.token = "+"
			return TokenKind.ADD_OPERATOR
		# -
		elif self.head[0] == "-":
			self.token = "-"
			return TokenKind.SUBTRACT_OPERATOR
		# *
		elif self.head[0] == "*":
			self.token = "*"
			return TokenKind.MULTIPLICATION_OPERATOR

		# <
		elif self.head[0] == '<':
			if len(self.head) > 1 and self.head[1] == "=":
				self.token = "<="
				return TokenKind.LESS_THAN_OR_EQUAL
			else:
				self.token = "<"
				return TokenKind.STRICTLY_LESS

		# >
		elif self.head[0] == '>':
			if len(self.head) > 1 and self.head[1] == "=":
				self.token = ">="
				return TokenKind.GREATER_THAN_OR_EQUAL
			else:
				self.token = ">"
				return TokenKind.STRICTLY_GREATER

		# Not special character, identifier, integer, or lowercase
		else:
			return TokenKind.ERROR
