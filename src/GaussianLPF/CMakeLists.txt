
set(GaussianLPF_SOURCE GaussianLPF.cxx)
GENERATECLP(GaussianLPF_SOURCE GaussianLPF.xml)


add_executable(GaussianLPF_${MYHAWKID} ${GaussianLPF_SOURCE})
target_link_libraries(GaussianLPF_${MYHAWKID} ${ITK_LIBRARIES})

set(DATA /nfsscratch/opt/ece5490/data)

# README example: apply 3D Gaussian LPF with sigma=2.5 in all directions
add_test(NAME GaussianLPF_ExampleParams
  COMMAND $<TARGET_FILE:GaussianLPF_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma 2.5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/GaussianLPF_out.nii.gz
)

# Verify the output file was actually written
add_test(NAME GaussianLPF_OutputCreated
  COMMAND ${CMAKE_COMMAND} -E md5sum
    ${CMAKE_CURRENT_BINARY_DIR}/GaussianLPF_out.nii.gz
)
set_tests_properties(GaussianLPF_OutputCreated PROPERTIES
  DEPENDS GaussianLPF_ExampleParams
)

# A missing input file must cause EXIT_FAILURE
add_test(NAME GaussianLPF_MissingInput
  COMMAND $<TARGET_FILE:GaussianLPF_${MYHAWKID}>
    --inputVolume /nonexistent/file.nii.gz
    --sigma 2.5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/GaussianLPF_missing_out.nii.gz
)
set_tests_properties(GaussianLPF_MissingInput PROPERTIES WILL_FAIL TRUE)
