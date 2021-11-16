cmake_minimum_required(VERSION 3.1)
project(data-compressor-app CXX)

set(CMAKE_C_COMPILER /usr/bin/gcc CACHE PATH "")
set(CMAKE_CXX_COMPILER /usr/bin/g++ CACHE PATH "")

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_EXTENSIONS OFF)

add_compile_options(-Wall -Wextra)

find_package(anjay REQUIRED)

add_executable(${PROJECT_NAME} src/main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE anjay)