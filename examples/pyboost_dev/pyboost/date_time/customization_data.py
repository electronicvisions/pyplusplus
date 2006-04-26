#! /usr/bin/python
# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import sys
import settings

#I have small problem: not all function of instantiated template is instantiated
#I am looking for some flag that will forse them to be instantiated
#-fkeep-inline-functions
#-fno-default-inline
#-fno-implement-inlines
#-frepo
    
includes = [
    "boost/date_time/special_defs.hpp"
    , "boost/date_time/time_defs.hpp" 
    , "boost/date_time/date_defs.hpp" 
    , "boost/date_time/int_adapter.hpp"
    , "boost/date_time/gregorian/gregorian.hpp" 
    , "boost/date_time/posix_time/posix_time.hpp"
    , "boost/date_time/local_time/local_time.hpp"
    ,  os.path.join( settings.generated_files_dir, 'date_time_wrapper.hpp' )
]

name2alias = {    
    "months_duration<boost::gregorian::greg_durations_config>" 
        : "months"
    , "date_duration<boost::date_time::duration_traits_adapted>" 
        : "date_duration"
    , "counted_time_system<boost::date_time::counted_time_rep<boost::posix_time::millisec_posix_time_system_config> >" 
        : "counted_time_system_pyplusplus"
    , "gregorian_calendar_base<boost::date_time::year_month_day_base<boost::gregorian::greg_year, boost::gregorian::greg_month, boost::gregorian::greg_day>,long unsigned int>" 
        : "gregorian_calendar_base_pyplusplus"
    , "year_month_day_base<boost::gregorian::greg_year,boost::gregorian::greg_month,boost::gregorian::greg_day>" 
        : "year_month_day"
    , "date<boost::gregorian::date,boost::gregorian::gregorian_calendar,boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >" 
        : "date_pyplusplus"
    , "years_duration<boost::gregorian::greg_durations_config>" 
        : "years"
    , "base_time<boost::posix_time::ptime,boost::date_time::counted_time_system<boost::date_time::counted_time_rep<boost::posix_time::millisec_posix_time_system_config> > >" 
        : "base_time_pyplusplus"
    , "month_functor<boost::gregorian::date>" 
        : "month_functor_pyplusplus"
    , "period<boost::gregorian::date,boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >" 
        : "date_period"
    , "subsecond_duration<boost::posix_time::time_duration,1000>" 
        : "milliseconds"
    , "subsecond_duration<boost::posix_time::time_duration,1000000>" 
        : "microseconds"
    , "partial_date<boost::gregorian::date>" 
        : "partial_date"
    , "nth_kday_of_month<boost::gregorian::date>" 
        : "nth_kday_of_month"
    , "first_kday_of_month<boost::gregorian::date>" 
        : "first_kday_of_month"
    , "last_kday_of_month<boost::gregorian::date>" 
        : "last_kday_of_month"
    , "year_based_generator<boost::gregorian::date>" 
        : "gregorian_year_based_generator"
    , "first_kday_after<boost::gregorian::date>" 
        : "first_kday_after"
    , "first_kday_before<boost::gregorian::date>" 
        : "first_kday_before"
    , "constrained_value<boost::CV::simple_exception_policy<short unsigned int, 1, 366, boost::gregorian::bad_day_of_year> >" 
        : 'day_of_year_type'
    , "int_adapter<long unsigned int>" 
        : "int_adapter_ulong"
    , "int_adapter<long int>" 
        : "int_adapter_long"
    , "int_adapter<int>" 
        : "int_adapter_int"
    , "int_adapter<long long int>" 
        : "int_adapter_long_long_int"
    , "equality_comparable1<boost::posix_time::time_duration,boost::detail::empty_base>"
        : "__impl_details_1"
    , "equality_comparable1<boost::posix_time::ptime,boost::detail::empty_base>"
        : "__impl_details_2"
    , "subtractable1<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>,boost::detail::empty_base>" 
        : "__impl_details_3"
    , "subtractable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>,boost::date_time::date_duration<boost::date_time::duration_traits_adapted>,boost::detail::empty_base,boost::detail::false_t>" 
        : "__impl_details_4"
    , "addable1<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>,boost::subtractable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::detail::empty_base, boost::detail::false_t> >" 
        : "__impl_details_5"
    , "equality_comparable<boost::posix_time::time_duration,boost::posix_time::time_duration,boost::detail::empty_base,boost::detail::false_t>" 
        : "__impl_details_6"
    , "less_than_comparable1<boost::posix_time::time_duration,boost::equality_comparable<boost::posix_time::time_duration, boost::posix_time::time_duration, boost::detail::empty_base, boost::detail::false_t> >" 
        : "__impl_details_7"
    , "equality_comparable<boost::posix_time::ptime,boost::posix_time::ptime,boost::detail::empty_base,boost::detail::false_t>" 
        : "__impl_details_8"
    , "less_than_comparable1<boost::posix_time::ptime,boost::equality_comparable<boost::posix_time::ptime, boost::posix_time::ptime, boost::detail::empty_base, boost::detail::false_t> >" 
        : "__impl_details_9"
    , "less_than_comparable<boost::posix_time::ptime,boost::equality_comparable<boost::posix_time::ptime, boost::posix_time::ptime, boost::detail::empty_base, boost::detail::false_t>,boost::detail::empty_base,boost::detail::true_t>" 
        : "__impl_details_10"
    , "addable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>,boost::subtractable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::detail::empty_base, boost::detail::false_t>,boost::detail::empty_base,boost::detail::true_t>" 
        : "__impl_details_11"
    , "equality_comparable1<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>,boost::addable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::subtractable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::detail::empty_base, boost::detail::false_t>, boost::detail::empty_base, boost::detail::true_t> >" 
        : "__impl_details_12"
    , "equality_comparable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>,boost::addable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::subtractable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::detail::empty_base, boost::detail::false_t>, boost::detail::empty_base, boost::detail::true_t>,boost::detail::empty_base,boost::detail::true_t>" 
        : "__impl_details_13"
    , "less_than_comparable1<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>,boost::equality_comparable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::addable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::subtractable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::detail::empty_base, boost::detail::false_t>, boost::detail::empty_base, boost::detail::true_t>, boost::detail::empty_base, boost::detail::true_t> >" 
        : "__impl_details_14"
    , "less_than_comparable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>,boost::equality_comparable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::addable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::subtractable<boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::date_time::date_duration<boost::date_time::duration_traits_adapted>, boost::detail::empty_base, boost::detail::false_t>, boost::detail::empty_base, boost::detail::true_t>, boost::detail::empty_base, boost::detail::true_t>,boost::detail::empty_base,boost::detail::true_t>" 
        : "__impl_details_15"
    , "equality_comparable1<boost::date_time::period<boost::posix_time::ptime, boost::posix_time::time_duration>,boost::detail::empty_base>" 
        : "__impl_details_16"
    , "equality_comparable<boost::date_time::period<boost::posix_time::ptime, boost::posix_time::time_duration>,boost::date_time::period<boost::posix_time::ptime, boost::posix_time::time_duration>,boost::detail::empty_base,boost::detail::false_t>" 
        : "__impl_details_17"
    , "less_than_comparable1<boost::date_time::period<boost::posix_time::ptime, boost::posix_time::time_duration>,boost::equality_comparable<boost::date_time::period<boost::posix_time::ptime, boost::posix_time::time_duration>, boost::date_time::period<boost::posix_time::ptime, boost::posix_time::time_duration>, boost::detail::empty_base, boost::detail::false_t> >" 
        : "__impl_details_18"
    , "less_than_comparable<boost::date_time::period<boost::posix_time::ptime, boost::posix_time::time_duration>,boost::equality_comparable<boost::date_time::period<boost::posix_time::ptime, boost::posix_time::time_duration>, boost::date_time::period<boost::posix_time::ptime, boost::posix_time::time_duration>, boost::detail::empty_base, boost::detail::false_t>,boost::detail::empty_base,boost::detail::true_t>" 
        : "__impl_details_19"
    , "equality_comparable1<boost::date_time::period<boost::gregorian::date, boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >,boost::detail::empty_base>" 
        : "__impl_details_20"
    , "equality_comparable<boost::date_time::period<boost::gregorian::date, boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >,boost::date_time::period<boost::gregorian::date, boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >,boost::detail::empty_base,boost::detail::false_t>" 
        : "__impl_details_21"
    , "less_than_comparable1<boost::date_time::period<boost::gregorian::date, boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >,boost::equality_comparable<boost::date_time::period<boost::gregorian::date, boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >, boost::date_time::period<boost::gregorian::date, boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >, boost::detail::empty_base, boost::detail::false_t> >" 
        : "__impl_details_22"
    , "less_than_comparable<boost::date_time::period<boost::gregorian::date, boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >,boost::equality_comparable<boost::date_time::period<boost::gregorian::date, boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >, boost::date_time::period<boost::gregorian::date, boost::date_time::date_duration<boost::date_time::duration_traits_adapted> >, boost::detail::empty_base, boost::detail::false_t>,boost::detail::empty_base,boost::detail::true_t>" 
        : "__impl_details_23"
    , "equality_comparable1<boost::gregorian::date,boost::detail::empty_base>" 
        : "__impl_details_24"
    , "equality_comparable<boost::gregorian::date,boost::gregorian::date,boost::detail::empty_base,boost::detail::false_t>" 
        : "__impl_details_25"
    , "less_than_comparable1<boost::gregorian::date,boost::equality_comparable<boost::gregorian::date, boost::gregorian::date, boost::detail::empty_base, boost::detail::false_t> >" 
        : "__impl_details_26"
    , "less_than_comparable<boost::gregorian::date,boost::equality_comparable<boost::gregorian::date, boost::gregorian::date, boost::detail::empty_base, boost::detail::false_t>,boost::detail::empty_base,boost::detail::true_t>" 
        : "__impl_details_27"
    , "less_than_comparable<boost::posix_time::time_duration,boost::equality_comparable<boost::posix_time::time_duration, boost::posix_time::time_duration, boost::detail::empty_base, boost::detail::false_t>,boost::detail::empty_base,boost::detail::true_t>" 
        : "__impl_details_28"    
    , "equality_comparable1<boost::date_time::period<boost::local_time::local_date_time_base<boost::posix_time::ptime, boost::date_time::time_zone_base<boost::posix_time::ptime, char> >, boost::posix_time::time_duration>,boost::detail::empty_base>" 
        : "__impl_details_29"
    , "equality_comparable<boost::date_time::period<boost::local_time::local_date_time_base<boost::posix_time::ptime, boost::date_time::time_zone_base<boost::posix_time::ptime, char> >, boost::posix_time::time_duration>,boost::date_time::period<boost::local_time::local_date_time_base<boost::posix_time::ptime, boost::date_time::time_zone_base<boost::posix_time::ptime, char> >, boost::posix_time::time_duration>,boost::detail::empty_base,boost::detail::false_t>"
        : "__impl_details_30"
    , "less_than_comparable1<boost::date_time::period<boost::local_time::local_date_time_base<boost::posix_time::ptime, boost::date_time::time_zone_base<boost::posix_time::ptime, char> >, boost::posix_time::time_duration>,boost::equality_comparable<boost::date_time::period<boost::local_time::local_date_time_base<boost::posix_time::ptime, boost::date_time::time_zone_base<boost::posix_time::ptime, char> >, boost::posix_time::time_duration>, boost::date_time::period<boost::local_time::local_date_time_base<boost::posix_time::ptime, boost::date_time::time_zone_base<boost::posix_time::ptime, char> >, boost::posix_time::time_duration>, boost::detail::empty_base, boost::detail::false_t> >"
        : "__impl_details_31"
    , "less_than_comparable<boost::date_time::period<boost::local_time::local_date_time_base<boost::posix_time::ptime, boost::date_time::time_zone_base<boost::posix_time::ptime, char> >, boost::posix_time::time_duration>,boost::equality_comparable<boost::date_time::period<boost::local_time::local_date_time_base<boost::posix_time::ptime, boost::date_time::time_zone_base<boost::posix_time::ptime, char> >, boost::posix_time::time_duration>, boost::date_time::period<boost::local_time::local_date_time_base<boost::posix_time::ptime, boost::date_time::time_zone_base<boost::posix_time::ptime, char> >, boost::posix_time::time_duration>, boost::detail::empty_base, boost::detail::false_t>,boost::detail::empty_base,boost::detail::true_t>"
        : "__impl_details_32"
    , "wrapping_int2<short int,1,12>"
        : "__impl_details_33"
    , "time_zone_base<boost::posix_time::ptime,char>" 
        : "time_zone_base"
    , "dst_day_calc_rule<boost::gregorian::date>" 
        : "dst_calc_rule"
    , "day_calc_dst_rule<boost::local_time::nth_kday_rule_spec>"
        : "nth_kday_dst_rule"
    , "local_date_time_base<boost::posix_time::ptime,boost::date_time::time_zone_base<boost::posix_time::ptime, char> >"
        : "local_date_time"
    , "dst_calculator<boost::gregorian::date,boost::posix_time::time_duration>" 
        : "dst_calculator"   
    , "ymd_formatter<boost::date_time::year_month_day_base<boost::gregorian::greg_year, boost::gregorian::greg_month, boost::gregorian::greg_day>,boost::date_time::iso_extended_format<wchar_t>,wchar_t>"
        : "ymd_iso_extended_wformatter"
    , "ymd_formatter<boost::date_time::year_month_day_base<boost::gregorian::greg_year, boost::gregorian::greg_month, boost::gregorian::greg_day>,boost::date_time::iso_format<wchar_t>,wchar_t>"
        : "ymd_iso_wformatter"
    , "ymd_formatter<boost::date_time::year_month_day_base<boost::gregorian::greg_year, boost::gregorian::greg_month, boost::gregorian::greg_day>,boost::date_time::simple_format<wchar_t>,wchar_t>"
        : "ymd_simple_wformatter"
    , "ymd_formatter<boost::date_time::year_month_day_base<boost::gregorian::greg_year, boost::gregorian::greg_month, boost::gregorian::greg_day>,boost::date_time::iso_extended_format<char>,char>"
        : "ymd_iso_extended_formatter"
    , "ymd_formatter<boost::date_time::year_month_day_base<boost::gregorian::greg_year, boost::gregorian::greg_month, boost::gregorian::greg_day>,boost::date_time::iso_format<char>,char>"
        : "ymd_iso_formatter"
    , "ymd_formatter<boost::date_time::year_month_day_base<boost::gregorian::greg_year, boost::gregorian::greg_month, boost::gregorian::greg_day>,boost::date_time::simple_format<char>,char>"
        : "ymd_simple_formatter"
    , "date_formatter<boost::gregorian::date,boost::date_time::iso_format<wchar_t>,wchar_t>"
        : "date_iso_wformatter"
    , "date_formatter<boost::gregorian::date,boost::date_time::iso_extended_format<wchar_t>,wchar_t>"
        : "date_iso_extended_wformatter"
    , "date_formatter<boost::gregorian::date,boost::date_time::simple_format<wchar_t>,wchar_t>"
        : "date_simple_wformatter"
    , "date_formatter<boost::gregorian::date,boost::date_time::iso_format<char>,char>"
        : "date_iso_formatter"
    , "date_formatter<boost::gregorian::date,boost::date_time::iso_extended_format<char>,char>"
        : "date_iso_extended_formatter"
    , "date_formatter<boost::gregorian::date,boost::date_time::simple_format<char>,char>"
        : "date_simple_formatter"
    , "month_formatter<boost::gregorian::greg_month,boost::date_time::iso_extended_format<wchar_t>,wchar_t>"
        : "month_iso_extended_wformatter"
    , "month_formatter<boost::gregorian::greg_month,boost::date_time::iso_format<wchar_t>,wchar_t>"
        : "month_iso_wformatter"
    , "month_formatter<boost::gregorian::greg_month,boost::date_time::simple_format<wchar_t>,wchar_t>"
        : "month_simple_wformatter"
    , "month_formatter<boost::gregorian::greg_month,boost::date_time::iso_extended_format<char>,char>"
        : "month_iso_extended_formatter"
    , "month_formatter<boost::gregorian::greg_month,boost::date_time::iso_format<char>,char>"
        : "month_iso_formatter"
    , "month_formatter<boost::gregorian::greg_month,boost::date_time::simple_format<char>,char>"
        : "month_simple_formatter"
    , "iso_extended_format<wchar_t>"
        : "iso_extended_wformat"
    , "iso_extended_format<char>"
        : "iso_extended_format"
    , "iso_format<wchar_t>"
        : "iso_wformat"
    , "iso_format<char>"
        : "iso_format"
    , "iso_format_base<char>"
        : "iso_format_base"
    , "iso_format_base<wchar_t>"
        : "iso_wformat_base"
    , "simple_format<char>"
        : "simple_format"
    , "simple_format<wchar_t>"
        : "simple_wformat"
}

if sys.platform == 'win32':
    name2alias[ "time_duration<boost::posix_time::time_duration,boost::date_time::time_resolution_traits<boost::date_time::time_resolution_traits_adapted64_impl, micro, 1000000, 6, long int> >" ] \
        = "time_duration_impl"
else:
    name2alias[ "time_duration<boost::posix_time::time_duration,boost::date_time::time_resolution_traits<boost::date_time::time_resolution_traits_adapted64_impl, micro, 1000000, 6, int> >" ] \
        = "time_duration_impl"

alias2name = {}
for name, alias in name2alias.items():
    alias2name[ alias ] = name

#may be those names are uglier, but they are much short
ns_aliases = {
    '::boost::date_time' : 'dt'
    , '::boost::gregorian' : 'gr'
    , '::boost::posix_time' : 'pt'
    , '::boost::local_time' : 'lt'
}


license = """// Copyright 2004 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
"""