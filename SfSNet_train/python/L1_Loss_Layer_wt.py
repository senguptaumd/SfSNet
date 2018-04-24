import caffe, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class L1LossLayerWt(caffe.Layer):

    def setup(self, bottom, top):
        # check input pair
        if len(bottom) != 3:
            raise Exception("Need two inputs to compute distance.")
	param = json.loads( self.param_str )
	self.w_real=float( param['wt_real'] )
	self.w_syn=float( param['wt_syn'] )

    def reshape(self, bottom, top):
        # check input dimensions match
        if bottom[0].count != bottom[1].count:
            raise Exception("Inputs must have the same dimension.")
        # difference is shape of inputs
        self.diff = np.zeros_like(bottom[0].data, dtype=np.float32)
        # loss output is scalar
        top[0].reshape(1)

    def forward(self, bottom, top):

        self.diff[...] = bottom[0].data - bottom[1].data
	
	sum=0
	for i in range(0,bottom[0].num):
		if bottom[2].data[i]>0:
			wt=self.w_real
		else: 
			wt=self.w_syn
		tmp=wt*np.sum(np.abs(self.diff[i,...]))
		sum=sum+tmp
		
	top[0].data[...]=sum/bottom[0].num
	

    def backward(self, top, propagate_down, bottom):

        for i in range(2):
            if not propagate_down[i]:
                continue
            if i == 0:
                sign = 1
            else:
                sign = -1
            bottom[i].diff[...] = sign*np.sign(self.diff) / bottom[i].num

	    for j in range(0,bottom[0].num):
		if bottom[2].data[j]>0:
			wt=self.w_real
		else: 
			wt=self.w_syn
		bottom[i].diff[j,...]=wt*bottom[i].diff[j,...]


	

