# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
This module is a collection of unrelated algorithms, that works on code creators
tree.
"""
import os
import math
import base64
from collections import defaultdict
from pygccxml import declarations
from pyplusplus import code_creators

class missing_call_policies:
    @staticmethod
    def _selector( creator ):
        if not isinstance( creator, code_creators.declaration_based_t ):
            return False
        if not isinstance( creator.declaration, declarations.calldef_t ):
            return False
        if isinstance( creator.declaration, declarations.constructor_t ):
            return False
        return hasattr(creator, 'call_policies') and not creator.call_policies

    @staticmethod
    def print_( extmodule ):
        creators = list(filter( missing_call_policies._selector
                           , code_creators.make_flatten_generator( extmodule.creators ) ))
        for creator in creators:
            print(creator.declaration.__class__.__name__, ': ', declarations.full_name( creator.declaration ))
            print('  *** MISSING CALL POLICY', creator.declaration.function_type().decl_string)
            print()

    @staticmethod
    def exclude( extmodule ):
        creators = list(filter( missing_call_policies._selector
                           , code_creators.make_flatten_generator( extmodule.creators ) ))
        for creator in creators:
            creator.parent.remove_creator( creator )

def split_sequence(seq, bucket_size):
    #split sequence to buckets, where every will contain maximum bucket_size items
    bucket_size = int(bucket_size)
    seq_len = len( seq )
    if seq_len <= bucket_size:
        return [ seq ]
    buckets = []
    num_of_buckets = int( math.ceil( float( seq_len ) / bucket_size ) )
    for i in range(num_of_buckets):
        from_ = i * bucket_size
        to = min( ( i + 1) * bucket_size, seq_len )
        buckets.append( seq[ from_ : to ] )
    return buckets


class exposed_decls_db_t( object ):
    DEFAULT_FILE_NAME = '%s.exposed_decl.pypp.txt'
    class row_t( declarations.decl_visitor_t ):
        FIELD_DELIMITER = '@'
        ALREADY_EXPOSED_DECL_SIGN = '-'
        EXPOSED_DECL_SIGN = '+'
        UNEXPOSED_DECL_SIGN = '~'
        CALLDEF_SIGNATURE_DELIMITER = '#'

        def __init__( self, decl_or_string ):
            self.key = ''
            self.exposed_sign = ''
            self.mangled_name = ''
            self.alias = ''
            if isinstance( decl_or_string, declarations.declaration_t ):
                self.__init_from_decl( decl_or_string )
            else:
                self.__init_from_str( decl_or_string )

        def find_out_mangled_name( self, declaration ):
            if declaration.mangled:
                return declaration.mangled
            elif declaration.location:
                # For unnamed enums, classes and unions or not mangled types
                # like typedefs
                filename, line = declaration.location.as_tuple()
                # Add mangled name of parent to distinguish instantiations
                # within template classes
                parent = self.find_out_mangled_name(declaration.parent)
                return "%s:%s:%s" % (parent,base64.b64encode(filename), line)
            elif isinstance( declaration, declarations.namespace_t ):
                return '' #I don't really care about unnamed namespaces
            else: #this should nevere happen
                raise RuntimeError( "Unable to create mangled name for declaration: " + str(declaration))

        def find_alias(self, decl):
            if self.FIELD_DELIMITER in self.alias:
                raise RuntimeError("invalid character in alias")
            else:
                return decl.alias

        def __init_from_str( self, row ):
            self.exposed_sign, self.key, self.mangled_name, self.alias \
                = row.split( self.FIELD_DELIMITER )

        def update_key( self, cls ):
            self.key = cls.__name__

        def __init_from_decl( self, declaration ):
            if declaration.already_exposed:
                self.exposed_sign = self.ALREADY_EXPOSED_DECL_SIGN
            elif declaration.ignore:
                self.exposed_sign = self.UNEXPOSED_DECL_SIGN
            else:
                self.exposed_sign = self.EXPOSED_DECL_SIGN

            self.update_key( declaration.__class__ )

            self.mangled_name = self.find_out_mangled_name( declaration )
            self.alias = self.find_alias(declaration)

        def __str__( self ):
            return self.FIELD_DELIMITER.join([ self.exposed_sign
                                               , self.key
                                               , self.mangled_name
                                               , self.alias])

    def __init__( self, module_name ):
        # ECM: might need py2to3
        self.__registry = defaultdict(lambda: defaultdict(list))# key : { name : set(row) }
        self.__row_delimiter = os.linesep
        self.__module_name = module_name

    def __file_name(self, fpath):
        if os.path.isdir( fpath ):
            fpath = os.path.join(fpath, self.DEFAULT_FILE_NAME % self.__module_name)
        return fpath

    def save( self, fpath ):
        with open( self.__file_name(fpath), 'w+b' ) as f:
            for name2rows in self.__registry.values():
                for rows in name2rows.values():
                    for row in rows:
                        f.write( '%s%s' % ( str(row), self.__row_delimiter ) )

    def load( self, fpath ):
        with open( self.__file_name(fpath), 'r+b' ) as f:
            for line in f:
                row = self.row_t( line.replace( self.__row_delimiter, '' ) )
                self.__update_registry( row )

    def __update_registry( self, row ):
        self.__registry[ row.key ][row.mangled_name].append(row)

    def __find_row_in_registry( self, row ):
        try:
            return next(rrow for rrow in self.__registry[ row.key ][ row.mangled_name ]
                if (rrow.key == row.key and
                    rrow.mangled_name == row.mangled_name))
        except (KeyError, StopIteration):
            return None

    def __find_in_registry( self, declaration ):
        row = self.row_t( declaration )
        found = self.__find_row_in_registry( row )
        if found:
            return found
        if isinstance( declaration, declarations.class_t ):
            row.update_key( declarations.class_declaration_t )
            found = self.__find_row_in_registry( row )
            if found:
                return found
        if isinstance( declaration, declarations.class_declaration_t ):
            row.update_key( declarations.class_t )
            found = self.__find_row_in_registry( row )
            if found:
                return found
        return None

    def is_exposed( self, declaration ):
        row = self.__find_in_registry( declaration)
        return row and self.row_t.EXPOSED_DECL_SIGN == row.exposed_sign

    def update_decls( self, global_ns ):
        for declaration in global_ns.decls():
            row = self.__find_in_registry( declaration )
            if not row:
                continue
            if self.row_t.ALREADY_EXPOSED_DECL_SIGN == row.exposed_sign:
                continue
            if self.row_t.EXPOSED_DECL_SIGN == row.exposed_sign:
                declaration.ignore = False
                declaration.already_exposed = self.__module_name
                declaration.alias = row.alias
            elif not decl.already_exposed:
                declaration.ignore = True
                declaration.already_exposed = False
                declaration.alias = row.alias

    def register_decls( self, global_ns, special_decls ):
        """register decls in the database

        global_ns - reference to the global namespace object
        special_decls - set of declarations, which were exposed, even so they
        were not ``included``. For example std containers.
        """
        for declaration in global_ns.decls():
            row = self.row_t( declaration )
            if declaration in special_decls:
                row.exposed_sign = row.EXPOSED_DECL_SIGN
            self.__update_registry( row )
