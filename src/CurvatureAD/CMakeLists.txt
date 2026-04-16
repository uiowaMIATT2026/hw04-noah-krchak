
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

# --- Edge-case tests ---

# ITK does not validate the sign of the conductance parameter; a negative conductance
# inverts the edge-stopping function but does not throw. EXIT_SUCCESS is expected, though
# the output will be numerically meaningless
add_test(NAME CurvatureAD_NegativeConductance
  COMMAND $<TARGET_FILE:CurvatureAD_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --conductance -1.0 --timeStep 0.1 --iterations 5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_neg_conductance_out.nii.gz
)

# A timeStep of zero means each iteration adds nothing (delta * 0 = 0), so the filter
# acts as a no-op and the output equals the input; ITK does not throw, EXIT_SUCCESS
add_test(NAME CurvatureAD_ZeroTimeStep
  COMMAND $<TARGET_FILE:CurvatureAD_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --conductance 2.0 --timeStep 0.0 --iterations 5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_zero_dt_out.nii.gz
)

# ITK does not validate the sign of the timeStep; a negative timeStep runs the
# diffusion in reverse (sharpening rather than smoothing) but does not throw,
# so EXIT_SUCCESS is expected
add_test(NAME CurvatureAD_NegativeTimeStep
  COMMAND $<TARGET_FILE:CurvatureAD_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --conductance 2.0 --timeStep -0.1 --iterations 5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_neg_dt_out.nii.gz
)

# The CFL stability limit for 3D curvature anisotropic diffusion is 0.5/2^3 = 0.0625.
# timeStep=0.13 exceeds this limit; ITK issues a stderr warning about instability
# but does not throw and returns EXIT_SUCCESS (output may contain numerical artifacts)
add_test(NAME CurvatureAD_UnstableTimeStep
  COMMAND $<TARGET_FILE:CurvatureAD_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --conductance 2.0 --timeStep 0.13 --iterations 5
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_unstable_dt_out.nii.gz
)

# iterations=0 means the filter loop never executes, producing an output identical
# to the input; ITK does not throw for zero iterations, so EXIT_SUCCESS is expected
add_test(NAME CurvatureAD_ZeroIterations
  COMMAND $<TARGET_FILE:CurvatureAD_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --conductance 2.0 --timeStep 0.05 --iterations 0
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_zero_iter_out.nii.gz
)

# iterations=1 is the minimum XML-constrained value; a single filtering pass should
# produce a slightly smoothed image and EXIT_SUCCESS
add_test(NAME CurvatureAD_BoundaryMinIterations
  COMMAND $<TARGET_FILE:CurvatureAD_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --conductance 2.0 --timeStep 0.05 --iterations 1
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_min_iter_out.nii.gz
)

# iterations=20 is the maximum XML-constrained value; the filter should produce
# heavy smoothing over 20 passes and EXIT_SUCCESS
add_test(NAME CurvatureAD_BoundaryMaxIterations
  COMMAND $<TARGET_FILE:CurvatureAD_${MYHAWKID}>
    --inputVolume ${DATA}/noisy/T1_icbm_normal_1mm_pn3_rf40.nii
    --conductance 2.0 --timeStep 0.05 --iterations 20
    --outputVolume ${CMAKE_CURRENT_BINARY_DIR}/CurvatureAD_max_iter_out.nii.gz
)
