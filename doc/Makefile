#
# Encoding: utf-8
# Project:	Implementation of the Lemke-Howson algorithm for finding MNE
# Author:	Petr Zemek <s3rvac@gmail.com>, 2009
#
# GNU Makefile for project documentation.
#

PROJ = documentation

all: $(PROJ).pdf

$(PROJ).pdf: $(PROJ).tex
	pdflatex $(PROJ)
	pdflatex $(PROJ)

clean:
	rm -f *.dvi *.log $(PROJ).blg $(PROJ).bbl $(PROJ).toc *.aux $(PROJ).out
