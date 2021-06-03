# -*- coding: utf-8 -*-
"""
@author: Joep Geuskens
"""
from ToLaTeXTable import LaTeXTable
import numpy as np
from pandas import DataFrame

file_name = "test.csv"
#create a test dataset
a = np.random.random((26,10))*10
#safe it to a file
np.savetxt(file_name, a, delimiter=",", header=",".join(["$x_{:d}$".format(i) for i in range(10)]))
#create a dataframe out of it
df = DataFrame(data=a, index=[c for c in "abcdefghijklmnopqrstuvwxyz"])

#create a latex table from the dataframe
ctl = LaTeXTable(df, headers=["$x_{:d}$".format(i) for i in range(10)]) #create the converter
#only needed for the dataframe (if an index is provided)
ctl.set_index_formatter(lambda s: r"\textbf{"+s+"}") #make the first column bold

#create a latex table from the dataset
ctl = LaTeXTable(a, headers=["$x_{:d}$".format(i) for i in range(10)])
#create a latex table from the csv file (if there is header=False, ncols MUST be given)
ctl = LaTeXTable(file_name, ncols=10, header=True)

ctl.set_formatters(lambda s: "{:.2f}".format(float(s))) #default formatter to convert strings to floats


#Optionally, set custom headers!
#ctl.set_headers(["$x$", "$y_1$", "$y_2$","$y_3$","$y_4$","$y_5$","$y_6$","$y_7$","$y_8$","$y_9$"]) #optionally add 'bold=True' for a bold header

#more custom stuff
ctl.set_column_line(0, "|") #add an outer column line 
ctl.set_column_line(1, "||") #add a double line after the first column
ctl.set_column_line(-1, "|") #add a line after the last column
ctl.set_row_lines([-1]) #add a line below the last row

#save the latex table to a tex file
ctl.tolatex("test.tex")