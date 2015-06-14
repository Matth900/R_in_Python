# Data Frames - Only Rectangular LIST of LISTS - See (R) - BETA Version - Written by Mattia Pennacchietti
# The purpose is to manage tables of heterogenous Arrays. Not for computing purposes
# Use together with other R-Like utilities (Mattia_lists)

import re # REGEX- Regular expression module, will be used to identify patterns when subsetting - (__getiem__ overloading)
from Mattia import * #import mattia_list


class data_frame:


    def __init__(self, l =[[]] ,row_names ='',col_names=''):
        
         # (l) must be a LIST of list 
        self.df = l
      
        lengths = set(len(el) for el in self.df)

        
        if len(lengths)>1:
            
            self.df = [[]]
            
            print ('Error! All the  elements  of the list must be a data')
            
        else:

            self.df = l
            
            self.nrows = list(lengths)[0]
            
            self.ncols = len(l)

            # Row and Column NAMES, if the user has provided no names ("") by default these are just numbers
            
            if row_names == '':

                self.rnames = range(1,self.nrows+1)

            else:

                # Check the User has actually provided row names for all the rows, if more names throw an error, otherwise fill with normal range

                if type(row_names) == list and len(row_names) == self.nrows:

                    self.rnames = row_names

                elif type(row_names) == list and len(row_names) > self.nrows:

                    print 'Error! You supplied too many names for the rows of this Data Frame'

                elif type(row_names) == list  and len(row_names) < self.nrows:

                    remaining_rows = self.nrows - len(row_names)
                    self.rnames = row_names + list(range(len(row_names)+1,self.nrows+1))

            if col_names == '':

                self.cnames = range(1,self.ncols+1)

            else:

                # Check the User has actually provided column names for all the rows, if more names throw an error, otherwise fill with normal range

                if type(col_names) == list and len(col_names) == self.ncols:

                    self.cnames = col_names

                elif type(col_names) == list and len(col_names) > self.ncols:

                    print 'Error! You supplied too many names for the columns of this Data Frame'

                elif type(col_names) == list and len(col_names) < self.ncols:

                    remaining_cols = self.ncols - len(col_names)
                    self.cnames = col_names + list(range(len(col_names)+1,self.ncols+1))



    def __str__(self):

        # Printing Column LABELS

        out = ''
        
        for j in range(1,self.ncols+1):

            if j < (self.ncols):

                out = out + '\t' + str(self.cnames[j-1]) + ':'

            else:

                out = out + '\t' + str(self.cnames[j-1]) + ':' + '\n'

        # Filling the Data Frame - Note that we fill BY COLLUMN


        
        for i in range(self.nrows):

            for j in range(self.ncols+1):

                if j == 0:

                    out = out + str(self.rnames[i]) + ': \t'

                elif j == self.ncols:

                    out = out + str(self.df[j-1][i]) + '\n'

                else:

                    out = out + str(self.df[j-1][i]) + '\t'
                        
            
        return out

    # Overloading the subsetting operator []: __getitem__

    def __getitem__(self,dims):

        #============= 1st CASE: Dims = Tuple =====================================================================
        # dims can be a tuple (i,j) - i= rows, j= columns. 
        # dims can be df(i,'r') ---- df(j,'c') where ('r') and ('j') stands for columns to retrieve single rows or col
        # dims can be a tuple made of one or two slice objects (e.g. 1:, 1:2, :, ecc)

        if type(dims) == tuple or type(dims) == list:

            if (type(dims[0]) == int and type(dims[1]) == int) and (dims[0] <= self.nrows and dims[1] <= self.ncols):

                # Returning a single element
                
                return self.df[dims[1]-1][dims[0]-1]

            elif type(dims[1]) == str:

                if dims[1] == 'r' or str(dims[1]) == ':' :

                    # Returning a List
                    
                    return [el[dims[0]-1] for el in self.df]

                elif dims[1] == 'c' or str(dims[1]) == ':' :


                    # Returning a List
                    
                    return self.df[dims[0]-1]

                else:

                    print('For subsetting a whole column or row, choose after the first index, either "c" or "r"')


            # When slicing remember Python rules: [i:j] => (i:j], from but not including (i) until and including (j)
            
            elif type(dims[0]) == slice and type(dims[1]) == int:

                # Slicing rows with fixed Columnn
                #temp = data_frame([el[dims[0]] for el in self.df])
                
                if dims[0].start == None and dims[0].stop == None:

                    temp = data_frame([el[dims[0]] for el in self.df])

                else:

                    new_slice = slice(dims[0].start-1,dims[0].stop)
                    temp = data_frame([el[new_slice] for el in self.df])
                    
                # Returning a List
                
                return temp[dims[1],'c']

            elif type(dims[0]) == int and type(dims[1]) == slice:

                # Slicing columns with fxed Rows

                if dims[1].start== None and dims[1].stop== None:

                    temp = self.df[dims[1]]

                else:
                    
                    new_slice = slice(dims[1].start-1,dims[1].stop)
                    temp = self.df[new_slice]
                    
                # Returning a List
                
                return [el[dims[0]-1] for el in temp]

            elif type(dims[0]) == slice and type(dims[1]) == slice:

                # Slicing columns
                
                if dims[1].start == None and dims[1].stop == None:

                    temp1 = data_frame(self.df[dims[1]])

                else:
                    
                    slice1 = slice(dims[1].start-1,dims[1].stop)
                    temp1 = data_frame(self.df[slice1])
                
                # Slicing rows
                
                if dims[0].start == None and dims[0].stop == None:

                    temp2 = data_frame([el[dims[0]] for el in temp1.df])

                else:
                    
                    slice0 = slice(dims[0].start-1,dims[0].stop)
                    temp2 =data_frame([el[slice0] for el in temp1.df])
                    
                # Returning a Data_Frame
                
                print temp2
                return temp2

            else:

                print('Error! Not valid indices. Make sure they are integers and within the bounds of the dataframed')

        else:

            print type(dims[0])
            print type(dims[1])
            print('Error! Not valid indices. Select two indices (i,j) for row and column number')
            

    # Implementing some other (R) subsetting and viewing functions as Head,Tail ecc

    def head(self,value = 1):

        # Checking first that the threshold for the head does not go beyond the number of rows of the data frame

        if value > self.nrows:

            print('Error! You selected more rows than those of the Data Frame. Choose a lower value')

        else:
            
            temp = data_frame([el[:value] for el in self.df])
        
            return temp
        # (value) is here to be understood as the number of first rows we want to visualize. By default we set it to 1


    def tail(self, value = 1):

        # Checking first that the threshold for the tail does not go beyond the number of rows of the data frame

        if value > self.nrows:

            print('Error! You selected more rows than those of the Data Frame. Choose a lower value')

        else:
            
            temp = data_frame([el[len(el)-value:] for el in self.df])

            return temp
        
        # (value) is here to be understood as the number of last rows we want to visualize. By default we set it to 1

    
    # Some SQL-Like / Relational Algebra statement to select only some rows within the data frame
    def select(self,col ='', cond_operator='', value='', out=0):

    # The condition must be written between quotes and must 
        '''

    The select statement resembles what is done in SQL, Relational Algebra.

    COL : Indicates the column upon which we want to verify the condition
    COND_OPERATOR : Indicates what logical operator we want apply on the row of the column
    VALUE : Indicates the value to supply the logical condition
    OUT  : Indicates the columns we want to see, from the filtered relation coming out of the query

    '''

        # WORK IN PROGRES!!! NOT FINISHED-----------------------------------------------------------------
        # Probably have to use mattia_lists

        # STEP 1 - Creating mattia_lists from the DataFrame

        # Generator of Mattia Lists
        m_lists = list(mattia_list(el, which_method='i') for el in self.df)

        # Note how we choose the which method (i) so that indices instead of booleans are returned

        col_index = self.cnames.index(col)
        column = m_lists[col_index]
        #print column.list

        if str(cond_operator) == 'equal':

            indices =  column == value


        elif str(cond_operator) == 'less_equal':

            indices = column <= value

        elif str(cond_operator) == 'less':

            indices = column < value

        elif str(cond_operator) == 'greater_equal':

            indices = column >= value

        elif str(cond_operator) == 'greater':

            indices =  column > value

        elif str(cond_operator) == 'not_equal':
        
            indices =  column !=value

        else:

            print 'Error! Invalid logical operator'


        # STEP 2 - Create the temp1 DataFrame made of the rows which satisfy the condition and ALL the columns
        
        temp0 = [[el[ind] for ind in indices] for el in self.df]
        temp1 = data_frame(temp0)
       
        # STEP 3 - Create the temp2/Final DataFrame selecting only the columns the user wants to see
        # Such columns can be indicated through single integers or names or lists of them or even slices objects
        # Supported implementation at June 2015: Only integers, list of integers
        view_columns = []
        if type(out) == list:
            
            view_columns.extend(out)

        else:

            view_columns.append(out)

        temp2 = data_frame([temp1.df[o-1] for o in view_columns])
        print temp2

        # ======================= SOME OLD STUFF =============================

        # DataFrame out of Mattia Lists
        #temp0 = [el.list for el in m_lists]
        #m_dframe = data_frame(temp0)
        #print m_dframe
                
        #lengths = [len(el) for el in self.df]
        
        #temp1 = []
        
        #for el in self.df:
            
            #temp1.append([el[i] for i in range(lengths[0]) if el[i] != None])
            
        #temp2 = data_frame(temp1)
        
        #print(temp1)


# =========================================END OF CLASS DATA.FRAME ===================================

# ===================================HELPER FUNCTIONS TO USE THE DATA.FRAME===========================


def tail(data_frame,value):

    temp = data_frame.tail(value)
    print temp

def head(data_frame, value):

    temp = data_frame.head(value)
    print temp

def SQL(query):

    # The query is a string which must respect the following format:
    # SELECT columns FROM Data_Frame WHERE rows_condition

    # Implementation through REGULAR EXPRESSIONS
    col_regex = 'SELECT (.+) FROM .+ WHERE .+'
    col = re.findall(col_regex,query)[0]
    
    df_regex = 'SELECT .+ FROM (.+) WHERE .+'
    df = re.findall(df_regex,query)
    
    col_cond_regex = 'SELECT .+ FROM .+ WHERE (.+) .+ .+'
    col_cond = re.findall(col_cond_regex,query)[0]

    op_cond_regex = 'SELECT .+ FROM .+ WHERE .+ (.+) .+'
    op_cond = re.findall(op_cond_regex,query)[0]

    value_cond_regex = 'SELECT .+ FROM .+ WHERE .+ .+ (.+)'
    value_cond = re.findall(value_cond_regex,query)[0]

    #select(self,col ='', cond_operator='', value='', out=0)
    #df.select(col_cond,op_cond,value_cond,col)
    
    data= globals()[df[0]]
    
    data.select(int(col_cond),op_cond,value_cond,int(col))

# ======================================== TESTING ===================================================


#Test0
#a=data_frame([[1,True,False,'Hello','World',None,False],[4,'AAPL',None,'LNKD','TWTR','FB','MS'],['BAC','DB','C',True,False,None,'BX']],['A','B','C','D','E','F','G'],['STOCK1','STOCK2','STOCK3'])      


#Test1
a=data_frame([[1,True,False,'Hello','World',None,False],[4,'AAPL',None,'LNKD','TWTR','FB','MS'],['BAC','DB','C',True,False,None,'BX']])

