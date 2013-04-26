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
    def __init__(self, typedef):
        registration_based.registration_based_t.__init__( self )
        declaration_based.declaration_based_t.__init__( self, declaration=typedef)
        self.works_on_instance = False

    def _gen_attr_access(self, decl):
        ret = []
        while not isinstance(decl, declarations.namespace_t):
            ret.append('attr("%s")' % decl.alias)
            decl = decl.parent
        ret.append('::boost::python::scope()')
        return ".".join(reversed(ret))

    def _create_impl(self):
        if self.declaration.already_exposed:
            return ''

        data = {
            "td_alias" : self._gen_attr_access(self.declaration),
            "target_alias" : self._gen_attr_access(self.declaration.target_decl),
        }

        # Print exception but allow loading to continue.
        typedef_code = []
        typedef_code.append('try {')
        typedef_code.append('%(td_alias)s = %(target_alias)s;' % data)
        typedef_code.append('} catch(bp::error_already_set) {')
        typedef_code.append('if (PyErr_Occurred()) PyErr_Print();')
        typedef_code.append('}')

        return os.linesep.join(typedef_code)

        bpl_enum = '%(bpl::enum_)s< %(name)s>("%(alias)s")' \
                   % { 'bpl::enum_' : algorithm.create_identifier( self, '::boost::python::enum_' )
                       , 'name' : algorithm.create_identifier( self, self.declaration.decl_string )
                       , 'alias' : self.alias }

        values = []
        # Add the values that should be exported
        for value_name in self.declaration.export_values:
            values.append( self._generate_value_code( value_name ) )

        # Export the values
        if len(self.declaration.export_values)>0:
            values.append( '.export_values()' )

        # Add the values that should not be exported
        for name in self.declaration.no_export_values:
            values.append( self._generate_value_code( name ) )

        values.append( ';' )

        values = self.indent( os.linesep.join( values ) )
        return bpl_enum + os.linesep + values

    def _get_system_files_impl( self ):
        return []

