
set(DOG_SOURCE DOG.cxx)
GENERATECLP(DOG_SOURCE DOG.xml)


add_executable(DOG_${MYHAWKID} ${DOG_SOURCE})
target_link_libraries(DOG_${MYHAWKID} ${ITK_LIBRARIES})

set(DATA /nfsscratch/opt/ece5490/data)

# README example: sigma1=2.5, sigma2=3.5 producing a rescaled [0,255] edge image
add_test(NAME DOG_ExampleParams
  COMMAND $<TARGET_FILE:DOG_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma1 2.5 --sigma2 3.5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/DOG_out.nii.gz
)

# Verify the output file was actually written
add_test(NAME DOG_OutputCreated
  COMMAND ${CMAKE_COMMAND} -E md5sum
    ${CMAKE_CURRENT_BINARY_DIR}/DOG_out.nii.gz
)
set_tests_properties(DOG_OutputCreated PROPERTIES
  DEPENDS DOG_ExampleParams
)

# Equal sigma values must be rejected with EXIT_FAILURE
add_test(NAME DOG_EqualSigmas
  COMMAND $<TARGET_FILE:DOG_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma1 2.5 --sigma2 2.5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/DOG_equal_sigma_out.nii.gz
)
set_tests_properties(DOG_EqualSigmas PROPERTIES WILL_FAIL TRUE)

# A missing input file must cause EXIT_FAILURE
add_test(NAME DOG_MissingInput
  COMMAND $<TARGET_FILE:DOG_${MYHAWKID}>
    --inputVolume /nonexistent/file.nii.gz
    --sigma1 2.5 --sigma2 3.5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/DOG_missing_out.nii.gz
)
set_tests_properties(DOG_MissingInput PROPERTIES WILL_FAIL TRUE)
