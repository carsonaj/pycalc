from ctypes import * 
lib = CDLL("/usr/local/lib/ccalc/libccalc.so")

class DoubleMatrix(Structure):
    _fields_ = [("nrow", c_int), 
                ("ncol", c_int),
                ("data", POINTER(c_double))]
    
    def __init__(self, nrow, ncol, data=[]):
        self.nrow = nrow
        self.ncol = ncol
        
        arr_type = c_double * (nrow * ncol)
        arr_inst = arr_type(*data)
        self.data = arr_inst
        
        return
    
    def __str__(self):
        l = [self.data[x] for x in range(self.nrow * self.ncol)]
        l = list(map(lambda x: f"{x:12.2f}", l))
        for i in range(self.nrow):
            l[(i + 1) * self.ncol - 1] = l[(i + 1) * self.ncol -1] + "\n"
        s = "".join(l)
                 
        return s
    
    def __setitem__(self, args, val):
        i = c_int(args[0])
        j = c_int(args[1])
        val = c_double(val)
        lib.dblmat_set_entry(self, i, j, val)
        
        return
    
    def __getitem__(self, args):
        i = c_int(args[0])
        j = c_int(args[1])
       
        return lib.dblmat_get_entry(self, i, j)
    
    def __eq__(self, other):
        assert type(self) == type(other)
        b = lib.dblmat_equal(self, other)
        return bool(b)
    
    def __add__(self, other):
        assert self.nrow == other.nrow
        assert self.ncol == other.ncol
        sum = DoubleMatrix(self.nrow, self.ncol)
        lib.dblmat_sum(self, other, sum)
        
        return sum
    
    def __rmul__(self, other):
        assert type(other) in {float, int}
        other = float(other)
        scaled = self.copy()
        lib.dblmat_scale(other, scaled)
        
        return scaled
    
    def __sub__(self, other):
        assert self.nrow == other.nrow
        assert self.ncol == other.ncol
        diff = self + (-other) 
        
        return diff
        
    def copy(self):
        cpy = DoubleMatrix(self.nrow, self.ncol, [self.data[x] for x in range(self.nrow * self.ncol)])
        
        return cpy

    def fill(self, data):
        assert len(data) == self.nrow * self.ncol
        arr_type = c_double * len(data)
        arr_inst = arr_type(*data)
        lib.dblmat_fill(self, arr_inst)
        
        return

    

    
lib.dblmat_set_entry.argtypes = [POINTER(DoubleMatrix), c_int, c_int, c_double] 
lib.dblmat_set_entry.restype = None
    
lib.dblmat_get_entry.argtypes = [POINTER(DoubleMatrix), c_int, c_int]
lib.dblmat_get_entry.restype = c_double

lib.dblmat_equal.argtypes = [POINTER(DoubleMatrix), POINTER(DoubleMatrix)]
lib.dblmat_equal.restype = c_int

lib.dblmat_sum.argtypes = [POINTER(DoubleMatrix), POINTER(DoubleMatrix), POINTER(DoubleMatrix)]
lib.dblmat_sum.restype = None
    
lib.dblmat_fill.argtypes = [POINTER(DoubleMatrix), POINTER(c_double)]
lib.dblmat_fill.restype = None

lib.dblmat_scale.argtypes = [c_double, POINTER(DoubleMatrix)]
lib.dblmat_scale.restype = None


