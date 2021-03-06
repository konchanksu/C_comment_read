PYTHON	= python
PYDOC	= pydoc
PYCS	= $(shell find . -name "*.pyc")
PYCACHE	= $(shell find . -name "__pycache__")
PYLINT	= pylint
PYUTEST = unittest

BASE	= comment
C_DIR   = ../c_programs/
C_FILE  = $(C_DIR)tmp.c
EXT	    = py
PACKAGE = packages
PKGTDIR	= $(shell echo $(PACKAGE) | cut -d '.' -f1)
TARGET	= $(BASE).$(EXT)
WORKDIR	= ./$(PACKAGE)/

LINTRST	= pylintresult.txt

all:
	@:

clean:
	@for each in ${PYCS} ; do echo "rm -f $${each}" ; rm -f $${each} ; done
	@for each in ${PYCACHE} ; do echo "rm -f $${each}" ; rm -rf $${each} ; done
	@if [ -e $(LINTRST) ] ; then echo "rm -f $(LINTRST)" ; rm -f $(LINTRST) ; fi
	@if [ -e MANIFEST ] ; then echo "rm -f MANIFEST" ; rm -f MANIFEST ; fi
	@find . -name ".DS_Store" -exec rm {} ";" -exec echo rm -f {} ";"

pydoc:
	(sleep 3 ; open http://localhost:9999/$(PACKAGE).html) & $(PYDOC) -p 9999

unittest:
	@find $(PKGTDIR) -name "[A-Za-z]*.py" -exec echo '*** ['{}'] ***' ";" -exec $(PYTHON) -m $(PYUTEST) {} ";"

test: all
	$(PYTHON) $(WORKDIR)$(TARGET) < $(C_FILE)

lint: clean
	$(PYLINT) `find . -name "*.py"` > $(LINTRST) ; less $(LINTRST)
