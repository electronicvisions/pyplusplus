# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
from . import algorithm
from . import code_creator
from . import declaration_based
from . import registration_based
from pygccxml import declarations

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

        # Schauder .... (don't know how to make it poperly :( )
        if isinstance(decl, declarations.bool_t):
            return self._bp_func('eval', ['"bool"'])
        elif isinstance(decl, self.INT_TYPES):
            return self._bp_func('eval', ['"int"'])
        elif isinstance(decl, self.FLOAT_TYPES):
            return self._bp_func('eval', ['"float"'])
        else:
            ret = []
            while not isinstance(decl, declarations.namespace_t):
                ret.append('attr("%s")' % decl.alias)
                decl = decl.parent
            ret.append(self._bp_func(*bp_fun))
            return ".".join(reversed(ret))

    def _create_impl(self):
        if self.declaration.already_exposed:
            return ''

        data = {
            "td_alias" : self._gen_attr_access(self.declaration),
        }

        if self.declaration.import_from_module:
            data["target_alias"] = self._gen_attr_access(self.declaration.target_decl,
                    ('import', ['"%s"' % self.declaration.import_from_module]))
        else:
            data["target_alias"] = self._gen_attr_access(self.declaration.target_decl)

        # Print exception but allow loading to continue.
        typedef_code = []
        typedef_code.append('try {')
        typedef_code.append('%(td_alias)s = %(target_alias)s;' % data)
        typedef_code.append('} catch(bp::error_already_set) {')
        typedef_code.append('if (PyErr_Occurred()) PyErr_Print();')
        typedef_code.append('}')

        return os.linesep.join(typedef_code)

    def _get_system_files_impl( self ):
        return []

