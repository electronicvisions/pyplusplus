# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import unittest
import fundamental_tester_base


MODULE_SPTR_DECL_CODE = \
"""
namespace boost{ namespace python{

    using namespace controllers;

    controller_i* get_pointer( my_smart_ptr_t< controller_i > const& p ){
        return p.get();
    }

    template <>
    struct pointee< my_smart_ptr_t< controller_i > >{
        typedef controller_i type;
    };


    add_x_t* get_pointer( my_smart_ptr_t< add_x_t > const& p ){
        return p.get();
    }

    template <>
    struct pointee< my_smart_ptr_t< add_x_t > >{
        typedef add_x_t type;
    };


}}// namespace boost::python converter
"""

MODULE_SPTR_REG_CODE = \
"""
    bp::register_ptr_to_python< my_smart_ptr_t< controllers::controller_i > >();

    bp::register_ptr_to_python< my_smart_ptr_t< controllers::add_x_t > >();

    bp::implicitly_convertible< my_smart_ptr_t< controllers::add_x_t >, my_smart_ptr_t< controllers::controller_i > >();

"""

class tester_t(fundamental_tester_base.fundamental_tester_base_t):
    EXTENSION_NAME = 'custom_smart_ptr_classes'

    def __init__( self, *args ):
        fundamental_tester_base.fundamental_tester_base_t.__init__(
            self
            , tester_t.EXTENSION_NAME
            , *args )

    def customize( self, mb ):
        mb.classes( lambda cls: 'ptr' in cls.name).exclude()
        mb.add_declaration_code( MODULE_SPTR_DECL_CODE )
        mb.add_registration_code( MODULE_SPTR_REG_CODE )

    def create_identity_value( self, module, v ):
        class identity_value_t( module.value_i ):
            def __init__( self, v ):
                module.value_i.__init__( self )
                self.value = v

            def get_value(self):
                return self.value

        return identity_value_t(v)

    def create_add_5_value( self, module, v ):
        class add_5_value_t( module.value_plus_x_t ):
            def __init__( self, v ):
                module.value_plus_x_t.__init__( self, v )

            def get_plus_value(self):
                print "I am here"
                return 5
        return add_5_value_t( v )

    def run_tests(self, module):
        add_0 = module.add_x_t( 23 )
        self.failUnless( 23 == add_0.get_value() )
        self.failUnless( 23 == module.ref_get_value( add_0 ) )
        self.failUnless( 23 == module.val_get_value( add_0 ) )
        self.failUnless( 23 == module.const_ref_get_value( add_0 ) )


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()