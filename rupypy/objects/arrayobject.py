from rupypy.module import ClassDef
from rupypy.modules.enumerable import Enumerable
from rupypy.objects.objectobject import W_BaseObject
from rupypy.objects.rangeobject import W_RangeObject

class W_ArrayObject(W_BaseObject):
    classdef = ClassDef("Array", W_BaseObject.classdef)
    classdef.include_module(Enumerable)

    def __init__(self, items_w):
        self.items_w = items_w

    def listview(self, space):
        return self.items_w

    classdef.app_method("""
    def to_s()
        result = "["
        i = 0
        self.each_with_index do |obj, i|
            if i > 0
                result << ", "
            end
            result << obj.to_s
        end
        result << "]"
    end
    """)

    @classdef.method("[]", idx="int")
    def method_subscript(self, space, idx):
        if isinstance(idx, W_RangeObject):
            start = idx.w_start.intvalue
            if idx.inclusive:
                end = idx.w_end.intvalue
            else:
                end = idx.w_end.intvalue + 1
            return W_ArrayObject(self.items_w[start:end])
        else:
            return self.items_w[idx]

    @classdef.method("[]=", idx="int")
    def method_subscript_assign(self, space, idx, w_obj):
        self.items_w[idx] = w_obj

    @classdef.method("length")
    def method_length(self, space):
        return space.newint(len(self.items_w))

    @classdef.method("+")
    def method_add(self, space, w_other):
        assert isinstance(w_other, W_ArrayObject)
        return space.newarray(self.items_w + w_other.items_w)

    @classdef.method("<<")
    def method_lshift(self, space, w_obj):
        self.items_w.append(w_obj)
        return self
        
    classdef.app_method("""
    def size
        self.length
    end
    """)

    classdef.app_method("""
    def each
        i = 0
        while i < self.length
            yield self[i]
            i += 1
        end
    end
    """)

    classdef.app_method("""
    def zip ary
        result = []
        self.each_with_index do |obj, idx|
            result << [obj, ary[idx]]
        end
        result
    end
    """)

    classdef.app_method("""
    def product ary
        result = []
        self.each do |obj|
            ary.each do |other|
                result << [obj, other]
            end
        end
        result
    end
    """)