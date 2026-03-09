# How does the edge response change as sigma1 and sigma2 vary?
Image used: MRHead example in Slicer

Sigma 1 < 2.5 and Sigma 2 < 2.5 and Sigma 2 - Sigma 1 < 1:

This experiment combines low sigma values and sigma values that are close together i.e. the difference
between them is less than 1. The image appears grainy if sigma 1 and sigma 2 are within 0.1 apart and the edges do
not appear to be well defined. When the difference between sigma 1 and sigma 2 is increased to 1 the graininess
starts to disappear and the edges become more well-defined.

Sigma 1 > 2.5 and Sigma 2 > 2.5 and Sigma 2 - Sigma 1 < 5:

This experiment combines higher sigma values and a medium distance between them. The graininess in the image has almost disappeared
completely when sigma 1 = 2.5 and sigma 2 = 3.5, and most edges are present in the image
although they appear blurry as if they have been smoothed over. When sigma 2 increases to 7.5 and sigma 1 remains the same 2.5.
the edges appear blurrier but more edges appear in the image compared to when sigma 2 was 3.5.

Sigma 1 = 2.5 and Sigma 2 > 2.5 and Sigma 2 - Sigma 1 > 10:

This experiment compares high distance of sigma 1 and sigma 2. As the distance of sigma 1 and sigma 2 increases,
the original image starts to appear again albeit in a blurred state acting as the original GaussianLPF. As the distance increases
to 50 where sigma 2 = 52.5, a several dark/black streaks start to appear in the background of the image mainly in the axial and sagittal planes.
These black streaks continue to appear in those planes as the distance between sigma 1 and sigma 2 increase beyond 50, suggesting a loss of background
information in those planes.