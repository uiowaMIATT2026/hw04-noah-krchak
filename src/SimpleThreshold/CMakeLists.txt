
set(SimpleThreshold_SOURCE SimpleThreshold.cxx)
GENERATECLP(SimpleThreshold_SOURCE SimpleThreshold.xml)


add_executable(SimpleThreshold_${MYHAWKID} ${SimpleThreshold_SOURCE})
target_link_libraries(SimpleThreshold_${MYHAWKID} ${ITK_LIBRARIES})

set(DATA /nfsscratch/opt/ece5490/data)

# README example: pixels in [50,100] → 200 (inside), all others → 150 (outside)
add_test(NAME SimpleThreshold_ExampleParams
  COMMAND $<TARGET_FILE:SimpleThreshold_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/SimpleThreshold_out.nii.gz
    --lowThreshold 50 --highThreshold 100
    --outsideValue 150 --insideValue 200
)

# Verify the output file was actually written
add_test(NAME SimpleThreshold_OutputCreated
  COMMAND ${CMAKE_COMMAND} -E md5sum
    ${CMAKE_CURRENT_BINARY_DIR}/SimpleThreshold_out.nii.gz
)
set_tests_properties(SimpleThreshold_OutputCreated PROPERTIES
  DEPENDS SimpleThreshold_ExampleParams
)

# A missing input file must cause EXIT_FAILURE
add_test(NAME SimpleThreshold_MissingInput
  COMMAND $<TARGET_FILE:SimpleThreshold_${MYHAWKID}>
    --inputVolume /nonexistent/file.nii.gz
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/SimpleThreshold_missing_out.nii.gz
    --lowThreshold 50 --highThreshold 100
    --outsideValue 150 --insideValue 200
)
set_tests_properties(SimpleThreshold_MissingInput PROPERTIES WILL_FAIL TRUE)
