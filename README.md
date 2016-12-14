Python symmetric array classes. 

These array objects are meant to be used as a reduced memory storage option for things like NxN linear pair correlation matrices, which are symmetric about their diagonals.

The objects are meant to be layered over numpy arrays, although the initialization should 
allow for the use of other containers that have callable initialization fucntions take an integer or tuple shape argument and 
have a dtype attribute. 
 
This module defines two symmetric array classes, SymmetricArray (NxN) and SymmetricArray3d (NxNxN),
which are meant to be used in place of numpy arrays where there are symmetric elements in the array they represent that have the same value.  These symmetric arrays classes only store the unique values of the array and therefore use just over half the memory of the full numpy array version. 

E.g. a SymmetricArray(10) object (representing a 10x10 symmetric array) 
stores the (10**2 + 10)/2 = 55 unique values instead of the full 100. 

Requires:
    NumPy 

  
