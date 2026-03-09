# How does sigma affect the smoothing and loss of image resolution?

As sigma increases the image becomes smoother and appears blurrier as edge information is lost. When sigma decreases
the image becomes less smooth and most edge information is kept. Keeping of edge information concides with the quality of image
resolution, if edge informaiton is lost, so too is the image resolution and vice versa. 

Low sigma values, from 0 - 1, have little affect on image resolution and smoothing. Sigma values between 2 and 3
have a noticeable effect on the image's smoothness and loss of image resolution. Once sigma reaches 8 the image starts
to become unrecognizable compared to the original image as it has become heavily smoothed and lost most of it's
resolution. Some images are unaffected by the same sigma value as shown in MRHead example
of Slicer. When selecting a sigma value of 8, the sagittal and axial planes become heavily smoothed
and lose some image resolution while the coronal plane remains largely unaffected. When the sigma value is 
increased to 20 the sagittal and axial planes become completely unrecognizable and lose most of their
image resolution whereas the coronal plane is lightly smoothed.

This suggests that gaussian smoothing has different affects depending on the change between neighboring pixels (i.e. edges).
If the image has many edges, those edges are smoothed over and the image resolution decreases in low values of sigma (i.e. 5 or 6).
If the image has fewer edges, the same smoothing does not occur until high values of sigma are reached (i.e. 20)