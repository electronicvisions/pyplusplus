# Helper classes for wrapper function creation

"""This sub-package provides text substitution services for creating C++ functions.

The helper classes in this package are meant to be used by the actual
calldef code creators (that are not part of this sub-package). They
implement the core of the "arg policy" mechanism which can be used by
a user to modify the source code for a function.

The main class of this sub-package is the class L{substitution_manager_t}. This
class maintains two sets of special variables, one for the wrapper function
and one for the virtual function, and provides text substitution services.
The variables contain parts of source code that can be inserted into the
function source code template which is generated by the user of the class.


"""

from transformer import transformer_t
import transformers
from function_transformation import function_transformation_t

def output( *args, **keywd ):
    def creator( function ):
        return transformers.output_t( function, *args, **keywd )
    return creator

def input( *args, **keywd ):
    def creator( function ):
        return transformers.input_t( function, *args, **keywd )
    return creator

def inout( *args, **keywd ):
    def creator( function ):
        return transformers.inout_t( function, *args, **keywd )
    return creator

def input_static_array( *args, **keywd ):
    def creator( function ):
        return transformers.input_static_array_t( function, *args, **keywd )
    return creator

def output_static_array( *args, **keywd ):
    def creator( function ):
        return transformers.output_static_array_t( function, *args, **keywd )
    return creator

def modify_type( *args, **keywd ):
    def creator( function ):
        return transformers.type_modifier_t( function, *args, **keywd )
    return creator
