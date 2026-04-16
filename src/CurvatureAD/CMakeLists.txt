
set(CurvatureAD_SOURCE CurvatureAD.cxx)
GENERATECLP(CurvatureAD_SOURCE CurvatureAD.xml)


add_executable(CurvatureAD_${MYHAWKID} ${CurvatureAD_SOURCE})
target_link_libraries(CurvatureAD_${MYHAWKID} ${ITK_LIBRARIES})

set(DATA /nfsscratch/opt/ece5490/data)

# README example: conductance=2.0, timeStep=0.1, iterations=5
add_test(NAME CurvatureAD_ExampleParams
  COMMAND $<TARGET_FILE:CurvatureAD_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --conductance 2.0 --timeStep 0.1 --iterations 5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_out.nii.gz
)

# Verify the output file was actually written
add_test(NAME CurvatureAD_OutputCreated
  COMMAND ${CMAKE_COMMAND} -E md5sum
    ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_out.nii.gz
)
set_tests_properties(CurvatureAD_OutputCreated PROPERTIES
  DEPENDS CurvatureAD_ExampleParams
)

# A missing input file must cause EXIT_FAILURE
add_test(NAME CurvatureAD_MissingInput
  COMMAND $<TARGET_FILE:CurvatureAD_${MYHAWKID}>
    --inputVolume /nonexistent/file.nii.gz
    --conductance 2.0 --timeStep 0.1 --iterations 5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_missing_out.nii.gz
)
set_tests_properties(CurvatureAD_MissingInput PROPERTIES WILL_FAIL TRUE)
