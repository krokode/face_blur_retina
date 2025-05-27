after first start
~/.deepface to be created
~/.deepface/weights to be created
retinaface.h5 will be downloaded from the url https://github.com/serengil/deepface_models/releases/download/v1.0/retinaface.h5
Downloading...
From: https://github.com/serengil/deepface_models/releases/download/v1.0/retinaface.h5
~/.deepface/weights/retinaface.h5



Add code bellow to face_coords.py for GPU acceleration (in case of using torch)

import torch
torch.set_default_tensor_type('torch.cuda.FloatTensor')

or

If retinaface-torch is used, add device='cuda' parameter.

