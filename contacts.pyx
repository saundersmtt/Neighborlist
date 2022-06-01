import numpy as np
import sys
from libc.stdlib cimport malloc, free
from libc.string cimport strcmp

cdef extern from "math.h":
    double sqrt(double m)

cdef extern from "Python.h":
    const char* PyUnicode_AsUTF8(object unicode)

cdef char ** to_cstring_array(list_str):
    cdef char **ret = <char **>malloc(len(list_str) * sizeof(char *))
    for i in range(len(list_str)):
        ret[i] = PyUnicode_AsUTF8(list_str[i])
    return(ret)

cdef char * to_cstring(_str):
    cdef char *ret = <char *>malloc(len(_str) * sizeof(char *))
    ret = PyUnicode_AsUTF8(_str)
    return(ret)

cpdef double distance(float[:] vector1, float[:] vector2):
    cdef double dist = sqrt((vector1[0]-vector2[0])**2+(vector1[1]-vector2[1])**2+(vector1[2]-vector2[2])**2)
    return(dist)

cpdef double dot(double[:] vector1, double[:] vector2):
    cdef double dprod = vector1[0]*vector2[0]+vector1[1]*vector2[1]+vector1[2]*vector2[2]
    return(dprod)

cpdef double norm(double[:] vector):
    cdef double mag = sqrt(vector[0]**2+vector[1]**2+vector[2]**2)
    return(mag)

cpdef double[:] diff(float[:] vector1, float[:] vector2):
    cdef int dim = 3
    cdef double[:] dif = np.zeros(3,dtype=float)
    dif[0] = vector1[0]-vector2[0] 
    dif[1] = vector1[1]-vector2[1]
    dif[2] = vector1[2]-vector2[2]
    return(dif)

cpdef int test(float[:,:] pos1, float[:,:] pos2, long[:] res1, long[:] res2, resn1, resn2, at1, at2, float cutoff, int frame, fname):
    cdef int i
    cdef int j
    cdef int dim = 3
    cdef int size1 = len(pos1)
    cdef int size2 = len(pos2)
    cdef char **atoms1 = to_cstring_array(at1)
    cdef char **atoms2 = to_cstring_array(at2)
    cdef char **rnames1 = to_cstring_array(resn1)
    cdef char **rnames2 = to_cstring_array(resn2)
    cdef char *name = to_cstring(fname)
    cdef double dist 
    with open(name.decode()+'.txt' , 'a') as f:
        f.write('{};\n'.format(frame))
        for i in range(size1):
            for j in range(size2):
                dist = distance(pos1[i], pos2[j])
                if dist <= cutoff:
                    f.write('{:5s} {:5d} {:5s} {:5d} {:5s} {:5d} {:5s} {:5d} {:5f} {:5f} {:5f} {:5f}\n'.format(rnames1[i].decode(),res1[i],atoms1[i].decode(),i,rnames2[j].decode(),res2[j],atoms2[j].decode(),j,dist,pos1[i][0]/10.0,pos1[i][1]/10.0,pos1[i][2]/10.0))
