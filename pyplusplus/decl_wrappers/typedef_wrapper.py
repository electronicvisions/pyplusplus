# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""defines class that configure typedef exposing"""

from pygccxml import declarations
from pygccxml.declarations import cpptypes, type_traits
from pyplusplus import messages
from . import decl_wrapper
from . import class_wrapper

class typedef_t(decl_wrapper.decl_wrapper_t, declarations.typedef_t):
    """defines a set of properties, that will instruct `Py++` how to expose the typedef

    Today, `Py++` does not exposes typedefs, but this could be changed in future.
    In C++, it is a common practices to give an aliases to the class. May be in
    future, `Py++` will generate code, that will register all those aliases.
    """

    EXPORTABLE_TYPES = (
            class_wrapper.class_t,
            cpptypes.char_t,
            cpptypes.signed_char_t,
            cpptypes.unsigned_char_t,
            cpptypes.wchar_t,
            cpptypes.short_int_t,
            cpptypes.short_unsigned_int_t,
            cpptypes.bool_t,
            cpptypes.int_t,
            cpptypes.unsigned_int_t,
            cpptypes.long_int_t,
            cpptypes.long_unsigned_int_t,
            cpptypes.long_long_int_t,
            cpptypes.long_long_unsigned_int_t,
            cpptypes.float_t,
            cpptypes.double_t,
            cpptypes.long_double_t,
    )

    ALREADY_EXPOSED_TYPES = (
            class_wrapper.class_t,
            class_wrapper.class_declaration_t,
    )

    def __init__(self, *arguments, **keywords):
        declarations.typedef_t.__init__(self, *arguments, **keywords )
        decl_wrapper.decl_wrapper_t.__init__( self )
        self._target_decl = None
        self.__is_directive = None

    def _exportable_impl( self ):
        if isinstance(self.target_decl, self.ALREADY_EXPOSED_TYPES):
            if self.target_decl.already_exposed:
                return ''
        if not isinstance(self.target_decl, self.EXPORTABLE_TYPES):
            return messages.W1066 % str( self )
        try:
            if not self.target_decl.exportable:
                return messages.W1067 % str( self )
        except AttributeError:
            pass
        return ''

    @property
    def target_decl(self):
        if self._target_decl is None:
            self._target_decl = type_traits.remove_declarated(self.decl_type)
        return self._target_decl

    @property
    def import_from_module(self):
        try:
            return self._import_from_module
        except AttributeError:
            target_already_exposed = getattr(self.target_decl, 'already_exposed', False)
            if isinstance(target_already_exposed, str):
                self._import_from_module = target_already_exposed
            else:
                self._import_from_module = None
            return self._import_from_module

    @import_from_module.setter
    def import_from_module(self, module):
        self._import_from_module = module


