import caffe
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class NormLayer(caffe.Layer):

    def setup(self, bottom, top):
        # check input pair
        if len(bottom) != 1:
            raise Exception("Need one input.")

    def reshape(self, bottom, top):
	top[0].reshape(*bottom[0].data.shape)

    def forward(self, bottom, top):
	sz=bottom[0].data.shape
	nor=bottom[0].data
	nor=2*nor-1
        
	ssq=np.linalg.norm(nor,axis=1)
	ssq=np.reshape(ssq,(sz[0],1,sz[2],sz[3]))
	norm=np.tile(ssq,(1,sz[1],1,1)) + 1e-8
	top[0].data[...]=np.divide(nor,norm)

    def backward(self, top, propagate_down, bottom):
	sz=bottom[0].data.shape
	nor=bottom[0].data
	nor=2*nor-1
	sc=np.sqrt(np.sum(np.multiply(nor,nor),axis=1,keepdims=True)) + 1e-8
	sc=np.tile(sc,(1,sz[1],1,1))
	
	for i in range(0,sz[0]):
		Ey=top[0].diff[i,...]
		ip=np.sum(np.multiply(Ey,top[0].data[i,...]),axis=0,keepdims=True)
		ip=np.tile(ip,(sz[1],1,1))
		bottom[0].diff[i,...]=2*np.divide(Ey - top[0].data[i,...]*ip,sc[i,...])




