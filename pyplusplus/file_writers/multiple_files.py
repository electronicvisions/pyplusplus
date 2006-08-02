# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import writer
from sets import Set as set
from pygccxml import declarations
from pyplusplus import decl_wrappers
from pyplusplus import code_creators

#TODO: to add namespace_alias_t classes
class multiple_files_t(writer.writer_t):
    """
    This class implements classic strategy of deviding classes to files
    one class in one header + source files.
    """ 
    HEADER_EXT = '.pypp.hpp'
    SOURCE_EXT = '.pypp.cpp'

    def __init__(self, extmodule, directory_path):
        """Constructor.

        @param extmodule: The root of a code creator tree
        @type extmodule: module_t
        @param directory_path: The output directory where the source files are written
        @type directory_path: str
        """
        writer.writer_t.__init__(self, extmodule)
        self.__directory_path = directory_path
        self.create_dir( directory_path )
        self.include_creators = []  # List of include_t creators that contain the generated headers
        self.split_header_names = []  # List of include file names for split files
        self.split_method_names = []  # List of methods from the split files

        
    def create_dir( self, directory_path ):
        """Create the output directory if it doesn't already exist.
        """
        if os.path.exists( directory_path ) and not os.path.isdir(directory_path):
            raise RuntimeError( 'directory_path should contain path to directory.' )
        if not os.path.exists( directory_path ):
            os.makedirs( directory_path )

    def _get_directory_path(self):
        return self.__directory_path
    directory_path = property( _get_directory_path,
                               doc="""The name of the output directory.
                               @type: str
                               """ )

    def create_function_code( self, function_name ):
        return "void %s();" % function_name

    def create_header( self, file_name, code ):
        """Return the content of a header file.

        @param file_name: A string that uniquely identifies the file name
        @type file_name: str
        @param function_name: The name of the register_xyz() function
        @type function_name: str
        @returns: The content for a header file
        @rtype: str
        """
        tmpl = os.linesep.join([
                    "#ifndef __%(file_name)s_hpp__pyplusplus_wrapper__"
                  , "#define __%(file_name)s_hpp__pyplusplus_wrapper__"
                  , ''
                  , "%(code)s"
                  , ''
                  , "#endif//__%(file_name)s_hpp__pyplusplus_wrapper__" ])
        
        content = ''
        if self.extmodule.license:
            content = self.extmodule.license.create() + os.linesep
        content = content + tmpl % { 'file_name' : file_name, 'code' : code }
        return content

    def find_out_value_traits_header( self, code_creator ):
        if not isinstance( code_creator, ( code_creators.class_t, code_creators.class_declaration_t ) ):
            return None
        if None is code_creator.declaration.indexing_suite:
            return None
        if not isinstance( code_creator.declaration.indexing_suite, decl_wrappers.indexing_suite2_t ):
            return None
        element_type = code_creator.declaration.indexing_suite.element_type
        class_traits = declarations.class_traits
        if not class_traits.is_my_case( element_type ):
            return None
        value_class = class_traits.get_declaration( element_type )
        return self.create_value_traits_header_name( value_class )
    
    def create_include_code( self, creators, head_headers=None, tail_headers=None ):      
        answer = []
        normalize = code_creators.include_directories_t.normalize
        if head_headers:
            answer.extend( map( lambda header: '#include "%s"' % normalize( header )
                                , head_headers ) )

        # Include all 'global' include files...
        includes = filter( lambda creator: isinstance( creator, code_creators.include_t )
                           , self.extmodule.creators )
        answer.extend( map( lambda creator: creator.create(), includes ) )
        
        for creator in creators:
            header = self.find_out_value_traits_header( creator )
            if header:
                answer.append( '#include "%s"' % header )
    
        if tail_headers:
            answer.extend( map( lambda header: '#include "%s"' % normalize( header )
                                , tail_headers ) )
        
        return os.linesep.join( answer )
    
    def create_namespaces_code( self, creators ):    
        # Write all 'global' namespace_alias_t and namespace_using_t creators first...
        ns_types = ( code_creators.namespace_alias_t, code_creators.namespace_using_t )
        ns_creators = filter( lambda x: isinstance( x, ns_types ), self.extmodule.creators )

        ns_creators.extend( filter( lambda x: isinstance( x, ns_types ), self.extmodule.body.creators ) )
        if not ns_creators:
            return ''
        else:
            return os.linesep.join( map( lambda creator: creator.create(), ns_creators ) )

    def create_source( self, file_name, function_name, registration_creators, declaration_creators=None ):
        """Return the content of a cpp file.

        @param file_name: The base name of the corresponding include file (without extension)
        @type file_name: str
        @param function_name: The name of the register_xyz() function
        @type function_name: str
        @param creators: The code creators that create the register_xyz() function
        @type creators: list of code_creator_t
        @returns: The content for a cpp file
        @rtype: str
        """
        
        if None is declaration_creators:
            declaration_creators = []
        creators = registration_creators + declaration_creators
        
        answer = []
        if self.extmodule.license:
            answer.append( self.extmodule.license.create() )
        
        head_headers = [ file_name + self.HEADER_EXT ]
        answer.append( self.create_include_code( creators, head_headers ) )

        answer.append( '' )
        answer.append( self.create_namespaces_code( creators ) )

        # Write wrapper classes...
        for creator in declaration_creators:
            answer.append( '' )
            answer.append( creator.create() )

        # Write the register() function...
        answer.append( '' )
        answer.append( 'void %s(){' % function_name )
        answer.append( '' )
        for creator in registration_creators:
            answer.append( code_creators.code_creator_t.indent( creator.create() ) )
            answer.append( '' )
        answer.append( '}' )
        return os.linesep.join( answer )
    
    def split_class_impl( self, class_creator):
        function_name = 'register_%s_class' % class_creator.alias
        file_path = os.path.join( self.directory_path, class_creator.alias )
        # Write the .h file...
        header_name = file_path + self.HEADER_EXT
        self.write_file( header_name
                         , self.create_header( class_creator.alias
                                               , self.create_function_code( function_name ) ) )
        class_wrapper = None
        decl_creators = class_creator.user_declarations[:]
        if isinstance( class_creator, code_creators.class_t ) and class_creator.wrapper:
            class_wrapper = class_creator.wrapper
            decl_creators.append( class_creator.wrapper )
        
        # Write the .cpp file...
        cpp_code = self.create_source( class_creator.alias
                                       , function_name
                                       , [class_creator]
                                       , decl_creators )
        self.write_file( file_path + self.SOURCE_EXT, cpp_code )
        if class_wrapper:
            # The wrapper has already been written above, so replace the create()
            # method with a new 'method' that just returns an empty string because
            # this method is later called again for the main source file.
            class_wrapper.create = lambda: ''
        # Replace the create() method so that only the register() method is called
        # (this is called later for the main source file).
        class_creator.create = lambda: function_name +'();'
        self.include_creators.append( code_creators.include_t( header_name ) )
        self.split_header_names.append(header_name)
        self.split_method_names.append(function_name)

    def split_class( self, class_creator):
        """Write the .h/.cpp file for one class.

        Writes a .h/.cpp file for the given class. The files use the class name
        as base file name.

        @param class_creator: The class creator for one particular class
        @type class_creator: class_t
        """
        try:
            self.split_class_impl( class_creator )
        except IOError, error:
            msg = [ 'Failed to write code for class "%s" into file.' % class_creator.declaration.name ]
            msg.append( "May be the class name is too long?." )
            msg.append( "Error: %s'" % str(error) )
            self.logger.error( os.linesep.join( msg ) )
            raise

    def create_value_traits_header_name( self, value_class ):
        return "_" + value_class.alias + "__value_traits" + self.HEADER_EXT

    def split_value_traits( self, value_traits ):
        """
        Write the value_traits class to header file, that will be included
        from files, that uses indexing suite 2
        """
        header_name = self.create_value_traits_header_name( value_traits.declaration ) 
        file_path = os.path.join( self.directory_path, header_name )
        self.write_file( file_path
                        , self.create_header( header_name.replace( '.', '_' )
                                              , value_traits.create() ) )
        value_traits.create = lambda: ''

    def split_creators( self, creators, pattern, function_name, registrator_pos ):
        """Write non-class creators into a particular .h/.cpp file.

        @param creators: The code creators that should be written
        @type creators: list of code_creator_t
        @param pattern: Name pattern that is used for constructing the final output file name
        @type pattern: str
        @param function_name: The name of the register_xyz() function
        @type function_name: str
        @param registrator_pos: The position of the code creator that creates the code to invoke the register_xyz() function.
        @type registrator_pos: int
        """
        if not creators:
            return
        file_pattern = self.extmodule.body.name + pattern
        file_path = os.path.join( self.directory_path, file_pattern )
        header_name = file_path + self.HEADER_EXT
        self.write_file( header_name
                         , self.create_header( file_pattern, self.create_function_code( function_name ) ) )
        self.write_file( file_path + self.SOURCE_EXT
                         , self.create_source( file_pattern
                                               , function_name
                                               , creators ))
        for creator in creators:
            creator.create = lambda: ''
        self.extmodule.body.adopt_creator( 
            code_creators.custom_text_t( function_name + '();' )
            , registrator_pos)
        self.include_creators.append( code_creators.include_t( header_name ) )        
        self.split_header_names.append(header_name)
        self.split_method_names.append(function_name)

    def split_enums( self ):
        """Write all enumerations into a separate .h/.cpp file.
        """
        enums_creators = filter( lambda x: isinstance(x, code_creators.enum_t )
                                 , self.extmodule.body.creators )

        self.split_creators( enums_creators, '_enumerations', 'register_enumerations', 0 )

    def split_global_variables( self ):
        """Write all global variables into a separate .h/.cpp file.
        """
        creators = filter( lambda x: isinstance(x, code_creators.global_variable_t )
                           , self.extmodule.body.creators )
        creators.extend( filter( lambda x: isinstance(x, code_creators.unnamed_enum_t )
                           , self.extmodule.body.creators ) )
        self.split_creators( creators, '_global_variables', 'register_global_variables', -1 )

    def split_free_functions( self ):
        """Write all free functions into a separate .h/.cpp file.
        """
        creators = filter( lambda x: isinstance(x, code_creators.free_function_t )
                           , self.extmodule.body.creators )
        self.split_creators( creators, '_free_functions', 'register_free_functions', -1 )

    #TODO: move write_main to __init__
    def write(self, write_main=True):
        """ Write out the module.
            Creates a separate source/header combo for each class and for enums, globals,
            and free functions.
            If write_main is True it writes out a main file that calls all the registration methods.
            After this call split_header_names and split_method_names will contain
            all the header files and registration methods used.  This can be used by
            user code to create custom registration methods if main is not written.
        """

        self.write_code_repository( self.__directory_path )

        self.extmodule.do_include_dirs_optimization()

        value_traits_classes = filter( lambda x: isinstance(x, code_creators.value_traits_t )
                                       , self.extmodule.creators )
        map( self.split_value_traits, value_traits_classes )
        
        # Obtain a list of all class creators...
        class_creators = filter( lambda x: isinstance(x, ( code_creators.class_t, code_creators.class_declaration_t ) )
                                 , self.extmodule.body.creators )
        # ...and write a .h/.cpp file for each class
        map( self.split_class, class_creators )
        
        self.split_enums()
        self.split_global_variables()
        self.split_free_functions()
        
        if write_main:
            self.include_creators.sort( cmp=lambda ic1, ic2: cmp( ic1.header, ic2.header ) )
            map( lambda creator: self.extmodule.adopt_include( creator )
                 , self.include_creators )
            main_cpp = os.path.join( self.directory_path, self.extmodule.body.name + '.main.cpp' )
            self.write_file( main_cpp, self.extmodule.create() + os.linesep )
