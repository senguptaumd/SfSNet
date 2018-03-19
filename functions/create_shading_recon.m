function [IRen0,Ishd0]=  create_shading_recon(n_out2,al_out2,light_out)
M=size(n_out2,1);
No1=reshape(n_out2,[M*M 3]);
tex1=reshape(al_out2,[M*M 3]);

la = lambertian_attenuation(3);
HN1 = normal_harmonics(No1', la);

HS1r=HN1*light_out(1:9); HS1g=HN1*light_out(10:18); HS1b=HN1*light_out(19:27); 
HS1(:,:,1)=reshape(HS1r,[M M]); HS1(:,:,2)=reshape(HS1g,[M M]); HS1(:,:,3)=reshape(HS1b,[M M]); 
Tex1=reshape(tex1,[M M 3]).*HS1;


IRen0=Tex1;
Shd=(200/255)*HS1; %200 is added instead of 255 so that not to scale the shading to all white
Ishd0=Shd;
end
