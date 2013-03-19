# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys

from pyplusplus import _logging_
from pyplusplus import decl_wrappers

class module_builder_t(object):
    """base class for different module builders."""

    def __init__( self, global_ns=None, encoding='ascii' ):
        """
        """
        object.__init__( self )
        self.logger = _logging_.loggers.module_builder
        self.__encoding = encoding
        self.__global_ns = global_ns

    def __get_global_ns( self ):
        if not self.__global_ns:
            raise RuntimeError( "Reference to global namespace declaration was not set." )
        return self.__global_ns
    def __set_global_ns( self, global_ns ):
        self.__global_ns = global_ns

    global_ns = property( __get_global_ns, __set_global_ns
                          ,  doc="""reference to global namespace""" )

    @property
    def encoding( self ):
        return self.__encoding

    def run_query_optimizer(self):
        """
        It is possible to optimize time that takes to execute queries. In most cases
        this is done from the :meth:`__init__` method. But there are use-case,
        when you need to disable optimizer and run it later.
        """
        self.global_ns.init_optimizer()

    def print_declarations(self, decl=None, detailed=True, recursive=True, writer=sys.stdout.write):
        """
        This function will print detailed description of all declarations or
        some specific one.

        :param decl: optional, if passed, then only it will be printed
        :type decl: instance of :class:`decl_wrappers.decl_wrapper_t` class
        """
        if None is decl:
            decl = self.global_ns
        decl_wrappers.print_declarations( decl, detailed, recursive, writer )

    #select decl(s) interfaces
    def decl( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.decl( *args, **kwargs )

    def decls( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.decls( *args, **kwargs )

    def class_( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.class_( *args, **kwargs )

    def classes( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.classes( *args, **kwargs )

    def variable( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.variable( *args, **kwargs )

    var = variable

    def variables( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.variables( *args, **kwargs )

    vars = variables

    def calldef( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.calldef( *args, **kwargs )

    def calldefs( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.calldefs( *args, **kwargs )

    def operator( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.operator( *args, **kwargs )

    def operators( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.operators( *args, **kwargs )

    def member_function( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.member_function( *args, **kwargs )

    mem_fun = member_function

    def member_functions( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.member_functions( *args, **kwargs )

    mem_funs = member_functions

    def constructor( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.constructor( *args, **kwargs )

    def constructors( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.constructors( *args, **kwargs )

    def member_operator( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.member_operator( *args, **kwargs )

    def member_operators( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.member_operators( *args, **kwargs )

    def casting_operator( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.casting_operator( *args, **kwargs )

    def casting_operators( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.casting_operators( *args, **kwargs )

    def enumeration( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.enumeration( *args, **kwargs )
    enum = enumeration

    def enumerations( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.scopedef_t` class documentation"""
        return self.global_ns.enumerations( *args, **kwargs )

    enums = enumerations

    def namespace( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.namespace_t` class documentation"""
        return self.global_ns.namespace( *args, **kwargs )

    def namespaces( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.namespace_t` class documentation"""
        return self.global_ns.namespaces( *args, **kwargs )

    def free_function( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.namespace_t` class documentation"""
        return self.global_ns.free_function( *args, **kwargs )

    free_fun = free_function

    def free_functions( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.namespace_t` class documentation"""
        return self.global_ns.free_functions( *args, **kwargs )

    free_funs = free_functions

    def free_operator( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.namespace_t` class documentation"""
        return self.global_ns.free_operator( *args, **kwargs )

    def free_operators( self, *args, **kwargs ):
        """Please see :class:`decl_wrappers.namespace_t` class documentation"""
        return self.global_ns.free_operators( *args, **kwargs )
