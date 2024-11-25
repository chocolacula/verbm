cmake_minimum_required(VERSION 3.19)

project(hello-reflection VERSION 0.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

enable_testing()

set(SOURCES
    main.cpp)

add_executable(${PROJECT_NAME} ${SOURCES})

include_directories(../library/include)
target_link_libraries(${PROJECT_NAME} PRIVATE reflection)
