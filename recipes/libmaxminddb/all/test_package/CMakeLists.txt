cmake_minimum_required(VERSION 3.1)
project(PackageTest C)

find_package(PkgConfig)
pkg_check_modules(LIBMAXMINDDB REQUIRED "libmaxminddb")

add_executable(example example.c)
target_include_directories(example PUBLIC ${LIBMAXMINDDB_INCLUDE_DIRS})
target_link_libraries(example ${LIBMAXMINDDB_LIBRARIES})
