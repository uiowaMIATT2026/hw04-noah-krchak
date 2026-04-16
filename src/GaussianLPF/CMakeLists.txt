
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

# --- Edge-case tests ---

# ITK's RecursiveGaussianImageFilter requires sigma > 0 and explicitly throws
# "Sigma must be greater than zero" for negative values, so EXIT_FAILURE is expected
add_test(NAME GaussianLPF_NegativeSigma
  COMMAND $<TARGET_FILE:GaussianLPF_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma -1.0
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/GaussianLPF_neg_sigma_out.nii.gz
)
set_tests_properties(GaussianLPF_NegativeSigma PROPERTIES WILL_FAIL TRUE)

# Zero sigma is also rejected by ITK with the same "Sigma must be greater than zero"
# exception, so EXIT_FAILURE is expected
add_test(NAME GaussianLPF_ZeroSigma
  COMMAND $<TARGET_FILE:GaussianLPF_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma 0.0
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/GaussianLPF_zero_sigma_out.nii.gz
)
set_tests_properties(GaussianLPF_ZeroSigma PROPERTIES WILL_FAIL TRUE)

# sigma=0.1 is the minimum value allowed by the XML constraints; the filter should
# apply very light smoothing and EXIT_SUCCESS
add_test(NAME GaussianLPF_BoundaryMinSigma
  COMMAND $<TARGET_FILE:GaussianLPF_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma 0.1
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/GaussianLPF_min_sigma_out.nii.gz
)

# sigma=5.0 is the maximum value allowed by the XML constraints; the filter should
# apply heavy smoothing across the volume and EXIT_SUCCESS
add_test(NAME GaussianLPF_BoundaryMaxSigma
  COMMAND $<TARGET_FILE:GaussianLPF_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma 5.0
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/GaussianLPF_max_sigma_out.nii.gz
)
