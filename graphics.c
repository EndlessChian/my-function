#define PY_SSIZE_T_CLEAN
#define PY_LIMITED_API
#define NO_IMPORT_ARRAY
//#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <../include/Python.h>
#include <../Lib/site-packages/numpy/core/include/numpy/arrayobject.h>
#include <math.h>
#include "graphics.h"

Py_NO_INLINE static void fdistance(float* arr1, float* arr2, uint8* out, size_t length){
    for (float k, h; length--; ){
        k = *arr1++;
        h = *arr2++;
        *out++ = (uint8)sqrt(k * k + h * h);
    }
}

Py_NO_INLINE static char conv(uint8* arr, char* kernel, uint8* out, size_t length,
                              const size_t shape[2], const size_t size[2], const uint8 ndim){
    static size_t i, j, k, n, m;
    int *r = (int*)malloc(ndim * sizeof(int) * 2);
    const int num = (int)size[0] * (int)size[1];
    uint8 *zprt;
    char *cprt;
    length *= ndim;
    for (k = num; k --; for (m = ndim; m --; r[m] += *kernel++));
    for (m = ndim, n = num / 2; m --; r[m + ndim] = -128 * r[m] + (int)n);
	for (i = shape[0]; i--; ){
	    for (j = 0; j != shape[1]; j+=ndim){
            for (m = ndim; m--; r[m] = r[m + ndim]);
            cprt = kernel;
            zprt = arr + j;
            for (k = size[0]; k --; ){
                for (n = 0; n != size[1]; n ++){
                    for (m = 0; m != ndim;
                        r[m++] += (int)(*--cprt) * (int)(zprt[n+m]));
                }
                zprt += length;
            }
            for (m = 0; m != ndim; m++)
                *out++ = (uint8)flip(r[m] / num + 128, 0, 255);
        }
        arr += length;
    }
	return 0;
}

static PyObject* distance(PyObject* self, PyObject* arg){
	PyObject* _arr1 = NULL;
	PyObject* _arr2 = NULL;
	PyObject* _out = NULL;
	if (! PyArg_ParseTuple(arg, "OOO", &_arr1, &_arr2, &_out)){
	    PyErr_SetString(PyExc_TypeError, "Not a python type.");
		return NULL;
    }
	PyArrayObject_fields* arr1 = (PyArrayObject_fields*)_arr1;
	PyArrayObject_fields* arr2 = (PyArrayObject_fields*)_arr2;
	PyArrayObject_fields* out = (PyArrayObject_fields*)_out;
	if (arr1 == NULL || arr2 == NULL || out == NULL){
	    PyErr_SetString(PyExc_TypeError, "Not a numpy type.");
		return NULL;
    }
    if (typeof(arr1) != 'f' || typeof(arr2) != 'f' || typeof(out) != 'B'){
        PyErr_SetString(PyExc_TypeError, "Not a float or uint8 type array.");
        return NULL;
    }
    size_t length = 1;
    for (size_t i=dimof(out); i--; length *= (size_t)shapeof(out, i));
    fdistance((float*)(arr1->data), (float*)(arr2->data), (uint8*)(out->data), length);
    Py_RETURN_NONE;
}

static PyObject* convolution(PyObject* self, PyObject* arg){
	PyObject* _arr = NULL;
	PyObject* _kernel = NULL;
	PyObject* _out = NULL;
	if (! PyArg_ParseTuple(arg, "OOO", &_arr, &_kernel, &_out)){
	    PyErr_SetString(PyExc_TypeError, "Not a python type.");
		return NULL;
    }
	PyArrayObject_fields* arr = (PyArrayObject_fields*)_arr;
	PyArrayObject_fields* kernel = (PyArrayObject_fields*)_kernel;
	PyArrayObject_fields* out = (PyArrayObject_fields*)_out;
	if (arr == NULL || kernel == NULL || out == NULL){
	    PyErr_SetString(PyExc_TypeError, "Not a numpy type.");
		return NULL;
    }
    if (typeof(arr) != 'B' || typeof(out) != 'B' || typeof(kernel) != 'b'){
        PyErr_SetString(PyExc_TypeError, "Not a uint8 type array.");
        return NULL;
    }
    uint8 ndim;
    if ((ndim = dimof(arr)) != dimof(out) || dimof(kernel) != ndim || (ndim != 2 && ndim != 3)){
        PyErr_SetString(PyExc_ValueError, "Not same-depth and 2|3-dim arrays.");
        return NULL;
    }
    size_t shape[2], shape0[2], size[2];
    if ((shape0[0] = shapeof(arr, 0)) - (size[0] = shapeof(kernel, 0)) + 1 != (shape[0] = shapeof(out, 0)) ||
        (shape0[1] = shapeof(arr, 1)) - (size[1] = shapeof(kernel, 1)) + 1 != (shape[1] = shapeof(out, 1))){
            PyErr_SetString(PyExc_ValueError, "Not current shapes, shape of out must be (arr.shape - kernel.shape + 1).");
            return NULL;
    }
    if (shape0[0] < size[0] || shape0[1] < size[1] || (size[0] * size[1]) > 132622){    // 2,147,481,735
        PyErr_SetString(PyExc_ValueError, "Too big kernel, kernel size must not bigger than input shape or 132622.");
        return NULL;
    }
	if(conv((uint8*)(arr->data), (kernel->data), (uint8*)(out->data), shape0[1], shape, size, ndim-1)){
        PyErr_SetString(PyExc_ValueError, "Can't calculate with this kernel.");
	    return NULL;
    }
	Py_RETURN_NONE;
}

static PyObject* swap(PyObject* self, PyObject* args){
	PyObject* _arr;
	int axis, ind1, ind2, ndim, i, j;
	if (! PyArg_ParseTuple(args, "Oiii", &_arr, &axis, &ind1, &ind2)){
	    PyErr_SetString(PyExc_TypeError, "Not a python type.");
		return NULL;
    }
	PyArrayObject_fields* arr = (PyArrayObject_fields*)_arr;
	if (arr == NULL){
	    PyErr_SetString(PyExc_TypeError, "argument in pos 0 is Not a numpy array.");
		return NULL;
    }
    ndim = dimof(arr);
    if (axis < 0) axis += ndim;
    if (ndim <= axis || axis < 0){
	    PyErr_SetString(PyExc_TypeError, "axis out of bounder.");
		return NULL;
    }
    i = shapeof(arr, axis);
    if (ind1 < 0) ind1 += i;
    if (ind2 < 0) ind2 += i;
    {
    static char str[] = "index 1 out of bounder.";
    if (i <= ind1 || ind1 < 0){
        str[6] = '1';
	    PyErr_SetString(PyExc_TypeError, str);
		return NULL;
    }
    if (i <= ind2 || ind2 < 0){
        str[6] = '2';
	    PyErr_SetString(PyExc_TypeError, str);
		return NULL;
    }
    }
    _swap(arr->data, axis, ind1, ind2, sizeof(typeof(arr)));
    ((typeof(arr))*) ptr = ((typeof(arr))*)arr->data;
    for (int y=shapeof(arr, 0), X=shapeof(arr, 1), x; --y; ){
        for (x=X; --x; ){
            j = (y * X + x) * 3;
            i = ptr[j + ind1];
            ptr[j + ind1] = ptr[j + ind2];
            ptr[j + ind2] = i;
        }
    }
    return _arr;
}
static void _swap(char* data, int axis, int ind1, int ind2, int size){

}

static PyMethodDef Methods[] = {
    {"convolution", (PyCFunction)convolution, METH_VARARGS,
     PyDoc_STR("conlution(const uint8 arr[][], int8 kernel[][], uint8 out[][]).")},
    {"distance", (PyCFunction)distance, METH_VARARGS,
     PyDoc_STR("distance(const float *arr1, const float *arr2, float *out).\n\t"
     "it calulate the sqrt distance and the array can be any shape but must have the same size.")},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "_graphics",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit__graphics(void){
    return PyModule_Create(&module);
}
