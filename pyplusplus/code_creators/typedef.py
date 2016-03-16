# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import algorithm
import code_creator
import declaration_based
import registration_based
from pygccxml import declarations
from pygccxml.declarations import type_traits

class typedef_t( registration_based.registration_based_t
              , declaration_based.declaration_based_t ):
    """
    create code that exposes C++ typdefs
    """
    INT_TYPES = (
            declarations.char_t,
            declarations.signed_char_t,
            declarations.unsigned_char_t,
            declarations.wchar_t,
            declarations.short_int_t,
            declarations.short_unsigned_int_t,
            declarations.int_t,
            declarations.unsigned_int_t,
            declarations.long_int_t,
            declarations.long_unsigned_int_t,
            declarations.long_long_int_t,
            declarations.long_long_unsigned_int_t,
    )
    FLOAT_TYPES = (
            declarations.float_t,
            declarations.double_t,
            declarations.long_double_t,
    )


    def _bp_func(self, identifier, args = []):
        return 'bp::' + identifier + '(' + ', '.join(args) + ')'

    def __init__(self, typedef):
        registration_based.registration_based_t.__init__( self )
        declaration_based.declaration_based_t.__init__( self, declaration=typedef)
        self.works_on_instance = False

    def _gen_attr_access(self, decl, bp_fun=('scope',[])):
        ret = []
        while not isinstance(decl, declarations.namespace_t):
            ret.append('attr("%s")' % decl.alias)
            decl = decl.parent
        ret.append(self._bp_func(*bp_fun))
        return ".".join(reversed(ret))

    def _gen_attr_access_target(self, decl, bp_fun=('scope',[])):

        # Schauder .... (don't know how to make it poperly :( )
        if isinstance(decl, declarations.bool_t):
            return self._bp_func('eval', ['"bool"'])
        elif isinstance(decl, self.INT_TYPES):
            return self._bp_func('eval', ['"int"'])
        elif isinstance(decl, self.FLOAT_TYPES):
            return self._bp_func('eval', ['"float"'])
        elif type_traits.is_std_string(decl):
            return self._bp_func('eval', ['"str"'])
        else:
            return self._gen_attr_access(decl, bp_fun)

    def _get_alias(self, decl):
        if isinstance(decl, declarations.bool_t):
            return "bool"
        elif isinstance(decl, self.INT_TYPES):
            return "int"
        elif isinstance(decl, self.FLOAT_TYPES):
            return "float"
        elif type_traits.is_std_string(decl):
            return "str"
        else:
            return decl.alias

    def _create_impl(self):
        if self.declaration.already_exposed:
            return ''

        data = {
            "td_alias" : self._gen_attr_access(self.declaration),
        }

        if self.declaration.import_from_module:
            data["target_alias"] = self._gen_attr_access_target(
                    self.declaration.target_decl,
                    ('import', ['"%s"' % self.declaration.import_from_module]))
        else:
            data["target_alias"] = self._gen_attr_access_target(
                    self.declaration.target_decl)
        # A python warning is issued, when the target decl can not be found in
        # the module. All other errors are passed to the user.
        typedef_code = [
            'try {',
            self.indent('%(td_alias)s = %(target_alias)s;' % data),
            '} catch(bp::error_already_set) {',
            self.indent('if (!PyErr_ExceptionMatches(PyExc_AttributeError)) {'),
            self.indent('PySys_WriteStderr("Unexpected python exception, while'
                        ' creating a typedef alias");', 2),
            self.indent('PyErr_Print();', 2),
            self.indent('} else {'),
            self.indent('PyErr_Clear();', 2),
            self.indent('if(PyErr_WarnEx(PyExc_RuntimeWarning, "Wrapping error:'
                        ' base type %s (wrapped as %s) for typedef %s was not'
                        ' found", 0) == -1) {' % (
                            self.declaration.target_decl.partial_decl_string,
                            self._get_alias(self.declaration.target_decl),
                            self.declaration.partial_decl_string), 2),
            self.indent('throw;', 3),
            self.indent('}', 2),
            self.indent('}'),
            '}',
        ]
        return os.linesep.join(typedef_code)

    def _get_system_files_impl( self ):
        return []

