# Data Frames - Only Rectangular LIST of LISTS - See (R) - BETA Version - Written by Mattia Pennacchietti
# The purpose is to manage tables of heterogenous Arrays. Not for computing purposes
# Use together with other R-Like utilities (Mattia_lists)

import re # REGEX- Regular expression module, will be used to identify patterns when subsetting - (__getiem__ overloading)
from Mattia import * #import mattia_list


class data_frame:


    def __init__(self, l =[[]] ,row_names ='',col_names='', key=''):
        
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

            # CHECKING THE KEY IF THE USER HAS PROVIDED ONE

            if key != '':

                if key in self.cnames:

                    self.check_key(self.df[self.cnames.index(key)])

                else:

                    print 'Wrong KEY! Wrong Column(s) name(s)'


    def check_key(self,key):

        # function to be called within __init__() initialization method

        # We use here the helper function (defined outside this class) duplicates()

        if duplicates(key) == True:

            print 'Error! Key not valid. There are multiple entries with the same value.'
            print 'That is not allowed for a primary key. Change column or use a combination of columns'

        else:

            pass
        
    
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

    # Appending new columns to the DataFrame

    def insert(self,new_list, by = 'col', fill_with_None = True):

        # by : indicates how we want to append the new list to the DataFrame, either by column or by row. The default option is by column

        if by == 'col':

            # Check that the new column has all the number of rows required, otherwise fill with None if less and if attribute set to true. Otherwise, error

            if len(new_list) < self.nrows:

                new_list.extend([None]*(self.nrows-len(new_list)))
                
                self.df.append(new_list)
                
                self.ncols +=1
                
                self.cnames.append(self.ncols)

            elif len(new_list) > self.nrows:

                print 'Error! The new column has too many rows'

            else:

                self.df.append(new_list)
                
                self.ncols += 1
                
                self.cnames.append(self.ncols)
                

        elif by == 'row':

            if len(new_list) < self.ncols:

                new_list.extend([None]*(self.ncols-len(new_list)))

                ind = 0

                for col in self.df:

                    col.append(new_list[ind])

                    ind += 1
                    

            elif len(new_list) > self.ncols:

                print 'Error! The new row has too many entries'

            else:

                ind = 0

                for col in self.df:

                    col.append(new_list[ind])
                    
                    ind += 1

            # Updating number of rows and their names
            
            self.nrows +=1
            
            self.rnames.append(self.nrows)
    

    # Removing either columns or rows from the dataframe

    def eliminate(self, col ='',row = ''):

        # (col) & (row) represents respectively the column and/or row names we want to eliminate
        
        # Remember the two List Methods to remove elements: 1)list.remove(elem_name) -- 2) del list[elem_index]
        
        # 1) PROCESS COLUMNS

        if col != '':

            if type(col) == list:

                for el in col:

                    ind = self.cnames.index(el)

                    del self.df[ind]

                    self.ncols -=1

                    del self.cnames[ind]

            elif type(col) == int or type(col) == str:
                
                if  col in self.cnames:

                    # STEP 1 - Find the corresponding index/indices to the name/s supplied by the user

                    ind = self.cnames.index(col)
                    
                    del self.df[ind] # Remember Python starts counting elements of a list from zero

                    self.ncols -=1

                    del self.cnames[ind]

                else:

                    print 'Error! The columns you want to delete do not correspond to those of the Data Frame. Select the appropriate names!' 

            else:

                print 'Error! Please choose either a single column and its name or multiple columns using a list of their names'


        # 1) PROCESS ROWS

        if row != '':

            if type(row) == list:

                for el in row:

                    for el_2 in self.df:

                        ind = self.rnames.index(el)

                        del el_2[ind]

                    self.nrows -=1

                    del self.rnames[ind]

            elif type(row) == int or type(row) == str:
                
                if row in self.rnames:

                    for el in self.df:

                        ind = self.rnames.index(row)

                        del el[ind]

                    self.nrows -= 1

                    del self.rnames[ind]

                else:

                    print 'Error! The rows you want to delete do not correspond to those of the Data Frame. Select the appropriate names!' 

            else:

                print 'Error! Please choose either a single column and its name or multiple columns using a list of their names'


    # ========================================== SQL Methods for DATA FRAME CLASS ===========================================

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
        
        return temp2

        # ======================= SOME OLD STUFF =============================

        # DataFrame out of Mattia Lists
        # temp0 = [el.list for el in m_lists]
        # m_dframe = data_frame(temp0)
        # print m_dframe
                
        # lengths = [len(el) for el in self.df]
        
        # temp1 = []
        
        # for el in self.df:
            
            # temp1.append([el[i] for i in range(lengths[0]) if el[i] != None])
            
        # temp2 = data_frame(temp1)
        
        # print(temp1)


    def unique_rows(self):

        # Keep track of duplicate rows

        temp_duplicates = []

        # Extract first all the rows from the Data Frame

        rows = [[ el[i] for el in self.df] for i in range(self.nrows)]

        for r in rows:

            for r2 in range(rows.index(r)+1,self.nrows):

                if (r == rows[r2]) == True:

                    temp_duplicates.append(r2)

        duplicates = temp_duplicates[::2]

        print duplicates

        self.eliminate(row=duplicates)

        print self

    # ======================================== JOIN METHODS ==========================================

    def join(self, other, col_name, typ = 'std'):

        # Other =  The other data_frame with which we want to make the join
        # The column name for making the join (NOTE! This must be the same in both Data Frames!!)
        # Possible type of joins are 1)std (default); 2)left; 3)right; 4)self

        output_query = [] # This will contain a list of rows for which column entries match and will be the basis for the output Data Frame
        
        if typ == 'std':

            if (col_name in self.cnames) and (col_name in other.cnames):

                rows_df1 = [[ el[i] for el in self.df] for i in range(self.nrows)]
                
                rows_df2 = [[ el[i] for el in other.df] for i in range(other.nrows)]

                for r1 in rows_df1:

                    for r2 in rows_df2:

                        if r1[self.cnames.index(col_name)] == r2[self.cnames.index(col_name)]:

                            output_query.append(r1+r2)

                # Create a Resulting Data Frame out of the new created tuples

                joined_df = data_frame([[el[j] for el in output_query] for j in range(self.ncols+other.ncols)])

                # Re-Labelling (ONLY COLUMNS) of the new MERGED DataFrame

                labels_self = ['A.{}'.format(name) for  name in self.cnames]

                labels_other = ['B.{}'.format(name) for name in other.cnames]

                labels_joined = labels_self+labels_other # Concatenating the two lists of  labes (column names)

                joined_df.cnames = labels_joined

                print joined_df

                return joined_df

            else:
                
                print 'Error! You have not selected a valid column to make the join'
                print other
        

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
    
    result = data.select(int(col_cond),op_cond,value_cond,int(col))

    print result


# A Powered version of the former SQL Function to enable for more conditions and more columns projections

def SQL2(query):

    # The query is a string which must respect the following format:
    # SELECT columns FROM Data_Frame WHERE rows_condition

    # Implementation through REGULAR EXPRESSIONS

    # MULTIPLE COLUMNS (sep = ',')
    cols_regex = 'SELECT (.+) FROM .+ WHERE .+'
    
    cols = re.findall(cols_regex,query)[0]
    
    cols = str(cols).split(',')

    # NO MULTIPLE DATAFRAMES
    df_regex = 'SELECT .+ FROM (.+) WHERE .+'
    
    df = re.findall(df_regex,query)
    
    # MULTIPLE CONDITIONS - DEFAULT = (AND) CONDITIONS [Separator = ',']
    cond_regex = 'SELECT .+ FROM .+ WHERE (.+)'
    
    cond = re.findall(cond_regex,query)[0]
    
    cond = str(cond).split(',')
    
    temp_cond = [el for el in cond]

    conditions = [el.split(' ') for el in temp_cond]

    temp_df= globals()[df[0]]

    # EXECUTING THE QUERY

    # STEP 1: IMPLENT THE METHOD SELECT AS DEFINED IN THE DATA_FRAME CLASS. INCLUDE ALL COLUMNS FOR NOW

    for num_cond in range(len(conditions)):

        # Remember that the value we use to test the condition could be (almost always) a number, a string, a Boolean, or a None Type
        # The problem is that the REGEX use to capture it

        if (conditions[num_cond][2]) == 'True':

            value = True

        elif conditions[num_cond][2] == 'False':

            value = False

        elif conditions[num_cond][2] == 'None':

            value = None

        else:

            try:
                        
                value = float(conditions[num_cond][2])

            except:

                value = conditions[num_cond][2]
                        
        
        temp_df = temp_df.select(int((conditions)[num_cond][0]),(conditions)[num_cond][1],value,temp_df.cnames)

    # STEP 2: PROJECT COLUMNS ON THE RESULTING RELATION FROM THE APPLIED CONDITIONS

    temp_df = data_frame([temp_df.df[int(proj_col)-1] for proj_col in cols])
            
    print temp_df



# An helper function to spot duplicate elements within a list

def duplicates(lst):

    # Argument  is simply a list

    for el_i in lst:

        for j in range(lst.index(el_i)+1,len(lst)):

            if el_i == lst[j]:

                return True

# ======================================== TESTING ===================================================

#Test1
a=data_frame([[10,2,False,'Hello','World',None,False],['Why',14,None,'LNKD','AS','FB','MS'],[2,False,'C',True,'ADB',None,'BX']])

#Test2
b=data_frame([[4,8,'Pie','Matth',True,'ABC',False],['What',6,True,'BAC','LNKD','FB','MS'],[14,4,'C',True,True,None,'BX']])

