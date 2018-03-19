function o = lambertian_attenuation(n)
%a = [.8862; 1.0233; .4954];
a = pi*[1,2/3,.25];
if n > 3
   error('didnt record more than 3 attenuations');
end
o = a(1:n);
