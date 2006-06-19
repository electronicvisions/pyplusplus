# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
from pygccxml import declarations
from pyplusplus import code_creators
from pyplusplus import _logging_
templates = declarations.templates

class types_database_t( object ):
    def __init__( self ):
        object.__init__( self )
        self.__variables = {} # decl_string : [type]
        self.__return_types = {} # decl_string : [type]
        self.__arguments_types = {} #decl_string : [type]
        self.__smart_ptrs = [ 'shared_ptr', 'auto_ptr' ] 
        self.__fundamental_strs = declarations.FUNDAMENTAL_TYPES.keys()
        self.__normalize_data = [ ',', '<', '>', '*', '&', '(', ')', '::' ]
        self.__used_vectors = set()
    
    def update( self, decl ):
        if isinstance( decl, declarations.calldef_t ):
            if not isinstance( decl, declarations.constructor_t ):
                self._update_db( self.__return_types, decl.return_type )
            map( lambda arg: self._update_db( self.__arguments_types, arg.type )
                 , decl.arguments )
        elif isinstance( decl, declarations.variable_t ):
            self._update_db( self.__variables, decl.type )
        else:
            assert 0
            
    def _is_relevant(self, decl_string):
        for smart_ptr in self.__smart_ptrs:
            if smart_ptr in decl_string:
                return True
        return False
    
    def _is_relevant_inst( self, name, args ):
        return self._is_relevant( name )

    def _normalize( self, decl_string ):
        if decl_string.startswith( '::' ):
            decl_string = decl_string[2:]
        answer = decl_string
        for data in self.__normalize_data:
            answer = answer.replace( data + ' ', data )
            answer = answer.replace( ' ' + data, data )
        return answer.replace( '  ', ' ' )

    def _update_containers_db( self, type ):
        #will return True is type was treated
        type = declarations.remove_alias( type )
        type = declarations.remove_pointer( type )
        type = declarations.remove_reference( type )        
        if declarations.vector_traits.is_vector( type ):
            vector = declarations.vector_traits.class_declaration( type )
            try:
                declarations.vector_traits.value_type( vector )
                self.__used_vectors.add( vector )
                return True
            except RuntimeError, error:
                msg = 'WARNING: pyplusplus found std::vector instantiation declaration, '
                msg = msg + 'but can not find out value type!'
                msg = msg + os.linesep + 'This class will not be exported!'
                msg = msg + os.linesep + 'std::vector instantiation is: ' + vector.decl_string
                _logging_.logger.warn( msg )
        return False
        
    def _update_db( self, db, type_ ):
        if self._update_containers_db( type_ ):
            return
        decl_string = self._normalize( declarations.base_type( type_ ).decl_string ) 
        if not templates.is_instantiation( decl_string ):
            return 
        if not self._is_relevant( decl_string ):
            return
        insts = filter( lambda inst: self._is_relevant_inst( inst[0], inst[1] )
                        , templates.split_recursive( decl_string ) )        
        for smart_ptr, args in insts:
            assert len( args ) == 1 
            pointee = self._normalize( args[0] )
            if not db.has_key(pointee):
                db[ pointee ] = []
            smart_ptr = self._normalize( smart_ptr )
            if (smart_ptr, type_) not in db[pointee]:
                db[ pointee ].append( (smart_ptr, type_) )
                
    def _find_smart_ptrs( self, db, class_decl ):
        decl_string = self._normalize( class_decl.decl_string )
        if db.has_key( decl_string ):
            return db[ decl_string ]
        else:
            return None
        
    def create_holder( self, class_decl ):
        #holder should be created when we pass object created in python
        #as parameter to function in C++ that takes the smart pointer by reference
        found = self._find_smart_ptrs( self.__arguments_types, class_decl )
        if not found:
            return None#not found or ambiguty
        
        held_type = None
        for smart_ptr, type_ in found:
            if declarations.is_reference( type_ ) and not declarations.is_const( type_.base ):
                temp = code_creators.held_type_t( smart_ptr=smart_ptr )
                if not held_type or 'shared_ptr' in smart_ptr:
                    held_type = temp
        return held_type
    
    def _create_registrators_from_db( self, db, class_creator, registered ):
        spregistrator_t = code_creators.smart_pointer_registrator_t
        found = self._find_smart_ptrs( db, class_creator.declaration )
        if not found:
            return
        for smart_ptr, type_ in found:
            already_registered = filter( lambda registrator: registrator.smart_ptr == smart_ptr
                                         , registered )
            if not already_registered:
                registered.append( spregistrator_t( smart_ptr=smart_ptr, class_creator=class_creator) )
    
    def create_registrators( self, class_creator ):
        """ Look for places where the class may be used as smart_ptr.
            - If found then create smart_pointer_registrator_t for that class and ptr type.
        """
        spconverter_t = code_creators.smart_pointers_converter_t
        registrators = []
        dbs = [ self.__arguments_types, self.__return_types, self.__variables ]
        for db in dbs:
            self._create_registrators_from_db( db, class_creator, registrators )
        if not class_creator.declaration.bases:
            return registrators
        # Add implicit converters from me to base classes and from derived classes to me
        answer = []
        for registrator in registrators:
            answer.append( registrator )
            decl = registrator.declaration
            for hierarchy_info in decl.recursive_bases:
                if hierarchy_info.access_type != declarations.ACCESS_TYPES.PRIVATE:
                    converter = spconverter_t( smart_ptr=registrator.smart_ptr
                                               , source=class_creator.declaration
                                               , target=hierarchy_info.related_class )
                    answer.append( converter )
            for hierarchy_info in decl.recursive_derived:
                if hierarchy_info.access_type != declarations.ACCESS_TYPES.PRIVATE:
                    converter = spconverter_t( smart_ptr=registrator.smart_ptr
                                               , source=hierarchy_info.related_class
                                               , target=class_creator.declaration )
                    answer.append( converter )
        return answer
    
    def _print_single_db(self, db):
        for decl_string in db.keys():
            print 'decl_string : ', decl_string
            for smart_ptr, type_ in db[ decl_string ]:
                print '    smart_ptr : ', smart_ptr
                print '    type_     : ', type_.decl_string
        
    def print_db( self ):
        dbs = [ self.__arguments_types, self.__return_types, self.__variables ]
        for db in dbs:
            self._print_single_db( db )
            
    def _get_used_vectors( self ):
        return self.__used_vectors
    used_vectors = property( _get_used_vectors )

