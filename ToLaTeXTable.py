# -*- coding: utf-8 -*-
"""
@author: Joep
"""
import numpy as np
from pandas import DataFrame
def LaTeXTable(data, **kwargs):
    if(type(data) is str):
        return CSVToLaTeX(data, **kwargs)
    elif(type(data) is np.ndarray):
        return MatrixToLaTeX(data, **kwargs)
    elif(type(data) is DataFrame):
        return DataFrameToLaTeX(data, **kwargs)

class __ToLaTeX__:
    def __init__(self, ncols, headers=None):
        self.ncols = ncols
        self.columns = None
        self.keys = dict()
        self.formatters = [str]*self.ncols
        self.headers = headers
        self.include_headers = (headers is not None)
        
    def set_include_headers(self, val):
        """
        If `val` is True, the first row of the table will be interpreted as a header.
        This is ignored if no headers are given by the csv file or by `set_headers()`
        """
        self.include_headers = val
    
    def set_headers(self, headers, bold=False):
        """
        Sets the headers of the table. This will automatically set `include_headers` to True.
        
        Parameters
        ----------
        headers : list
            The headers of the table. Its length should equal the number of columns in the csv file.
        bold : boolean, optional
            If True, the headers are styled with a bold font. The default is False.

        Raises
        ------
        ValueError
             If `len(headers)!=ncols`

        Returns
        -------
        None.

        """
        if(len(headers)==self.ncols):
            self.headers = headers
            self.include_headers = True
            self.keys["bold"] = bold
        else:
            raise ValueError("Number of headers does not match number of columns")
    
    def set_columns(self, columns):
        """
        Sets the column types of the table. The argument can be either a string or a list.
        In the first case, the columns of the table will be set to the literal string,
        otherwise the length of `columns` should equal `ncols`.
        'center', 'left' and 'right' are interpreted as 'c', 'l' and 'r' respectively.

        Parameters
        ----------
        columns : list
            List of column types.

        Returns
        -------
        None.

        """
        if(type(columns) is str):
            self.columns = columns
        if(len(columns)!=self.ncols):
            raise ValueError("Number of columns given does not correspond to ncols")
        self.columns = []
        for i in range(len(columns)):
            if(columns[i] == "center"):
                self.columns.append("c")
            elif(columns[i] == "left"):
                self.columns.append("l")
            elif(columns[i] == "right"):
                self.columns.append("r")
            else:
                self.columns.append(columns[i])
    
    #has no effect if self.columns is a string
    def set_column_lines(self, lines):
        """
        Sets the column separation lines of the table.
        
        Parameters
        ----------
        lines : list or string
            if string: the string can be either `all` or `none` in which case all column lines or none will be added respectively
            if list: the list should contain only integers. These are the indices of the column lines which are added. 0 being the leftmost line (at the start of the table)
            and -1 or `ncols+1` being the outermost line on the right
        """
        if(type(lines) is str):
            if(lines=="all"):
                self.keys["clines"] = ["|"]*(self.ncols+1)
            elif(lines=="none"):
                self.keys["clines"] = [""]*(self.ncols+1)
        elif (type(lines[0]) is int):
        	l = [""]*(self.ncols+1)
        	for i in lines:
        		l[i] = "|"
        	self.keys["clines"] = l
        else:
        	self.keys["clines"] = lines
    
    def set_column_line(self, idx, line):
        """
        Sets the column separation line at index `idx` to `line`.

        Parameters
        ----------
        idx : int
            index of the column seperator to be set. 0 is the outer left line and -1 or `ncols+1` the outer right line.
        line : str
            column type. Can be `|` or `||` for a single and double line respectively.

        Returns
        -------
        None.

        """
        if("clines" not in self.keys):
            self.set_column_lines("none")
        self.keys["clines"][idx] = line
    
    def set_row_lines(self, lines):
        """
        Sets the indices of the rows after which a separator line (`\hline`) should be added

        Parameters
        ----------
        lines : list of int
            indices of the rows. -1 indicates the line at the end of the table

        Returns
        -------
        None.

        """
        self.keys["rlines"] = lines
    
    def set_formatters(self, formatters):
        """
        Sets the formatters of the columns. This is usually necessary to obtain convert the CSV data to the
        required precision or notation. For example, printing each value with 2 decimal precision is done using
        `set_formatters(lambda s: "{:.2f}".format(float(s)))

        Parameters
        ----------
        formatters : list or lambda
            if lambda, a list of length `ncols` is created with each element being equal to `formatters`.
            The length of this list should equal the number of columns. Each element should be a function
            that takes a string as input and returns the formatted value.

        Raises
        ------
        ValueError
            if the length of `formatters` does not equals `ncols`.

        Returns
        -------
        None.

        """
        if(isinstance(formatters, (tuple, list))):    
            if(len(formatters) == self.ncols):
                self.formatters = formatters
            else:
                raise ValueError("length of argument does not match number of columns")
        else:
            self.formatters = [formatters]*self.ncols
    
    def set_formatter(self, idx, formatter):
        """
        Sets the formatter of column `idx`
        Parameters
        ----------
        idx : int
            index of the column, 0 being the leftmost column.
        formatter : lambda or function
            a function which takes a string as input and returns the formatted value. Example `set_formatter(0, lambda s: "{:.2f}".format(float(s)))`

        Returns
        -------
        None.

        """
        self.formatters[idx] = formatter
        
    def __construct_headers__(self):
        if(self.columns is None):
            self.columns = ["c"]*self.ncols
            
        if(type(self.columns) is str):
            colstr = self.columns
        else:
            if("clines" in self.keys):
                lines = self.keys["clines"]
            else:
                lines = [""]*(self.ncols+1)
            
            colstr = lines[0]
            for i in range(self.ncols):
                colstr += self.columns[i]+lines[i+1]
        headers = r"\begin{tabular}{"+colstr+"}" + "\n"
        all_lines = False
        rlines = []
        if("rlines" in self.keys):
            if(type(self.keys["rlines"]) is str):
                if(self.keys["rlines"] == "all"): all_lines = True
                elif(self.keys["rlines"] == "none"): rlines = [100000000]
            else:
                rlines = self.keys["rlines"]
        else:
            rlines = [10000000000] #yeah, bad programming, I know...
        if(self.include_headers):
            if("bold" in self.keys and self.keys["bold"]):
                self.headers = [r"\textbf{"+s+"}" for s in self.headers]
            headers += "\\hline\n"
            headers += " & ".join(self.headers) + "\\\\\n"
            headers += "\\hline\n"
        return all_lines, rlines, headers
    
    def tolatex(self):
        pass #this has to be implemented by the other classes

class CSVToLaTeX(__ToLaTeX__):
    def __init__(self, fname : str, ncols=None, header=False, **kwargs):
        """
        Creates the CSVToLaTeX object. Remember to close the object with `.close()` to close the csv input stream.
        
        Parameters
        ----------
        fname : string
            name of the input csv file.
        ncols : int, optional
            number of columns. This and/or `header` has to be given. The default is None.
        header : boolean, optional
            if True, the first line of the csv file is interpreted as a list of headers (column titles).
            The amount of columns is inferred from the number of elements in this list. This or `ncols` has to be given. 
            If they are both given, the number of headers has to match `ncols`. The default is False.
        **kwargs : key-value arguments
            arguments which are passed on to csv.reader().

        Raises
        ------
        ValueError
            If `ncols` is given and `header` is `True` but the number of headers does not match `ncols`.

        Returns
        -------
        None.

        """
        import csv
        if(ncols is None and header==False):
            raise ValueError("If the file does not include a header, please provide the number of columns")
        self.file = open(fname)
        self.reader = csv.reader(self.file, **kwargs)
        if(header):
            headers = list(next(self.reader))
            try:
                if(headers[0][0]=="#"): headers[0] = headers[0][1:]
            except:
                pass
            self.ncols = len(headers)
            if(ncols is not None and self.ncols != ncols):
                raise ValueError("Number of columns ({:d}) does not match number of headers ({:d})!".format(self.ncols, ncols))
            super().__init__(self.ncols, headers)
        else:
            super().__init__(ncols)
            
    def tolatex(self, fname):
        ofile = open(fname, 'w')
        all_lines, rlines, headers = self.__construct_headers__()
        ofile.write(headers)
        endline = r"\\" + "\n"
        
        rownr = 0
        idx = 0
        for row in self.reader:
            line = " & ".join([self.formatters[i](row[i]) for i in range(self.ncols)])
            ofile.write(line + endline)
            if(all_lines):
                ofile.write("\\hline\n")
            elif(idx < len(rlines) and rownr == rlines[idx]):
                idx += 1
                ofile.write("\\hline\n")
            rownr += 1
        if(rlines[-1]==-1):
            ofile.write("\\hline\n")
            
        ofile.write(r"\end{tabular}")
        ofile.close()
    
    def close(self):
         self.file.close()
         
    def __del__(self):
        self.close()
        
class MatrixToLaTeX(__ToLaTeX__):
    def __init__(self, data, headers=None):
        if(len(data.shape)!=2):
            raise ValueError("Expected dataset of dimension 2, got " + str(len(data.shape)))
        super().__init__(data.shape[1], headers)
        self.data = data
    
    def tolatex(self, fname):
        ofile = open(fname, 'w')
        all_lines, rlines, headers = self.__construct_headers__()
        ofile.write(headers)
        endline = r"\\" + "\n"
        
        rownr = 0
        idx = 0
        for row_idx in range(self.data.shape[0]):
            line = " & ".join([self.formatters[i](self.data[row_idx,i]) for i in range(self.ncols)])
            ofile.write(line + endline)
            if(all_lines):
                ofile.write("\\hline\n")
            elif(idx < len(rlines) and rownr == rlines[idx]):
                idx += 1
                ofile.write("\\hline\n")
            rownr += 1
        if(rlines[-1]==-1):
            ofile.write("\\hline\n")
            
        ofile.write(r"\end{tabular}")
        ofile.close()
        
class DataFrameToLaTeX(__ToLaTeX__):
    def __init__(self, df, include_headers=True, include_index=True, headers=None):
        if(df.ndim!=2):
            raise ValueError("Expected dataframe of dimension 2, got " + str(df.ndim))
        ncols = df.shape[1]
        if(include_index): ncols += 1
        if(headers is None):
            headers = [str(c) for c in df.columns]
            if(include_index):
                headers = [""] + headers
        else:
            if(len(headers)!=ncols):
                if(len(headers)==ncols-1):
                    headers = [""] + headers
                else:
                    raise ValueError("Number of given headers does not match number of columns")
        super().__init__(ncols, headers)
        self.set_include_headers(include_headers)
        self.include_index = include_index
        self.df = df
        if(include_index):
            self.index_formatter = str
        
    def set_index_formatter(self, fmt):
        self.index_formatter = fmt
        
    def tolatex(self, fname):
        ofile = open(fname, 'w')
        all_lines, rlines, headers = self.__construct_headers__()
        ofile.write(headers)
        endline = r"\\" + "\n"
        
        rownr = 0
        idx = 0
        for row_idx in range(self.df.shape[0]):
            line = " & ".join([self.formatters[i](self.df.iloc[row_idx,i]) for i in range(self.df.shape[1])])
            if(self.include_headers):
                line = self.index_formatter(self.df.index[row_idx]) + " & " + line
            ofile.write(line + endline)
            if(all_lines):
                ofile.write("\\hline\n")
            elif(idx < len(rlines) and rownr == rlines[idx]):
                idx += 1
                ofile.write("\\hline\n")
            rownr += 1
        if(rlines[-1]==-1):
            ofile.write("\\hline\n")
            
        ofile.write(r"\end{tabular}")
        ofile.close()