import os
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
import cv2
import caffe
import spherical_harmonics

# caffe.set_mode_cpu();
caffe.set_device(0);
caffe.set_mode_gpu();

model = 'SfSNet_deploy.prototxt'
weights = 'SfSNet.caffemodel.h5'
net = caffe.Net(model, weights, caffe.TEST)

# Choose Dataset
dat_idx = input('Please enter 1 for images with masks and 0 for images without mask: ')
dat_idx = int(dat_idx)
if dat_idx == 1:
    # Images and masks are provided
    list_im = os.listdir('Images_mask/');
    list_im = list(filter(lambda f: f.endswith('_face.png'), list_im))
    list_im.sort()
elif dat_idx == 0:
    # No mask provided (Need to use your own mask).
    list_im = os.listdir('Images/');
    list_im = list(filter(lambda f: f.endswith('.png'), list_im))
    list_im.sort()
else:
    print('Wrong Option!');
    sys.exit(1)

fig, axs = plt.subplots(2, 3, figsize=(24,16))
for i in range(2):
    for j in range(3):
        axs[i][j].axis('off')
axs[0][0].set_title('Image')
axs[0][1].set_title('Normal')
axs[0][2].set_title('Albedo')
axs[1][1].set_title('Shading')
axs[1][2].set_title('Recon')

M = 128; # size of input for SfSNet
for i in range(len(list_im)):
    if dat_idx == 1:
        im = cv2.imread(os.path.join('Images_mask/', list_im[i]));
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        mask = cv2.imread(os.path.join('Images_mask/', list_im[i].replace('face', 'mask')));
        mask = cv2.resize(mask, (M, M));
        mask = mask/255;
    else:
        im = cv2.imread(os.path.join('Images/', list_im[i]));
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    # Prepare images
    im = cv2.resize(im, (M, M))
    im = im.astype(np.float32)/255
    im_data = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    im_data = im_data.reshape((1,) + im_data.shape)
    im_data = im_data.transpose((0,3,1,2))

    # Pass images
    net.blobs['data'].data[...] = im_data
    output = net.forward();
    al_out = output['Aconv0'].transpose((0,2,3,1))[0]
    n_out  = output['Nconv0'].transpose((0,2,3,1))[0]
    light_out = output['fc_light'][0]

    # light_out is a 27 dimensional vector. 9 dimension for each channel of
    # RGB. For every 9 dimensional, 1st dimension is ambient illumination
    # (0th order), next 3 dimension is directional (1st order), next 5
    # dimension is 2nd order approximation. You can simply use 27
    # dimensional feature vector as lighting representation.

    # Transform
    n_out2 = cv2.cvtColor(n_out, cv2.COLOR_BGR2RGB)
    n_out2 = 2*n_out2-1; # [-1 1]
    n_out2 = n_out2/(np.expand_dims(np.linalg.norm(n_out2,axis=2),axis=2)+1e-10)

    al_out2 = cv2.cvtColor(al_out, cv2.COLOR_BGR2RGB)

    # Note: n_out2, al_out2, light_out is the actual output

    # Create reconstruction and shading image
    light_out_data = light_out.reshape((1,) + light_out.shape)
    n_out2_data = n_out2.reshape((1,) + n_out2.shape)
    Ishd = spherical_harmonics.compute_shading(light_out_data, n_out2_data)[0]
    Irec = Ishd*al_out2

    # Visualize light_out on a sphere (not included in test_SfSNet.m)
    sphere_normals = spherical_harmonics.get_sphere_normals()
    sphere_normals_data = sphere_normals.reshape((1,) + sphere_normals.shape)
    Ilight = spherical_harmonics.compute_shading(light_out_data, sphere_normals_data)[0]

    if dat_idx == 1:
        axs[0][0].imshow(mask*im)
        axs[0][1].imshow(mask*((1+n_out2)/2).clip(0,1))
        axs[0][2].imshow(mask*al_out2.clip(0,1))
        axs[1][0].imshow(Ilight.clip(0,1))
        axs[1][1].imshow(mask*200/255*Ishd.clip(0,1))
        axs[1][2].imshow(mask*Irec.clip(0,1))
    else:
        axs[0][0].imshow(im)
        axs[0][1].imshow(((1+n_out2)/2).clip(0,1))
        axs[0][2].imshow(al_out2.clip(0,1))
        axs[1][0].imshow(Ilight.clip(0,1))
        axs[1][1].imshow(200/255*Ishd.clip(0,1))
        axs[1][2].imshow(Irec.clip(0,1))

    input('Press Enter to Continue')
