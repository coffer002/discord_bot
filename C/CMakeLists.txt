cmake_minimum_required(VERSION 4.3)
project(bot_engine_math C)

set(CMAKE_C_STANDARD 11)

#bot_engine_math
add_library(bot_engine_math_main SHARED bot_engine_math/library.c)

#bot_engine_monitor
add_library(bot_engine_monitor_main SHARED bot_engine_monitor/library.c)