import numpy as np

def normalize(arr, axis=0):
    """
    Normalize an array along a certain axis
    """
    return arr/(np.expand_dims(np.linalg.norm(arr,axis=axis),axis=axis)+1e-10)

def get_sphere_normals(image_size=512, sphere_radius=224):
    """
    Return the normals for a 2D image of a sphere
    """
    center_x, center_y = image_size//2, image_size//2
    sphere_normals = np.zeros((image_size,image_size,3))
    for i in range(image_size):
        for j in range(image_size):
            x = (i-center_x)/sphere_radius
            y = (j-center_y)/sphere_radius
            discriminant = 1-x*x-y*y
            if discriminant > 0:
                z = np.sqrt(discriminant)
                sphere_normals[i, j, 0] = x
                sphere_normals[i, j, 1] = y
                sphere_normals[i, j, 2] = z
            else:
                sphere_normals[i, j, :] = 0
    return sphere_normals

def get_sphere_mask(image_size=512, sphere_radius=224):
    """
    Return the mask for a 2D image of a sphere
    """
    center_x, center_y = image_size//2, image_size//2
    sphere_mask = np.zeros((image_size,image_size,3))
    for i in range(image_size):
        for j in range(image_size):
            x = (i-center_x)/sphere_radius
            y = (j-center_y)/sphere_radius
            discriminant = 1-x*x-y*y
            if discriminant > 0:
                sphere_mask[i, j, :] = 1
            else:
                sphere_mask[i, j, :] = 0
    return sphere_mask

def compute_shading(lights, normals=None, mode='sfsnet'):
    """
    Adapted from SfSNet/SfSNet_train/python/Shading_Layer.py

    Assumes lights is N x 27 and normals is N x H x W x 3
    """
    if normals is None:
        # render SH on sphere
        normals = get_sphere_normals()
        normals = np.tile(normals, (lights.shape[0],1,1,1))
    
    normals = normalize(normals, axis=3)
    normals = normals.transpose((0,3,1,2))

    shading = np.zeros(normals.shape)

    sz = normals.shape

    att = np.pi*np.array([1, 2.0/3, 0.25])

    c1 = att[0]*(1.0/np.sqrt(4*np.pi))            # 1   * 0.282095 = 0.282095
    c2 = att[1]*(np.sqrt(3.0/(4*np.pi)))          # 2/3 * 0.488602 = 0.325735
    c3 = att[2]*0.5*(np.sqrt(5.0/(4*np.pi)))      # 1/4 * 0.315392 = 0.078848
    c4 = att[2]*(3.0*(np.sqrt(5.0/(12*np.pi))))   # 1/4 * 1.092548 = 0.273137
    c5 = att[2]*(3.0*(np.sqrt(5.0/(48*np.pi))))   # 1/4 * 0.546274 = 0.136568 = c4/2.0

    for i in range(0, sz[0]):
        nx = normals[i,0,...]
        ny = normals[i,1,...]      
        nz = normals[i,2,...]  

        if mode == 'sfsnet':
            # SH representation used by SfSNet
            H1 = c1*np.ones((sz[2],sz[3]))
            H2 = c2*nz
            H3 = c2*nx
            H4 = c2*ny
            H5 = c3*(2*nz*nz - nx*nx -ny*ny)
            H6 = c4*nx*nz
            H7 = c4*ny*nz
            H8 = c5*(nx*nx - ny*ny)
            H9 = c4*nx*ny
        else:
            # SH representation used by LDAN, DirectX SH, Google SH, etc.
            H1 = c1*np.ones((sz[2],sz[3]))
            H2 = -c2*ny
            H3 = c2*nz
            H4 = -c2*nx
            H5 = c4*nx*ny
            H6 = -c4*ny*nz
            H7 = c3*(2*nz*nz - nx*nx -ny*ny) # equivalent to c3*(3*nz*nz - 1)
            H8 = -c4*nx*nz 
            H9 = c5*(nx*nx - ny*ny)

        for j in range(0,3) :
            L=lights[i,j*9:(j+1)*9]
            shading[i,j,:,:]=L[0]*H1+L[1]*H2+L[2]*H3+L[3]*H4+L[4]*H5+L[5]*H6+L[6]*H7+L[7]*H8+L[8]*H9

    shading = shading.transpose((0,2,3,1))
    return shading
