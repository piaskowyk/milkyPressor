cmake_minimum_required(VERSION 3.1)
project(data-compressor-app C)
# project(data-compressor-app CXX)

# set(CMAKE_C_COMPILER /usr/bin/gcc CACHE PATH "")
# set(CMAKE_CXX_COMPILER /usr/bin/g++ CACHE PATH "")

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_EXTENSIONS OFF)

add_compile_options(-Wall -Wextra)

# add_library(${PROJECT_NAME} SHARED src/time_object.cpp)
# target_include_directories(${PROJECT_NAME} PRIVATE "./src")
find_package(anjay REQUIRED)
# add_executable(${PROJECT_NAME} src/main.cpp)
add_executable(${PROJECT_NAME}
                src_notify/main.c
                src_notify/time_object.h
                src_notify/time_object.c)
target_link_libraries(${PROJECT_NAME} PRIVATE anjay)