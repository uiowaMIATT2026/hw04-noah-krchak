# What parameters did you choose to achieve good smoothing without losing to much edge detail?

Image used: MRHead example from Slicer

CurvatureAD is also based on AnisotropicDiffusionImageFilter and AnisotropicDiffusionFunction. The discussion
below is a copy of the discussion in GradientAD README.MD since they use the parameters for their
algorithms.

Time step plays a very significant role in gradient anisotropic diffusion. When the time step parameter
is greater than 0.3 the brain starts to lose its edges and fold details. When greater
than 0.5 wavy lines start to appear and the head becomes blurrier. As the time step parameter increases
further each plane just becomes waves.

Conductance plays a much smaller role where even increasing the parameter to 10000 does not result in the complete
loss of the image, only a slight blurring of edges within the image itself. According to ITK's documentation on anisotropic
diffusion function which is what is applied in curvature anisotropic diffusion conductance should be between 0.5 and 2.0
and time step should be between 0.125 and 0.0625. The Iterations parameter dictates how many times the time-step should be updated, and ITK
specifies that a general rule-of-thumb is that the higher number of iterations is the more diffused the image
becomes. Increasing iterations also increases computation time, where 5 iterations takes around
31.2 seconds to run the algorithm.

Therefore, the parameter range to start with should be the following:

- Time Step: 0.0625 - 0.125
- Conductance: 0.5 - 2.0
- Iterations: 5

Parameter set 1:

- Time Step: 0.125
- Conductance: 0.5
- Iterations: 5

Parameter set 2:

- Time Step: 0.125
- Conductance: 2.0
- Iterations: 5

Parameter set 3:

- Time Step: 0.0625
- Conductance: 0.5
- Iterations: 5

Parameter set 4:

- Time Step: 0.0625
- Conductance: 2.0
- Iterations: 5

Conclusion:

ADD LATER

