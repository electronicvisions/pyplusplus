# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)
#
# Authors:
#   Allen Bierbaum
#
# This file defines overrides to the standard pyplusplus behavior
#

# --- Over ride the behavior of mdecl_wrapper ---- #
import pygccxml.declarations.mdecl_wrapper as mdecl_wrapper
pd = pygccxml.declarations

# Define the call redirector so it can return arguments
# This method will now return multiple arguments by
# concatenating the arguments returned from the individual calls.
# If the returns arguments are delcarations, then it will wrap them
# to create an mdecl holder.
def new_call_redirector_t__call__(self, *arguments, **keywords):
   results = []
   for d in self.decls:
      callable_ = getattr(d, self.name)
      answer = callable_( *arguments, **keywords )
      results.append( answer )
   
   #I assume that all functions will return same type:
   if not results:
      return
   
   # If all elements are a decl type
   # - Extract all decls and make a new decl wrapper
   if not False in [isinstance(x,(pd.declaration_t,pd.mdecl_wrapper_t)) for x in results]:
      all_decls = []
      for x in results:
         if isinstance( x, declaration.declaration_t ):
            all_decls.append(x)
         elif isinstance( x, mdecl_wrapper_t ):
            all_decls.extend(x.decls)
         else:
            assert False, "Should not get here"
      return mdecl_wrapper_t( all_decls )
   # Otherwise, just return the list
   else:
      return results

mdecl_wrapper.call_redirector_t.__call__ = new_call_redirector_t__call__

# Override the mdecl_wrapper_t.__getitem__ method

def new_mdecl_wrapper_t__getitem__(self,index):
   """Provide access to declaration.
      If passed a standard index, then return contained decl.
      Else call the getitem method of the contained decls.
   """
   if isinstance(index, (int, slice)):
      return self.decls[index]
   else:
      return self.__getattr__("__getitem__")(index)
mdecl_wrapper.mdecl_wrapper_t.__getitem__ = new_mdecl_wrapper_t__getitem__   
