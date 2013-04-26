# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import compound

class module_body_t(compound.compound_t):
    def __init__( self, name ):
        compound.compound_t.__init__(self )
        self._name = name
        self.head_creators = []
        self.tail_creators = []

    def adopt_head_creator(self, creator, index=None):
        """Add a creator to the list of children creators.
        The code will be placed in the head section of the body.

        :param creator: Creator object
        :type creator: :class:`code_creators.code_creator_t`
        :param index: Desired position of the creator or None to append it to the end of the list
        :type index: int
        """
        self._adopt_creator(creator, self.head_creators, index)

    def adopt_head_creators(self, creators, index=None):
        """Add a creator to the list of children creators.
        The code will be placed in the head section of the body.

        :param creators: list of creators object
        :type creator: :class:`code_creators.code_creator_t`
        :param index: Desired position of the creator or None to append it to the end of the list
        :type index: int
        """
        self._adopt_creators(creators, self.head_creators, index)

    def adopt_tail_creator(self, creator, index=None):
        """Add a creator to the list of children creators.
        The code will be placed in the tail section of the body.

        :param creator: Creator object
        :type creator: :class:`code_creators.code_creator_t`
        :param index: Desired position of the creator or None to append it to the end of the list
        :type index: int
        """
        self._adopt_creator(creator, self.tail_creators, index)

    def adopt_tail_creators(self, creators, index=None):
        """Add a creators to the list of children creators.
        The code will be placed in the tail section of the body.

        :param creators: list of creators object
        :type creator: :class:`code_creators.code_creator_t`
        :param index: Desired position of the creator or None to append it to the end of the list
        :type index: int
        """
        self._adopt_creators(creators, self.tail_creators, index)

    def _get_name(self):
        return self._name
    name = property( _get_name )

    def _create_impl(self):
        creators = self.head_creators + self.creators + self.tail_creators
        result = []
        result.append( "BOOST_PYTHON_MODULE(%s){" % self.name )
        result.append( compound.compound_t.create_internal_code( creators ) )
        result.append( "}" )
        return os.linesep.join( result )

    def _get_system_files_impl( self ):
        return []
