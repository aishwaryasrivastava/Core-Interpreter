from Tokenizer import Tokenizer
from TokenKind import TokenKind
from enum import Enum
import sys

# Core Interpreter (Printer, Parser, and Executer)
# Author:	Aishwarya Srivastava
# Date:		04/04/2018

DECLARED = []
VARIABLES = {}

class Prog:
	def __init__(self):
		self.ds = None
		self.ss = None

	def ParseProg(self):
		# Error check
		if (t.getToken() == TokenKind.KEYWORD_PROGRAM): 
			t.skipToken() 
			self.ds = DS()
			self.ds.ParseDS()

			if (t.getToken() == TokenKind.KEYWORD_BEGIN): 
				t.skipToken()
				self.ss = SS()
				self.ss.ParseSS()
				if (t.getToken() == TokenKind.KEYWORD_END): 
					t.skipToken()
				else:
					print("ERROR! Missing END")
					return
			else:
				print("ERROR! Missing BEGIN")
				return
		else:
			print("ERROR! Missing PROGRAM")
			return
	
	def PrintProg(self,file):
		file.write("program\n")
		indent = "	"
		self.ds.PrintDS(file,indent)
		file.write("begin\n")
		self.ss.PrintSS(file,indent)
		file.write("end\n")
	
	def ExecProg(self):
		self.ds.ExecDS()
		self.ss.ExecSS()

class DS:
	def __init__(self):
		self.ds = None
		self.decl = None

	def ParseDS(self):
		if (t.getToken() == TokenKind.KEYWORD_INT):
			self.decl = Decl()
			self.decl.ParseDecl()
			if (t.getToken() == TokenKind.KEYWORD_INT):
				self.ds = DS()
				self.ds.ParseDS()

	def PrintDS(self, file, indent):
		self.decl.PrintDecl(file, indent)
		if (self.ds is not None):
			self.ds.PrintDS(file, indent)

	def ExecDS(self):
		self.decl.ExecDecl()
		if (self.ds is not None):
			self.ds.ExecDS()

class SS:
	def __init__(self):
		self.ss = None
		self.stmt = None

	def ParseSS(self):
		self.stmt = Stmt()
		self.stmt.ParseStmt()
		if (t.getToken() in [TokenKind.IDENTIFIER, TokenKind.KEYWORD_IF, TokenKind.KEYWORD_WHILE, TokenKind.KEYWORD_READ, TokenKind.KEYWORD_WRITE]):
			self.ss = SS()
			self.ss.ParseSS()

	def PrintSS(self,file,indent):
		self.stmt.PrintStmt(file,indent)
		if(self.ss is not None):
			self.ss.PrintSS(file,indent)

	def ExecSS(self):
		self.stmt.ExecStmt()
		if(self.ss is not None):
			self.ss.ExecSS()

class Decl:
	def __init__(self):
		self.IDList = None

	def ParseDecl(self):
		if (t.getToken()==TokenKind.KEYWORD_INT):
			t.skipToken()
			self.IDList = IDList()
			self.IDList.ParseIDList()
			if (t.getToken() == TokenKind.SEMICOLON):
				t.skipToken()
			else:
				print("ERROR! Missing ;")
				return
	def ExecDecl(self):
		self.IDList.DeclareIDList()


	def PrintDecl(self, file, indent):
		file.write(indent)
		file.write("int ")
		self.IDList.PrintIDList(file,indent)
		file.write(";\n")
	

class IDList:
	def __init__(self):
		self.ID = None
		self.IDList = None

	def ParseIDList(self):
		self.ID = ID()
		self.ID.ParseID()

		if (t.getToken() == TokenKind.COMMA):
			t.skipToken() # Skip the ,
			self.IDList = IDList()
			self.IDList.ParseIDList()

	def PrintIDList(self,file,indent):
		self.ID.PrintID(file,indent)
		if (self.IDList is not None):
			self.IDList.PrintIDList(file,indent)

	def SetIDValues(self, values):
		if len(values)>0:
			self.ID.SetIDValue(values[0])
		if self.IDList is not None:
			self.IDList.SetIDValues(values[1:])

	def GetIDNames(self):
		if (self.IDList is None):
			return [self.ID.GetIDName()]
		else:
			return [self.ID.GetIDName()] + self.IDList.GetIDNames()

	def DeclareIDList(self):
		self.ID.DeclareID()
		if (self.IDList is not None):
			self.IDList.DeclareIDList()

class ID:
	def __init__(self):
		self.name = ""
		self.IDvalue = 0

	def ParseID(self):
		if (t.getToken() == TokenKind.IDENTIFIER):
			self.name = t.getTokenName()
			t.skipToken()

	def PrintID(self,file,indent):
		file.write(self.name + " ")

	def SetIDValue(self, value):
		self.IDvalue = int(value)

	def GetIDValue(self):
		return self.IDvalue

	def GetIDName(self):
		return self.name

	def DeclareID(self):
		DECLARED.append(self.name)



class Stmt:
	def __init__(self):
		self.altNo = 0
		self.AssignStmt = None
		self.IfStmt = None
		self.LoopStmt = None
		self.InStmt = None
		self.OutStmt = None

	def ParseStmt(self ):
		token = t.getToken()
		# If 
		if (token == TokenKind.KEYWORD_IF):
			self.IfStmt = If()
			self.IfStmt.ParseIf()
			self.altNo = 2
		# Loop
		if (token == TokenKind.KEYWORD_WHILE):
			self.LoopStmt = Loop()
			self.LoopStmt.ParseLoop()
			self.altNo = 3
		# Read
		if (token == TokenKind.KEYWORD_READ):
			self.InStmt = In()
			self.InStmt.ParseIn()
			self.altNo = 4

		# Write
		if (token == TokenKind.KEYWORD_WRITE):
			self.OutStmt = Out()
			self.OutStmt.ParseOut()
			self.altNo = 5

		# Assignment
		if (token == TokenKind.IDENTIFIER):
			self.AssignStmt = Assign()
			self.AssignStmt.ParseAssign()
			self.altNo = 1


		# Do the same for If, Loop, In, Out
	
	def PrintStmt(self,file,indent):
		if (self.altNo == 1): self.AssignStmt.PrintAssign(file,indent)
		elif (self.altNo == 2): self.IfStmt.PrintIf(file,indent)
		elif (self.altNo == 3): self.LoopStmt.PrintLoop(file,indent)
		elif (self.altNo == 4): self.InStmt.PrintIn(file,indent)
		elif (self.altNo == 5): self.OutStmt.PrintOut(file,indent)

	def ExecStmt(self):
		if (self.altNo == 1): self.AssignStmt.ExecAssign()
		elif (self.altNo == 2): self.IfStmt.ExecIf()
		elif (self.altNo == 3): self.LoopStmt.ExecLoop()
		elif (self.altNo == 4): self.InStmt.ExecIn()
		elif (self.altNo == 5): self.OutStmt.ExecOut() 

class Assign:
	def __init__(self):
		self.Id = None
		self.Exp = None

	def ParseAssign(self):
		self.Id = ID()
		self.Id.ParseID()
		if (t.getToken() == TokenKind.ASSIGNMENT_OPERATOR):
			t.skipToken()
			self.Exp = Exp()
			self.Exp.ParseExp()
			if (t.getToken() == TokenKind.SEMICOLON): 
				t.skipToken()
			else:
				print("ERROR! Missing ;")
		else:
			print("ERROR! Missing =")

	def ExecAssign(self):
		self.Id.SetIDValue(self.Exp.EvalExp())
		VARIABLES[self.Id.GetIDName()] = int(self.Id.GetIDValue())

	def PrintAssign(self,file,indent):
		file.write(indent)
		self.Id.PrintID(file,indent)
		file.write(" = ")
		self.Exp.PrintExp(file,indent)
		file.write(";\n")

class If:
	def __init__(self):
		self.cond = None
		self.ss1 = None
		self.ss2 = None
		self.altNo = 0

	def ParseIf(self):
		if (t.getToken() == TokenKind.KEYWORD_IF): 
			t.skipToken()
			self.cond = Cond()
			self.cond.ParseCond()
			if (t.getToken() == TokenKind.KEYWORD_THEN): 
				t.skipToken()
				self.ss1 = SS()
				self.ss1.ParseSS()
				token = t.getToken()
				if (token == TokenKind.KEYWORD_ELSE):
					self.altNo = 1
					t.skipToken() # Skip "else"
					self.ss2 = SS()
					self.ss2.ParseSS()
				if (t.getToken() == TokenKind.KEYWORD_END):
					t.skipToken() # Skip "end"
					if (t.getToken() == TokenKind.SEMICOLON): 
						t.skipToken() # Skip ";"
					else:
						print("Error! Missing ;")
				else:
					print("Error! Missing END")
	
	def PrintIf(self,file,indent):
		file.write(indent)
		file.write("if ")
		self.cond.PrintCond(file,indent)
		file.write("\n")
		file.write(indent)
		file.write("then\n")
		self.ss1.PrintSS(file,indent+"\t")
		if (self.altNo == 1):
			file.write(indent)
			file.write("else\n")
			self.ss2.PrintSS(file,indent+"\t")
		file.write(indent)
		file.write("end;\n")

	def ExecIf(self):
		if(self.cond.EvalCond()):
			self.ss1.ExecSS()
		elif (self.altNo == 1):
			self.ss2.ExecSS()

class Loop:
	def __init__(self):
		self.cond = None
		self.stmtseq = None

	def ParseLoop(self):
		if (t.getToken() == TokenKind.KEYWORD_WHILE):
			t.skipToken() # skip "while"
			self.cond = Cond()
			self.cond.ParseCond()
			if (t.getToken() == TokenKind.KEYWORD_LOOP):
				t.skipToken() # skip "loop"
				self.stmtseq = SS()
				self.stmtseq.ParseSS()
				if (t.getToken() == TokenKind.KEYWORD_END):
					t.skipToken()
					if (t.getToken() == TokenKind.SEMICOLON):
						t.skipToken()
					else: 
						print("Error! Missing ;") 
						return
				else:
					print("Error! Missing END")
					return

	def PrintLoop(self,file,indent):
		file.write(indent)
		file.write("while ")
		self.cond.PrintCond(file,indent)
		file.write(" loop\n")
		self.stmtseq.PrintSS(file,indent+"\t")
		file.write(indent)
		file.write("end;\n")

	# are u sure tho
	def ExecLoop(self):
		while(self.cond.EvalCond()):
			self.stmtseq.ExecSS()

class In:
	def __init__(self):
		self.IdList = None

	def ParseIn(self):
		if (t.getToken == TokenKind.KEYWORD_READ):
			t.skipToken()
			self.IdList = IdList()
			self.IdList.ParseIDList()
			if (t.getToken == TokenKind.SEMICOLON):
				t.skipToken()
			else:
				print("ERROR! Missing ;")
		else:
			print("ERROR! Missing READ keyword")

	def PrintIn(self,file,indent):
		file.write(indent)
		file.write("read ")
		self.IdList.PrintIDList(file,indent)

	def ExecuteIn(self):
		readInput = raw_input()
		readValues = readInput.split()
		if len(readValues)!= len(self.IdList):
			print("Error! Incorrect number of values")
		else:
			areInts = True
			for value in readValues:
				areInts = areInts and value.isdigit()
			if (not areInts):
				print("ERROR! Non-integer values!")
			else:
				self.IdList.SetIDValues(readValues)

class Out:
	def __init__(self):
		self.IdList = None

	def PrintOut(self,file,indent):
		file.write(indent)
		file.write("write ")
		self.IdList.PrintIDList(file,indent)
		file.write(";\n")

	def ParseOut(self):
		if (t.getToken() == TokenKind.KEYWORD_WRITE):
			t.skipToken()
			self.IdList = IDList()
			self.IdList.ParseIDList()
			if (t.getToken() == TokenKind.SEMICOLON):
				t.skipToken()
			else:
				print("ERROR! Missing ; in WRITE statement")
		else:
			print("ERROR! Missing keyword WRITE")

	def ExecOut(self):
		values = self.IdList.GetIDNames()
		for x in values:
			print(VARIABLES[x])
		
class Cond:
	def __init__(self):
		self.comp = None
		self.cond1 = None
		self.cond2 = None
		self.altNo = 0

	def ParseCond(self):
		
		if (t.getToken() == TokenKind.NOT_OPERATOR):
			# not
			self.altNo = 2
			t.skipToken()
			self.cond1 = Cond()
			self.cond1.ParseCond()

		if (t.getToken() == TokenKind.OPEN_SQUARE):
			t.skipToken()
			self.cond1 = Cond()
			self.cond1.ParseCond()
			if (t.getToken() == TokenKind.AND_OPERATOR):
				self.altNo = 3
				t.skipToken()
			elif (t.getToken() == TokenKind.OR_OPERATOR):
				self.altNo = 4
				t.skipToken()
			else:
				print("ERROR while parsing condition")
				return
			
			self.cond2 = Cond()
			self.cond2.ParseCond()

			if (t.getToken() == TokenKind.CLOSED_SQUARE):
				t.skipToken()

			else:
				print("ERROR! Missing ]")
				return

		else:
			# comparison
			self.altNo = 1
			self.comp = Comp()
			self.comp.ParseComp()
			

	def PrintCond(self,file,indent):
		if (self.altNo == 1):  
			self.comp.PrintComp(file,indent)
		elif (self.altNo == 2):  
			file.write("!") 
			self.cond1.PrintCond(file,indent)
		elif (self.altNo == 3): 
			file.write("[ ")
			self.cond1.PrintCond(file,indent) 
			file.write(" && ") 
			self.cond2.PrintCond(file,indent)
			file.write(" ]")
		elif (self.altNo == 4): 
			file.write("[ ")
			self.cond1.PrintCond(file,indent) 
			file.write(" || ") 
			self.cond2.PrintCond(file,indent)
			file.write(" ]")

	def EvalCond(self):
		if (self.altNo == 1): return self.comp.EvalComp()
		elif (self.altNo == 2): return not self.cond1.EvalCond()
		elif (self.altNo == 3): return self.cond1.EvalCond() and self.cond2.EvalCond()
		elif (self.altNo == 4): return self.cond1.EvalCond() or self.cond2.EvalCond()

class Comp:
	def __init__(self):
		self.op1 = None
		self.op2 = None
		self.altNo = 0
		self.compop = ""

	def ParseComp(self):
		if(t.getToken() == TokenKind.OPEN_PAREN):
			t.skipToken()
			self.op1 = OP()
			self.op1.ParseOP()
			
			if(t.getToken() == TokenKind.INEQUALITY_TEST): self.altNo = 1
			elif(t.getToken() == TokenKind.EQUALITY_TEST): self.altNo = 2
			elif(t.getToken() == TokenKind.STRICTLY_LESS): self.altNo = 3
			elif(t.getToken() == TokenKind.STRICTLY_GREATER): self.altNo = 4
			elif(t.getToken() == TokenKind.LESS_THAN_OR_EQUAL): self.altNo = 5
			elif(t.getToken() == TokenKind.GREATER_THAN_OR_EQUAL): self.altNo = 6
			else: 
				print("INVALID OPERATOR IN COMP") 
				return

			self.compop = t.getTokenName()
			t.skipToken()

			self.op2 = OP()
			self.op2.ParseOP()
			if(t.getToken() == TokenKind.CLOSED_PAREN):
				t.skipToken()
			else:
				print("ERROR! Missing ) in comp")
				return
		else:
			print("ERROR! Missing ( in comp")
			return

	def EvalComp(self):
		x = self.op1.EvalOP()
		y = self.op2.EvalOP()
		if (self.altNo == 1): return x != y
		elif (self.altNo == 2): return x == y
		elif (self.altNo == 3): return x < y
		elif (self.altNo == 4): return x > y
		elif (self.altNo == 5): return x <= y
		elif (self.altNo == 6): return x >= y


	def PrintComp(self,file,indent):
		file.write("( ")
		self.op1.PrintOP(file,indent)
		file.write(self.compop)
		self.op2.PrintOP(file,indent)
		file.write(" )")

class Exp:
	def __init__(self):
		self.trm = None
		self.exp = None
		self.altNo = 0

	def ParseExp(self):
		self.trm = Trm()
		self.trm.ParseTrm()
		if (t.getToken() == TokenKind.ADD_OPERATOR):
			self.altNo = 1
			t.skinToken()
			self.exp = Exp()
			self.exp.ParseExp()
		elif (t.getToken() == TokenKind.SUBTRACT_OPERATOR):
			self.altNo = 2
			t.skipToken()
			self.exp = Exp()
			self.exp.ParseExp()
		else: 
			self.altNo = 3

	def EvalExp(self):
		if (self.altNo == 1):
			return self.trm.EvalTrm() + self.exp.EvalExp()
		elif (self.altNo == 2):
			return self.trm.EvalTrm() - self.exp.EvalExp()
		elif (self.altNo == 3):
			return self.trm.EvalTrm()

	def PrintExp(self,file,indent):
		if (self.altNo == 1):
			self.trm.PrintTrm(file,indent)
			file.write(" + ")
			self.exp.PrintExp(file,indent)
		elif (self.altNo == 2):
			self.trm.PrintTrm(file,indent)
			file.write(" - ")
			self.exp.PrintExp(file,indent)
		elif (self.altNo == 3):
			self.trm.PrintTrm(file,indent)

class Trm():
	def __init__(self):
		self.op = None
		self.trm = None
		self.altNo = 0

	def ParseTrm(self):
		self.op = OP()
		self.op.ParseOP()
		if (t.getToken() == TokenKind.MULTIPLICATION_OPERATOR):
			t.skipToken()
			self.altNo = 1
			self.trm = Trm()
			self.trm.ParseTrm()
	
	def PrintTrm(self,file,indent):
		self.op.PrintOP(file,indent)
		if (self.altNo == 1):
			file.write(" * ")
			self.trm.PrintTrm(file,indent)

	def EvalTrm(self):
		if (self.altNo == 1):
			return self.op.EvalOP() * self.trm.EvalTrm()
		else:
			return self.op.EvalOP()

class OP():
	def __init__(self):
		self.no = None
		self.id = None
		self.exp = None
		self.altNo = 0

	def ParseOP(self):
		if (t.getToken() == TokenKind.INTEGER_CONSTANT):
			self.altNo = 1
			self.no = t.getTokenName()
			t.skipToken()
		elif (t.getToken() == TokenKind.IDENTIFIER):
			self.altNo = 2
			self.id = ID()
			self.id.ParseID()
		elif (t.getToken() == TokenKind.OPEN_PAREN):
			t.skipToken()
			self.altNo = 3
			self.exp = Exp()
			self.exp.ParseExp()
			if (t.getToken() == TokenKind.CLOSED_PAREN):
				t.skipToken()
			else:
				print("ERROR! Missing ) in OP")
				return
		else:
			print("ERROR! Invalid operand ")
			return

	def PrintOP(self,file,indent):
		if (self.altNo == 1): file.write(self.no+" ")
		elif (self.altNo == 2): self.id.PrintID(file,indent)
		elif (self.altNo == 3): 
			file.write("( ")
			self.exp.PrintExp(file,indent)
			file.write(" )")

	def EvalOP(self):
		if (self.altNo == 1):
			return int(self.no)
		elif (self.altNo == 2):
			if self.id.GetIDName() in VARIABLES.keys():
				return VARIABLES[self.id.GetIDName()]
			else: return 0
		elif (self.altNo == 3):
			return self.exp.EvalExp()

# Reading the file and creating a list of words
programfile = sys.argv[1]
filename = sys.argv[2]
infile = open(filename, "r")

tail = []
for line in infile:
	for string in line.split():
		tail.append(string)
infile.close()

# Opening output file for writing
nameAndFormat = filename.split(".txt")
outfilename = "testoutput.txt".join(nameAndFormat)
outfile = open(outfilename, "w")
prettyprint = open(programfile,"w")

# Creating a tokenizer
t = Tokenizer(tail)

Program = Prog()
Program.ParseProg()
Program.PrintProg(prettyprint)
Program.ExecProg()

prettyprint.close()
outfile.close()



