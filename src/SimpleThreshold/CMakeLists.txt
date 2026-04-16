
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

# --- Edge-case tests ---

# ITK's BinaryThresholdImageFilter explicitly checks that lower <= upper and throws
# an exception when that invariant is violated, so this must return EXIT_FAILURE
add_test(NAME SimpleThreshold_InvertedRange
  COMMAND $<TARGET_FILE:SimpleThreshold_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/SimpleThreshold_inverted_out.nii.gz
    --lowThreshold 100 --highThreshold 50
    --outsideValue 150 --insideValue 200
)
set_tests_properties(SimpleThreshold_InvertedRange PROPERTIES WILL_FAIL TRUE)

# A single-value range (low == high) is legal: only pixels whose intensity equals
# exactly 75 receive insideValue; all others receive outsideValue
add_test(NAME SimpleThreshold_SingleValueRange
  COMMAND $<TARGET_FILE:SimpleThreshold_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/SimpleThreshold_single_out.nii.gz
    --lowThreshold 75 --highThreshold 75
    --outsideValue 150 --insideValue 200
)

# When insideValue and outsideValue are identical the output image is uniform
# regardless of which pixels fall inside the threshold range; still EXIT_SUCCESS
add_test(NAME SimpleThreshold_InsideEqualsOutside
  COMMAND $<TARGET_FILE:SimpleThreshold_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/SimpleThreshold_uniform_out.nii.gz
    --lowThreshold 50 --highThreshold 100
    --outsideValue 100 --insideValue 100
)

# A full-range threshold (0 to 255) means every pixel is "inside", so the entire
# output image is set to insideValue; must EXIT_SUCCESS
add_test(NAME SimpleThreshold_FullRange
  COMMAND $<TARGET_FILE:SimpleThreshold_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/SimpleThreshold_full_out.nii.gz
    --lowThreshold 0 --highThreshold 255
    --outsideValue 150 --insideValue 200
)
