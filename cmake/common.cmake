function(configure_build module_name)
    set(MODULE_OUTPUT_BASE "${CMAKE_BINARY_DIR}/build/${module_name}")

    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${MODULE_OUTPUT_BASE}/bin" PARENT_SCOPE)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${MODULE_OUTPUT_BASE}/lib" PARENT_SCOPE)
    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${MODULE_OUTPUT_BASE}/lib" PARENT_SCOPE)

    file(MAKE_DIRECTORY "${MODULE_OUTPUT_BASE}/bin")
    file(MAKE_DIRECTORY "${MODULE_OUTPUT_BASE}/lib")
endfunction()

function(configure_install target_name)
    install(TARGETS ${target_name}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)
    install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/
        DESTINATION include
        FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp")
endfunction()

function (configure_compiler cpp_standard)
    if(MSVC)
        add_compile_options(/W4 /WX)
    else()
        add_compile_options(-Wall -Wextra -Wpedantic -Werror)
    endif()

    set(CMAKE_CXX_STANDARD ${cpp_standard})
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    set(CMAKE_CXX_EXTENSIONS OFF)

endfunction()