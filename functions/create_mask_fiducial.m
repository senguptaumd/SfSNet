function [] = create_mask_fiducial(fiducials,Image)
%fiducals is 2x68 
border_fid=fiducials(:,1:17);
face_fid=fiducials(:,18:end);

c1=[border_fid(1,1); face_fid(2,3)]; %left
c2=[border_fid(1,17); face_fid(2,8)]; %right
eye=norm(face_fid(:,23)-face_fid(:,26));
c3=face_fid(:,3); c3(2)=c3(2)-0.3*eye;
c4=face_fid(:,8); c4(2)=c4(2)-0.3*eye;
border=[c1 border_fid c2 c4 c3];
        
M=size(Image,1);
        
[X,Y]=meshgrid(1:M,1:M);
[in,on]=inpolygon(X(:),Y(:),border(1,:)',border(2,:)');
mask=round(reshape(in|on,[M M])); Mask=repmat(255*uint8(mask),[1 1 3]);