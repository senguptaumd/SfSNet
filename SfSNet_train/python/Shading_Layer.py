import caffe
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class ShadingLayer(caffe.Layer):

    def setup(self, bottom, top):
        # check input pair
        if len(bottom) != 2:
            raise Exception("Need two input.")

    def reshape(self, bottom, top):
	top[0].reshape(*bottom[0].data.shape)


    def forward(self, bottom, top):
	sz=bottom[0].data.shape

	att = np.pi*np.array([1, 2.0/3, 0.25])

	c1=att[0]*(1.0/np.sqrt(4*np.pi))
        c2=att[1]*(np.sqrt(3.0/(4*np.pi)))
	c3=att[2]*0.5*(np.sqrt(5.0/(4*np.pi)))
    	c4=att[2]*(3.0*(np.sqrt(5.0/(12*np.pi))))
	c5=att[2]*(3.0*(np.sqrt(5.0/(48*np.pi))))

	for i in range(0,sz[0]) :
		nx=bottom[0].data[i,0,...]
		ny=bottom[0].data[i,1,...]		
		nz=bottom[0].data[i,2,...]	


		H1=c1*np.ones((sz[2],sz[3]))
		H2=c2*nz
		H3=c2*nx
		H4=c2*ny
		H5=c3*(2*nz*nz - nx*nx -ny*ny)
		H6=c4*nx*nz
		H7=c4*ny*nz
		H8=c5*(nx*nx - ny*ny)
		H9=c4*nx*ny	


		for j in range(0,3) :
			L=bottom[1].data[i,j*9:(j+1)*9]
			top[0].data[i,j,:,:]=L[0]*H1+L[1]*H2+L[2]*H3+L[3]*H4+L[4]*H5+L[5]*H6+L[6]*H7+L[7]*H8+L[8]*H9



    def backward(self, top, propagate_down, bottom):

	sz=bottom[0].data.shape
	sz1=bottom[1].data.shape
	att = np.pi*np.array([1, 2.0/3, 0.25])
	c1=att[0]*(1.0/np.sqrt(4*np.pi))
        c2=att[1]*(np.sqrt(3.0/(4*np.pi)))
	c3=att[2]*0.5*(np.sqrt(5.0/(4*np.pi)))                                  
	c4=att[2]*(3.0*(np.sqrt(5.0/(12*np.pi))))                               
	c5=att[2]*(3.0*(np.sqrt(5.0/(48*np.pi))))
	#for normals
	
	
	for i in range(0,sz[0]) :
		nx=bottom[0].data[i,0,...]
		ny=bottom[0].data[i,1,...]		
		nz=bottom[0].data[i,2,...]
		dSx=np.zeros((sz[2],sz[3]))
 		dSy=np.zeros((sz[2],sz[3]))
		dSz=np.zeros((sz[2],sz[3]))

		H1=c1*np.ones((sz[2],sz[3]))
		H2=c2*nz
		H3=c2*nx
		H4=c2*ny
		H5=c3*(2*nz*nz - nx*nx -ny*ny)
		H6=c4*nx*nz
		H7=c4*ny*nz
		H8=c5*(nx*nx - ny*ny)
		H9=c4*nx*ny
		dL=np.zeros(sz1[1])

		for j in range(0,3) :
				L=bottom[1].data[i,j*9:(j+1)*9]
				Sx=c2*L[2]+(2*c5*L[7]-2*c3*L[4])*nx+c4*L[5]*nz+c4*L[8]*ny
				Sy=c2*L[3] -(2*c3*L[4]+2*c5*L[7])*ny + c4*L[6]*nz + c4*L[8]*nx
				Sz=c2*L[1]+4*c3*L[4]*nz+c4*L[5]*nx+c4*L[6]*ny

				dSx=dSx + top[0].diff[i,j,:,:]*Sx
				dSy=dSy + top[0].diff[i,j,:,:]*Sy
				dSz=dSz + top[0].diff[i,j,:,:]*Sz

				for kk in range(0,9) :
				    dL[j*9+kk]=np.sum(top[0].diff[i,j,:,:]*(locals()['H{0}'.format(kk+1)])); 

		bottom[0].diff[i,0,:,:]=dSx
		bottom[0].diff[i,1,:,:]=dSy
		bottom[0].diff[i,2,:,:]=dSz
		bottom[1].diff[i,:]=np.reshape(dL,(1,sz1[1]))

	
