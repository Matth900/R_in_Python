# Utilities - Mattia Pennacchietti - Beta Version
# Userful methods for lists to be treated as in (R)

class mattia_list():

    '''
    ========================= DOCUMENTATION =======================
    Some useful methods for lists subsetting, grouping, comparisons
    Logical comparisons similar to R, as well as naming features
    ===============================================================
    '''

    def __init__(self,init,names = '' ,which_method='b'):

        self.list = init

        # Names are the strings lists with which we identify Lists elemetnsng. They must be lists of strings
        
        names_correct = []
        
        if type(names) != list:

            if type(names) == str:

                names_correct.append(names)

            else:

                print 'Error! One name supplied which is not a valid string'

        else:

            for each_name in names: 

                if type(each_name) == str:

                    names_correct.append(each_name)

                else:

                    print 'Detected One element which is not a valid string'
                    names_correct = []
                    break


        self.names = names_correct
        

        # Which Method = This indicates whether when comparing list with a number or string the returning list is of logicals
        # or of integers representing indices. This must be either b = booleans, i = indices. Boolean by default

        if which_method == 'b' or which_method== 'i':

            self.which = which_method

        else:

            print 'Error! Which method must be either (b) for boolean, or (i) for indices'
      

    # Divide a list into a group of a certain number of itmes sequentially - (m) stands for number of grouping elements
    
    def groupby(self,m, direction = 'left'):

        if direction == 'left':

            d = 1

        elif direction == 'right':

            d = -1

        else:

            print 'Error! The direction supplied is wrong! Choose (left/right)'

            
        temp =[[sub for sub in self.list[d*m*i:d*m*(1+i)]] for i in range(0,len(self.list)/m)]
        remaining = len(self.list)%m

        if remaining > 0:
            
            temp.append(self.list[d*-remaining:])

        return temp


    # Overloading for slicing the list for the an instance of the Mattia_list : operator [] - __getCtem__ to use Lists as subsetting items
    # if you want to subset lists as usual simply do [] on instance_name.list

    def __getitem__(self, list_ind):

        #Creating the list types of the list index
        types = []
        
        subsetted = []

        if type(list_ind) != list:

            print 'Error! input must be a list! Use [[]] also for single elements'

        # Check if all the items of the list are of the same type. 
        else:

            for element in list_ind:
                
                types.append(type(element))

            if types== [type(list_ind[0]) for i in range(1,len(list_ind)+1)]:

                b = 0 # This is for keeping track of boolean positions
                
                for logic in list_ind:

                    if type(logic) == bool:

                        #return [el for el in self.list if ind[self.list.index(el)]== True]
                        if logic:
                            
                            subsetted.append(self.list[b])

                        b +=1                            
                        
                    elif type(logic) == int:

                        subsetted.append(self.list[logic])

                    elif type(logic) == str :

                        if logic in self.names:

                            subsetted.append(self.list[self.names.index(logic)])

                        else:

                            print 'No element with this attribute name'
            else:

                print "The subsetting list must contain elements of the same type!!"
                

            return subsetted
            #return types
            #return list_index
        
    # Overloading some logical operators (<,<=,==,!=,>=,>) when comparing list with a Scalar Number or String. Returns list of boolean
    # or positions of those elements which satisfy the condition. Which of the two methods depends on User preference when setting the
    # Mattia List
    
    def __eq__(self,value): # Overloading of the (==) operator; (value) stands for the value we want to match our list with 

        if self.which == 'b':
        
            return [(el==value) for el in self.list]

        else:

            iterator = [(i,j) for i,j in ((self.list[ind],ind) for ind in range(len(self.list)))]
            return [self.list.index(el,n) for el,n in iterator if el==value]

    def __ne__(self,value): # Overloading of the (!=) operator; (value) stands for the value we want to match our list with

        if self.which == 'b':

            return [(el!=value) for el in self.list]

        else:

            iterator = [(i,j) for i,j in ((self.list[ind],ind) for ind in range(len(self.list)))]
            return [self.list.index(el,n) for el,n in iterator if el!=value]   
            
    

    def __lt__(self,value): # Overloading of the (<) operator; (value) stands for the value we want to match our list with 

        if self.which == 'b':

            return [(el<value) for el in self.list]

        else:

            iterator = [(i,j) for i,j in ((self.list[ind],ind) for ind in range(len(self.list)))]
            return [self.list.index(el,n) for el,n in iterator if el<value]   
            
    

    def __le__(self,value): # Overloading of the (<=) operator; (value) stands for the value we want to match our list with 

        if self.which == 'b':

            return [(el<=value) for el in self.list]

        else:

            iterator = [(i,j) for i,j in ((self.list[ind],ind) for ind in range(len(self.list)))]
            return [self.list.index(el,n) for el,n in iterator if el<=value]  

    
    def __gt__(self,value): # Overloading of the (>) operator; (value) stands for the value we want to match our list with 

        if self.which == 'b':

            return [(el>value) for el in self.list]

        else:

            iterator = [(i,j) for i,j in ((self.list[ind],ind) for ind in range(len(self.list)))]
            return [self.list.index(el,n) for el,n in iterator if el>value]
            


    def __ge__(self,value): # Overloading of the (>=) operator; (value) stands for the value we want to match our list with 

        if self.which == 'b':

            return [(el>=value) for el in self.list]

        else:
            
            iterator = [(i,j) for i,j in ((self.list[ind],ind) for ind in range(len(self.list)))]
            return [self.list.index(el,n) for el,n in iterator if el>=value]
    


    # Overloading + and * operators to work with lists of any element - this will yield List of Lists 

    def __add__(self,value):

        # value is here intended to be an list of the same dimension

        if len(self.list) != len(value):

            print 'Error! The two lists must have equal length'

        else:

            return [[i,j] for i,j in ((self.list[ind],value[ind]) for ind in range(len(self.list)))]

    def __mul__(self,value):

        # value is here intended to be an list of the same dimension

        if len(self.list) != len(value):

            print 'Error! The two lists must have equal length'

        else:

            return [[i,j] for i,j in ((self.list[ind1],value[ind2]) for ind1 in range(len(self.list)) for ind2 in range(len(self.list)))]


    # Re-converting to normal lists
    
    def tolist(self):

        return list(el for el in self.list)


    # Overloading the str and print statement

    def __str__(self):

        try:
            
            return str(self.list)

        except:

            print 'Object is not a Mattia_list'




#=================================== END OF THE CLASS ===========================================



#==================================== Additional functions for mattia_lists======================
def names(mattia_list):

    try:
        
        return mattia_list.names

    except:


        print 'Objet is not a Mattia_list'


#=================================== SOME TESTING ================================================
a = mattia_list(['AAPL','MSFT','LNKD','TWTR'],['stock1','stock2','stock3','stock4'])
#b = a.groupby(2)
#d = a == 'APL'
#e = a[a=='Mattia']



