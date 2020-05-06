<!--<h3><b>SfSNet</b></h3>-->
## <b>SfSNet : Learning Shape, Reflectance and Illuminance of Faces in the Wild</b> [[Project Page]](http://senguptaumd.github.io/SfSNet/) <br>
[Soumyadip Sengupta](http://legacydirs.umiacs.umd.edu/~sengupta/), [Angjoo Kanazawa](http://www.cs.berkeley.edu/~kanazawa/), [Carlos D. Castillo](http://legacydirs.umiacs.umd.edu/~carlos/), [David W. Jacobs](https://www.cs.umd.edu/~djacobs/). In [CVPR, 2018 (Spotlight)](https://arxiv.org/pdf/1712.01261.pdf).

<img src="https://github.com/senguptaumd/SfSNet/blob/gh-pages/resources/Teaser1.png" width="500px" >

### Overview
 - (0) Test script: `test_SfSNet.m`
 - (1) Test images along with mask: Images_mask
 - (2) Test images without mask: Images
 
Run 'test_SfSNet' on Matlab to run SfSNet on the supplied test images. 

### Dependencies ###
This code requires a working installation of [Caffe](http://caffe.berkeleyvision.org/) and Matlab interface for Caffe. For guidelines and help with installation of Caffe, consult the [installation guide](http://caffe.berkeleyvision.org/) and [Caffe users group](https://groups.google.com/forum/#!forum/caffe-users).

Please set the variable `PATH_TO_CAFFE_MATLAB`, in line 3 of `test_SfSNet.m` as `$PATH_TO_CAFFE/matlab` (path to matlab folder for the caffe installation)

### Notes
We detect keypoints on the face using <a href="https://arxiv.org/abs/1611.00851">All-in-One Network</a> and compute a mask from it. Unfortunately the code is not distributable. Ideally, you can use any keypoint detector and generate a mask based on the facial contour.

For the ease of use, we include a matlab function `functions/create_mask_fiducial.m` which computes a mask given keypoints. The keypoint definitions are shown in `functions/facial_landmarks_68markup-768x619.jpg`. [Dlib C++ Library](http://dlib.net/) can be used to detect 68 keypoints based on this definition.

### Training Code
We provided neccessary .prototxt training and solver files, along with python loss layers needed to train SfSNet. Please check `SfSNet_train` for more details.

### Training Data
We provide [250k synthetic face images](https://drive.google.com/file/d/1UQONt9Usk3PKztSIoXeNUEUqD5s6z69e/view?usp=sharing) with Ground-Truth normal, albedo and lighting at 512x512 resolution generated with [3DMM](http://gravis.dmi.unibas.ch/Sigg99.html). Caution the file size is ~120GB. This data is provided only for research purposes.

##### Note: Please fill out this [form](https://goo.gl/forms/lLTaT4KYgGQAmBhh2) to request access to the synthetic data.

For real data, please download the aligned and cropped [CelebA face dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html).

### License
Copyright 2018 University of Maryland

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


### Citation
If you use this code for your research, please consider citing:
```
@InProceedings{sfsnetSengupta18,
  title={SfSNet: Learning Shape, Refectance and Illuminance of Faces in the Wild},
  author = {Soumyadip Sengupta and Angjoo Kanazawa and Carlos D. Castillo and David W. Jacobs},
  booktitle={Computer Vision and Pattern Regognition (CVPR)},
  year={2018}
}
```
