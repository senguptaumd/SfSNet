### SfSNet Training Code:

License: 

Please do not redistribute the code. The testing code is published at: https://senguptaumd.github.io/SfSNet/. Feel free to use that.
The training code is provided to individuals based on specific cases and requirements.

Disclaimer:

The SOFTWARE PACKAGE provided in this page is provided "as is", without any guarantee made as to its suitability or fitness for any particular use. It may contain bugs, so use of this tool is at your own risk. We take no responsibility for any damage of any sort that may unintentionally be caused through its use.

FILES:

Training files: sfsnet_train.prototxt | solver_sfsnet_train.prototxt
'python' folder contains neccessary python files for computing the loss. These files should be placed at $PATH_TO_CAFFE/python. 


DATA:
Check sfsnet_train.prototxt to see data loading

'Data': HDF5 Data format of caffe containing image and 27 dimensional lighting vector. Check HDF5 data layer of caffe for details
'Mask': Uses Caffe ImageData layer. Provide a .txt file with each row containing (a) path to a mask image (b) a label where +1 indicates real and -1 indicates synthetic. Check the loss files to see how 		labels can be used for different weights on real and synthetic data.
'Normal', 'Albedo': Same format as 'Mask' layer 



