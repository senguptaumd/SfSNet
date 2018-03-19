<!--<h3><b>SfSNet</b></h3>-->
## <b>SfSNet : Learning Shape, Reflectance and Illuminance of Faces in the Wild</b> [[Project Page]](http://senguptaumd.github.io/SfSNet/) <br>
[Soumyadip Sengupta](http://legacydirs.umiacs.umd.edu/~sengupta/), [Angjoo Kanazawa](http://www.cs.berkeley.edu/~kanazawa/), [Carlos D. Castillo](http://legacydirs.umiacs.umd.edu/~carlos/), [David W. Jacobs](https://www.cs.umd.edu/~djacobs/). In [CVPR, 2018 (Spotlight)](https://arxiv.org/pdf/1712.01261.pdf).

<img src="https://github.com/senguptaumd/SfSNet/blob/gh-pages/resources/Teaser1.png" width="500px" >

### Overview:
 - (0) Test script: test_SfSNet.m
 - (1) Test images along with mask: Images_mask
 - (2) Test images without mask: Images

Note: We detect keypoints on the face and compute a mask from it. The keypoint detections are based on . Unfortunately the code is not distributable. Ideally, you can use any keypoint detector and generate a mask based on the facial contour.

### Dependencies ###
This code requires a working installation of [Caffe](http://caffe.berkeleyvision.org/) and Matlab interface for Caffe. For guidelines and help with installation of Caffe, consult the [installation guide](http://caffe.berkeleyvision.org/) and [Caffe users group](https://groups.google.com/forum/#!forum/caffe-users).

Please set the variable PATH_TO_CAFFE_MATLAB, in line 3 of test_SfSNet.m as $PATH_TO_CAFFE/matlab (path to matlab folder for the caffe installation)

