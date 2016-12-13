"""Some simple symmetric array classes

This module defines two symmetric array classes, SymmetricArray (NxN) and SymmetricArray3d (NxNxN),
which are meant to be used in place of numpy arrays where the arrays they 
represent where there are symmetric elements that have the same value in array. These 
symmetric arrays classes only store the unique values of the array and therefore use 
just over half the memory of the full numpy array version. 
E.g. a SymmetricArray(10) object (representing a 10x10 symmetric array) 
stores the (10**2 + 10)/2 = 55 unique values instead of the full 100.  
 
Examples:
    >> import SymmetricArray as symarr
    >> sym_array_a = symarr.SymmetricArray(10)
    >> print sym_array_a
    Representation of a 10x10 array where array[i,j] = array[j,i] with 55 unique values.
    >> sym_array_a[1, 9] = 1.0
    >> print sym_array_a[9, 1]
    1.0
        
    >> sym_array_b = symarr.SymmetricArray3d(10)
    >> print sym_array_b
    Representation of a 10x10x10 array where array[i,j,k] = array[j,i,k] with 550 unique values.
    >> 
    >> sym_array_b[1, 9, 2] = 5.0
    >> print sym_array_a[9, 1, 2]
    5.0
    
    >> import numpy as np
    >> sym_array_c = symarr.SymmetricArray(10, fill_function=np.full, 5, dtype=np.int)
    >> print sym_array_c[1,5]
    5
    >> print sym_array_c[1,5]
    5
  
"""

#imports
import numpy as np
import sys


# NxN symmetric array
class SymmetricArray:
    """ NxN symmetric array object    
    An array object for the case of NxN array where a[i,j] = a[j,i]. An array of this
    will have (N**2 + N)/2 unique values, which is a little over half the total values 
    in the full NxN array. This class takes advantage of this by essentially building 
    a triangle matrix with only the unique values.  
                    
    """
    def __init__(self, N, fill_function=np.zeros, *args, **kwargs):
    """ Initialization of the SymmetricArray object.  

        Args:
            N (int): Defines the shape of the array, i.e. NxN.   
            fill_function (np.array_builder, optional): Set the np.array function to use to
                fill the array.  The default is numpy.zeros, which will fill the array with zeros.
                Other options include numpy.full and numpy.random.random.  
            *args (optional): Additional arguments to be passed to the fill_function
            **kwargs (optional): Additional keyword arguments to be passed to the fill_function.
        
        Attributes:
            nframes (int): The number Frame objects being stored.
            pid (int): The process id that the frames object is created in.
            path (str): The path to where the shelved Frame data is stored.
            save (bool): Set whether to save the shelved Frame data after frames object deletion. 
            fs_name (str): The base name of the shelve database file used to store Frame objects.
            frame_shelf (shelve.Shelf): The Shelf that will hold the Frame objects.
        """
        self.unique = (N**2 + N)/2
        self.shape = N
        self.values = []
        self.sm1 = N-1
        #print "fill_func_args", args
        #print "fill_func_kwargs", kwargs
        #check the fill function
        for i in xrange(N):
            self.values.append(fill_function((N-i), *args, **kwargs ))
        self.dtype = self.values[0].dtype

        return

    def __getitem__(self, keys):
        if isinstance(keys, int):
            raise IndexError('Index '+str(keys)+' has the wrong number of keys.')
            return
        elif len(keys) != 2:
            raise IndexError('Index '+str(keys)+' has the wrong number of keys.')
            return
        for key in keys:
            if (key > self.sm1):
                raise IndexError('Index '+str(key)+' is out of range.')
                return
        value = self.getitem(keys[0], keys[1])
        return value
        
    def __setitem__(self, keys, value):
        if isinstance(keys, int):
            raise IndexError('Index '+str(keys)+' has the wrong number of keys.')
            return
        elif len(keys) != 2:
            raise IndexError('Index '+str(keys)+' has the wrong number of keys.')
            return
        for key in keys:
            if (key > self.sm1):
                raise IndexError('Index '+str(key)+' is out of range.')
                return

        self.setitem(keys[0], keys[1], value)
        return

    def getitem(self, keya, keyb):
        if (keya > self.sm1):
            raise IndexError('Index '+str(keya)+' is out of range.')
            return
        elif (keyb > self.sm1):
            raise IndexError('Index '+str(keyb)+' is out of range.')
            return
        key_arr = [keya, keyb]
        mink = min(key_arr)
        maxk = max(key_arr)
        return self.values[mink][maxk-mink]

    def setitem(self, keya, keyb, value):
        if (keya > self.sm1):
            raise IndexError('Index '+str(keya)+' is out of range.')
            return
        elif (keyb > self.sm1):
            raise IndexError('Index '+str(keyb)+' is out of range.')
            return
        key_arr = [keya, keyb]
        mink = min(key_arr)
        maxk = max(key_arr)
        self.values[mink][maxk-mink] = value
        return

    # basic += to add some constant value to all elements
    def __iadd__(self, value):
        for i in xrange(self.shape-1):
            for j in xrange(i+1, self.shape):
                self[i, j] = value 
                
        return
        
    #build and return the full NxN numpy array version
    def full(self):
        outarr = np.zeros((self.shape, self.shape))
        for i in xrange(self.shape-1):
            for j in xrange(i+1, self.shape):
                value = self[i, j] 
                outarr[i][j] = value
                outarr[j][i] = value
        return outarr

    def __len__(self):
        return self.unique

    def __repr__(self):
        return "Representation of an "+str(self.shape)+"x"+str(self.shape)+" array where array[i,j] = array[j,i] with "+str(self.unique)+" unique values."
    
    def __str__(self):
        return "Representation of an "+str(self.shape)+"x"+str(self.shape)+" array where array[i,j] = array[j,i] with "+str(self.unique)+" unique values."


#this array class is symmetric in the first two 
# indices, i.e. the first two indices are interchangeable
# or a.getitem(i, j, k) = a.getitem(j, i, k).
#  
class SymmetricArray3d:

    def __init__(self, N, fill_function=np.zeros, *args, **kwarg):
        self.unique = ((N**2 + N)/2)*N
        self.shape = N
        self.values = []
        self.sm1 = N-1
        for i in xrange(N):
                self.values.append(fill_func((N-i, N), *args, **kwargs))
        self.dtype = self.values[0].dtype

        return

    def getitem(self, keya, keyb, keyc):
        if (keya > self.sm1):
            raise IndexError('Index '+str(keya)+' is out of range.')
            return
        elif (keyb > self.sm1):
            raise IndexError('Index '+str(keyb)+' is out of range.')
            return
        elif (keyc > self.sm1):
            raise IndexError('Index '+str(keyc)+' is out of range.')
            return
        key_arr = [keya, keyb]
        mink = min(key_arr)
        maxk = max(key_arr)
        return self.values[mink][maxk-mink][keyc]

    def setitem(self, keya, keyb, keyc, value):
        if (keya > self.sm1):
            raise IndexError('Index '+str(keya)+' is out of range.')
            return
        elif (keyb > self.sm1):
            raise IndexError('Index '+str(keyb)+' is out of range.')
            return
        elif (keyc > self.sm1):
            raise IndexError('Index '+str(keyc)+' is out of range.')
            return
        key_arr = [keya, keyb]
        mink = min(key_arr)
        maxk = max(key_arr)
        self.values[mink][maxk-mink][keyc] = value
        return

    def total_size(self):
        total = 0
        for array in self.values:
            size_array = sys.getsizeof(array)
            total+=size_array
        return total

    def __getitem__(self, keys):
        if isinstance(keys, int):
            raise IndexError('Index '+str(keys)+' has the wrong number of keys.')
            return
        elif len(keys) != 3:
            raise IndexError('Index '+str(keys)+' has the wrong number of keys.')
            return
        for key in keys:
            if (key > self.sm1):
                raise IndexError('Index '+str(key)+' is out of range.')
                return
        
        value = self.getitem(keys[0], keys[1], keys[2])
        return value
        
    def __setitem__(self, keys, value):
        if isinstance(keys, int):
            raise IndexError('Index '+str(keys)+' has the wrong number of keys.')
            return
        elif len(keys) != 3:
            raise IndexError('Index '+str(keys)+' has the wrong number of keys.')
            return
        for key in keys:
            if (key > self.sm1):
                raise IndexError('Index '+str(key)+' is out of range.')
                return
        self.setitem(keys[0], keys[1], keys[2], value)
        return

    def __len__(self):
        return self.unique

    def __repr__(self):
        return "Representation of an "+str(self.shape)+"x"+str(self.shape)+"x"+str(self.shape)+" array where array[i,j,k] = array[j,i,k] with "+str(self.unique)+" unique values."
    
    def __str__(self):
        return "Representation of an "+str(self.shape)+"x"+str(self.shape)+"x"+str(self.shape)+" array where array[i,j,k] = array[j,i,k] with "+str(self.unique)+" unique values."
