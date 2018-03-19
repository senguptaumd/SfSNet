clc; clear;
%% TO DO: Add your Matcaffe path as $PATH_TO_CAFFE/matlab
addpath(genpath('/scratch2/photometric_stereo/caffe/matlab/'));

addpath(genpath('functions'));

model = 'SfSNet_deploy.prototxt';
weights='SfSNet.caffemodel.h5';

GPU_ID=0; %Set your GPU ID
caffe.set_mode_gpu();
caffe.set_device(GPU_ID);
net = caffe.Net(model, weights, 'test');


%% Choose Dataset
%Images and masks are provided
%list_im=dir('Images_mask/*_face.png'); dat_idx=1;


%No mask provided (Need to use your own mask).
list_im=dir('Images/*.png'); dat_idx=0; %Uncomment to test with this mode

M=128; %size of input for SfSNet
for i=1:length(list_im)
    
    if dat_idx
        im=imread(['Images_mask/' list_im(i).name]); im=imresize(im,[M M]);
        mask_name=['Images_mask/' strrep(list_im(i).name,'face','mask')];
        Mask=imread(mask_name); mask=single(Mask)/255; mask=imresize(mask,[M M]);
    else
        im=imread(['Images/' list_im(i).name]); im=imresize(im,[M M]);
    end
    
    %Prepare images
   im=reshape(im,[size(im)]); im=single(im)/255;
    im_data = im(:, :, [3, 2, 1]);  % permute channels from RGB to BGR
    im_data = permute(im_data, [2, 1, 3]); 
    
    %pass images  
    out_im = net.forward({im_data});
    n_out=out_im{2}; al_out=out_im{1}; light_out=out_im{3};
    
    %light_out is a 27 dimensional vector. 9 dimension for each channel of
    %RGB. For every 9 dimensional, 1st dimension is ambient illumination
    %(0th order), next 3 dimension is directional (1st order), next 5
    %dimension is 2nd order approximation. You can simply use 27
    %dimensional feature vector as lighting representation.
    
    %Transform
    n_out2=n_out(:,:,[3 2 1]); 
    n_out2=imrotate(n_out2,-90); n_out2=fliplr(n_out2);
    n_out2=2*n_out2-1; %[-1 1]
    nr=sqrt(sum(n_out2.^2,3)); n_out2=n_out2./repmat(nr,[1 1 3]);
    
    al_out2=imrotate(al_out,-90);
    al_out2=al_out2(:,:,[3 2 1]); al_out2=fliplr(al_out2);
    
    %% Note: n_out2, al_out2, light_out is the actual output
    
    [Irec,Ishd]=create_shading_recon(n_out2,al_out2,light_out);
    
    
    if dat_idx
        subplot(2,3,1); imshow(im); title('Image');
        subplot(2,3,2); imshow(((1+n_out2)/2).*mask + (1-mask).*ones(M,M,3)); title('Normal');
        subplot(2,3,3); imshow(al_out2.*mask+ (1-mask).*ones(M,M,3)); title('Albedo');
        subplot(2,3,5); imshow(Ishd.*mask+ (1-mask).*ones(M,M,3)); title('Shading');
        subplot(2,3,6); imshow(Irec.*mask+ (1-mask).*ones(M,M,3)); title('Recon');
    else
        subplot(2,3,1); imshow(im); title('Image');
        subplot(2,3,2); imshow((1+n_out2)/2); title('Normal');
        subplot(2,3,3); imshow(al_out2);  title('Albedo');
        subplot(2,3,5); imshow(Ishd); title('Shading');
        subplot(2,3,6); imshow(Irec); title('Recon');
    end
      
        disp('Press Enter to Continue');
        pause();
end

    
    
    
    
