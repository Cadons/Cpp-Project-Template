# Source files
set(SOURCES
        src/MyClassLib.cpp
)
#headers
set(HEADERS
        include/MyClassLib.h
)
configure_build(mylib)
# Create executable
add_library(mylib ${SOURCES} ${HEADERS})
target_include_directories(mylib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)