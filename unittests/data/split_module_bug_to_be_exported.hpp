// Copyright 2004 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __split_module_bug_to_be_exported_hpp__
#define __split_module_bug_to_be_exported_hpp__

typedef struct opaque_ *opaque_pointer;

inline opaque_pointer get_opaque(){ return 0; }


#endif//__split_module_to_be_exported_hpp__
