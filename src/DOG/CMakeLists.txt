
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

# --- Edge-case tests ---

# ITK's RecursiveGaussianImageFilter throws "Sigma must be greater than zero" for
# sigma1 <= 0, so a negative sigma1 must cause EXIT_FAILURE
add_test(NAME DOG_NegativeSigma1
  COMMAND $<TARGET_FILE:DOG_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma1 -1.0 --sigma2 3.5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/DOG_neg_sigma1_out.nii.gz
)
set_tests_properties(DOG_NegativeSigma1 PROPERTIES WILL_FAIL TRUE)

# ITK throws the same "Sigma must be greater than zero" exception for sigma2 == 0,
# so zero sigma2 must cause EXIT_FAILURE
add_test(NAME DOG_ZeroSigma2
  COMMAND $<TARGET_FILE:DOG_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma1 2.5 --sigma2 0.0
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/DOG_zero_sigma2_out.nii.gz
)
set_tests_properties(DOG_ZeroSigma2 PROPERTIES WILL_FAIL TRUE)

# Reversing the sigma order (sigma1 > sigma2) is mathematically valid: the subtraction
# Gsigma1 - Gsigma2 simply produces an inverted (negative) edge response which is then
# rescaled to [0,255] by the RescaleIntensityImageFilter; must EXIT_SUCCESS
add_test(NAME DOG_ReversedSigmas
  COMMAND $<TARGET_FILE:DOG_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma1 3.5 --sigma2 2.5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/DOG_reversed_out.nii.gz
)

# Very close but unequal sigmas pass the sigma1 != sigma2 guard; the DOG response
# will be very faint (small difference between the two Gaussians) but must EXIT_SUCCESS
add_test(NAME DOG_CloseSigmas
  COMMAND $<TARGET_FILE:DOG_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --sigma1 2.5 --sigma2 2.6
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/DOG_close_sigma_out.nii.gz
)
