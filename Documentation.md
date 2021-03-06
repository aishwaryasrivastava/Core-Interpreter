Documentation
----
Aishwarya Srivastava, 04/04/2018

This is some brief documentation for the Core Interpreter project. 

1. The ```Tokenizer``` class
This class is largely based on the Tokenizer interface provided in the course material. An instance of the class has 3 class members:
	1. ```Tail```: the complete list of words read from the input
	2. ```Head```: the item on the tail that is currently being tokenized
	3. ```Token```: the most recent token that has been read by the tokenizer

The constructor for the ```tokenizer``` class takes in a list of words from the input which becomes the tail of the tokenizer. It assignes the first word form this tail to be the head, and the token to be the empty string.

```getToken()```: This method mimics the finite state automata discussed in class and sets ```self.token``` to be the token that is read from the head, and returns the kind of ```self.token```.
```skipToken()```: This method removes ```self.token``` from ```self.head``` so that a new token can be read. If ```self.head``` is empty, it updates it to be the next string in ```self.tail```.

2. Interpreter
This interpreter makes use of the object oriented approach discussed in class, where each non-terminal symbol is represented by it's own class.

2. User manual
Note: Make sure that the input file is in the same folder as the source code. If not, then the absolute path of the input file must be used when running the test driver.
In order to run the test driver, simply go to the command line terminal, and enter:
	```python3 Interpreter.py <coreprogram> <inputdata>```
For example, if the input file is named ```test.txt```, and you wish to print the pretty print version of the code in ```coreprogram.txt```, then the command is as follows:
	```python3 Interpreter.py coreprogram.txt test.txt```

*Make sure that you use python3 and not just python, as the source code uses a lot of features that do not exist in the earlier versions.


3. Notes
The Interpreter was tested on input files containing various kinds of errors, such as single pipe symbols, or digits followed immediately after lower-case words. It was also tested on multiple non-erroneous files as well, including the ones provided in the course website. As of now there are no known bugs in the tokenizer. Some of the input files on which the code was tested is in the folder named "test-files".