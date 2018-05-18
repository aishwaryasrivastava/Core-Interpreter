Core Interpreter
----
Aishwarya Srivastava, 04/04/2018

This is an implementation of the Core Interpreter Project, written in Python 3.5.0. The submission contains 3 .py files as listed below, this README, a text file listing the command used to execute the test driver (```Runfile.txt```), brief documentation (```documentation.txt```), and a folder containing some test files (```test-files```). The source code files are listed as below:

1. ```TokenKind.py```: 
An enumeration class that holds the different token kinds. It uses the same values as the as the token kinds given in the lab description posted on the course website.
2. ```Tokenizer.py```:
The Tokenizer that is used for this project. It uses the finite state automata discussed in class to find tokens.
3. ```Interpreter.py```:
The main interpreter for this project. It parses, executes, and prints an input Core program according to the BNF discussed in class.

In order to run the interpreter, go to the terminal and type the following command (also available in Runfile.txt without the filename):
	```python3 Interpreter.py <coreprogram> <inputdata>```

For example, if you want to tokenize a program saved in test.txt, this is the command you should use:
	```python3 Interpreter.py coreprogram.txt test.txt```

Note that this project is entirely written in python3, and may cause issues when run with just python (e.g. enum class not available, print is a statement, not a method, etc.)