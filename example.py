# -*- coding: utf-8 -*-
"""
@author: Joep Geuskens
"""
from CSVToLatex import CSVToLaTeX
import numpy as np


file_name = "test.csv"
#create a test file
a = np.random.random((30,10))*10
np.savetxt(file_name, a, delimiter=",", header=",".join(["$x_{:d}$".format(i) for i in range(10)]))

ctl = CSVToLaTeX(file_name, ncols=10, header=True) #create the converter

ctl.set_formatters(lambda s: "{:.2f}".format(float(s))) #default formatter to convert strings to floats

ctl.set_formatter(0, lambda s: r"\textbf{{ {:.2f} }}".format(float(s))) #make the first column bold

#Optionally, set `header=False` on line 10 and instead use the line below to add custom headers!
#ctl.set_headers(["$x$", "$y_1$", "$y_2$","$y_3$","$y_4$","$y_5$","$y_6$","$y_7$","$y_8$","$y_9$"]) #optionally add 'bold=True' for a bold header

#more custom stuff
ctl.set_column_line(0, "|") #add an outer column line 
ctl.set_column_line(1, "||") #add a double line after the first column
ctl.set_column_line(-1, "|") #add a line after the last column
ctl.set_row_lines([-1]) #add a line below the last row

#save the latex table to a tex file
ctl.tolatex("test.tex")