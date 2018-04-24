import caffe
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class ChangeFormLayer(caffe.Layer):

    def setup(self, bottom, top):
        # check input pair
        if len(bottom) != 1:
            raise Exception("Need one input.")

    def reshape(self, bottom, top):
	top[0].reshape(*bottom[0].data.shape)


    def forward(self, bottom, top):
	top[0].data[:,0,:,:]=bottom[0].data[:,2,:,:]; top[0].data[:,1,:,:]=bottom[0].data[:,1,:,:]; top[0].data[:,2,:,:]=bottom[0].data[:,0,:,:];

    def backward(self, top, propagate_down, bottom):
	bottom[0].diff[:,0,:,:]=top[0].diff[:,2,:,:]; bottom[0].diff[:,1,:,:]=top[0].diff[:,1,:,:]; bottom[0].diff[:,2,:,:]=top[0].diff[:,0,:,:];

