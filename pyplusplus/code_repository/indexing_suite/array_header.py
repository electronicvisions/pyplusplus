# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
This file contains indexing suite v2 code
"""

file_name = "indexing_suite/array.hpp"

code = """// This file has been generated by Py++.

// This file has been generated by Py++.

// This file has been generated by Py++.

// This file has been generated by Py++.

// This file has been generated by Py++.

// Copyright (c) 2013 Christoph Koke
//
// Use, modification and distribution is subject to the Boost Software
// License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy
// at http://www.boost.org/LICENSE_1_0.txt)
//
// Header file array.hpp
//
// Indexing algorithms support for std::array instances
//

#ifndef BOOST_PYTHON_INDEXING_ARRAY_HPP
#define BOOST_PYTHON_INDEXING_ARRAY_HPP

#include <array>

#include <indexing_suite/container_traits.hpp>
#include <indexing_suite/container_suite.hpp>
#include <indexing_suite/algorithms.hpp>
#include <indexing_suite/suite_utils.hpp>

#include <boost/python/return_internal_reference.hpp>
#include <boost/type_traits/has_operator.hpp>

namespace boost { namespace python { namespace indexing {
	/////////////////////////////////////////////////////////////////////////
	// ContainerTraits implementation for std::list instances
	/////////////////////////////////////////////////////////////////////////

	namespace detail {
		template<typename T>
		struct is_array	{
			static const bool value = false;
		};

		template <typename T, size_t N>
		struct is_array< std::array<T, N> > {
			static const bool value = true;
		};

		template <typename T, bool>
		struct get_equal_to {
			typedef std::equal_to<T> equal_to;
		};

		template <typename T>
		struct get_equal_to<T, false> {};

		template <typename T, bool>
		struct get_less {
			typedef std::less<T> less;
		};

		template <typename T>
		struct get_less<T, false> {};

		template <typename T>
		struct array_has_equal_to {
			BOOST_STATIC_ASSERT(!is_pointer<T>::value);
			static const bool value = has_equal_to<T>::value;
		};

		template <typename T, size_t N>
		struct array_has_equal_to< std::array<T, N> > {
			static const bool value = array_has_equal_to<T>::value;
		};

		template<typename T>
		class has_array_base
		{
			private:
				// better match if SFINAE doesn't fail
				typedef char true_type;
				template<typename U, size_t N>
				static typename std::enable_if<
				    std::is_base_of<std::array<U, N>, T>::value, true_type>::type
				test(std::array<U, N> const*);

				typedef int false_type;
				static false_type test(...);
			public:
				static const bool value =
					(sizeof(test((T const*)NULL))==sizeof(true_type));
		};

		// X : public std::array<T, 3>
		template <typename T, typename = void>
		struct array_has_less
		{
			static const bool value = boost::has_less<T>::value;
		};

		template <typename T>
		struct array_has_less<T,
			typename std::enable_if<!is_array<T>::value && has_array_base<T>::value>::type>
		{
			static const bool value = array_has_less<typename T::value_type>::value;
		};

		template <typename T, size_t N>
		struct array_has_less< std::array<T, N>, void>
		{
			static const bool value = array_has_less<T>::value;
		};

	} // end detail

	template <class T>
	struct array_value_traits :
		detail::get_equal_to<T, detail::array_has_equal_to<T>::value>,
		detail::get_less<T, detail::array_has_less<T>::value>
	{
		BOOST_STATIC_CONSTANT(bool, equality_comparable = detail::array_has_equal_to<T>::value);
		BOOST_STATIC_CONSTANT(bool, less_than_comparable = detail::array_has_less<T>::value);

		// Default, do-nothing, version of visit_container_class
		template<typename PythonClass, typename Policy>
		static void visit_container_class (PythonClass &, Policy const &) { }
	};

	template<
		typename Container,
		typename ValueTraits = array_value_traits<typename Container::value_type>
	 >
	 class array_traits : public base_container_traits<Container, ValueTraits>
	 {
		 typedef base_container_traits<Container, ValueTraits> base_class;

	 public:
		 typedef typename base_class::value_traits_type value_traits_type;

		 typedef BOOST_DEDUCED_TYPENAME mpl::if_<
			 mpl::or_<is_fundamental<BOOST_DEDUCED_TYPENAME base_class::value_type>
				, is_enum<BOOST_DEDUCED_TYPENAME base_class::value_type> >,
			 default_container_policies,
			 return_internal_reference<>
				 >::type policy_type;

		 BOOST_STATIC_CONSTANT(method_set_type,
			 supported_methods = (
				   method_len
				 | method_iter
				 | method_getitem
				 | method_getitem_slice

				 | detail::method_set_if<
					 value_traits_type::equality_comparable,
					 method_contains
					 | method_count
					 | method_index
					 | method_equal
				 >::value

				 | detail::method_set_if<
					 base_class::is_mutable,
					 method_reverse
					 | method_setitem
					 | method_setitem_slice
				 >::value

				 | detail::method_set_if<
						base_class::is_mutable && value_traits_type::less_than_comparable,
						method_sort
				  >::value

		));
	 };

#if !defined(BOOST_NO_TEMPLATE_PARTIAL_SPECIALIZATION)
namespace detail {
	///////////////////////////////////////////////////////////////////////
	// algorithms support for std::array instances
	///////////////////////////////////////////////////////////////////////

	template <class T, size_t N >
	class algorithms_selector< std::array<T, N> >
	{
		typedef std::array<T, N> Container;

		typedef array_traits<Container>       mutable_traits;
		typedef array_traits<Container const> const_traits;

		public:
		typedef default_algorithms<mutable_traits> mutable_algorithms;
		typedef default_algorithms<const_traits>   const_algorithms;
	};
}
#endif

template<
	class Container,
	method_set_type MethodMask = all_methods,
	class Traits = array_traits<Container>
	 >
struct array_suite
: visitor<default_algorithms<Traits>, BOOST_DEDUCED_TYPENAME Traits::policy_type, MethodMask>
{
};

} } }

#endif // BOOST_PYTHON_INDEXING_ARRAY_HPP


"""
