
set(GradientAD_SOURCE GradientAD.cxx)
GENERATECLP(GradientAD_SOURCE GradientAD.xml)


add_executable(GradientAD_${MYHAWKID} ${GradientAD_SOURCE})
target_link_libraries(GradientAD_${MYHAWKID} ${ITK_LIBRARIES})

set(DATA /nfsscratch/opt/ece5490/data)

# README example: conductance=2.0, timeStep=0.1, iterations=5
add_test(NAME GradientAD_ExampleParams
  COMMAND $<TARGET_FILE:GradientAD_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --conductance 2.0 --timeStep 0.1 --iterations 5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/GradientAD_out.nii.gz
)

# Verify the output file was actually written
add_test(NAME GradientAD_OutputCreated
  COMMAND ${CMAKE_COMMAND} -E md5sum
    ${CMAKE_CURRENT_BINARY_DIR}/GradientAD_out.nii.gz
)
set_tests_properties(GradientAD_OutputCreated PROPERTIES
  DEPENDS GradientAD_ExampleParams
)

# A missing input file must cause EXIT_FAILURE
add_test(NAME GradientAD_MissingInput
  COMMAND $<TARGET_FILE:GradientAD_${MYHAWKID}>
    --inputVolume /nonexistent/file.nii.gz
    --conductance 2.0 --timeStep 0.1 --iterations 5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/GradientAD_missing_out.nii.gz
)
set_tests_properties(GradientAD_MissingInput PROPERTIES WILL_FAIL TRUE)
