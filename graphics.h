#pragma once
#include <Python.h>
#define uint8 unsigned char

Py_NO_INLINE static void fdistance(float* arr1, float* arr2, uint8* out, size_t length);

Py_NO_INLINE static char conv(uint8* arr, char* kernel, uint8* out, size_t length,
                              const size_t shape[2], const size_t size[2], const uint8 ndim);

static PyObject* convolution(PyObject* self, PyObject* arg);

static PyObject* swap(PyObject* self, PyObject* args);

PyMODINIT_FUNC Pyinit_graphics(void);

static struct PyModuleDef module;

#define uint8 unsigned char
#define int16 short
// char
#define typeof(x) (x->descr->type)
// int
#define dimof(x) (x->nd)
// int
#define byteof(x) (x->descr->elsize)
// long long*
#define shapeof(x, i) (x->dimensions[i])

#define inshape(x, d0, d1, prt, type) { \
        prt = (type**)malloc(sizeof(type*) * d0); \
        for (size_t i = 0; i<d0; i++) \
            prt[i] = x + i * (d1 * sizeof(type)); \
    }

#define flip(a, min, max) ((a < min)? min: ((a > max)? max: a))

//static PyMethodDef Methods[];

//typedef struct PyArrayObject{
//    PyObject_HEAD
//    char *data;
//    int nd;
//    npy_intp
//}