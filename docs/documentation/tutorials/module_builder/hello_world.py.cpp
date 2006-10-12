// This file has been generated by pyplusplus.

//Boost Software License( http://boost.org/more/license_info.html )

#include "boost/python.hpp"

#include "hello_world.hpp"

namespace bp = boost::python;

BOOST_PYTHON_MODULE(hw){
    bp::enum_<color>("Color")
        .value("blue", blue)
        .value("green", green)
        .value("red", red)
        .export_values()
        ;

    bp::class_< animal, boost::noncopyable >( "animal", bp::init< bp::optional< std::string const & > >(( bp::arg("name")="" )) )    
        .def("get_name_ptr"
                , &::animal::get_name_ptr
                , bp::return_internal_reference< 1, bp::default_call_policies >() )    
        .def("name"
                , &::animal::name
                , bp::return_value_policy< bp::copy_const_reference, bp::default_call_policies >() );

    bp::implicitly_convertible< std::string const &, animal >();
}