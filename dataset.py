import torch
from torchvision import datasets, transforms


import sys
import time
import random
# import theano
import numpy as np
import traceback
from PIL import Image
from six.moves import queue
from multiprocessing import Process, Event

from lib.imgVoxDataloader import imgVoxDataloader

# from lib.config import cfg
# from lib.data_augmentation import preprocess_img
# from lib.data_io import get_voxel_file, get_rendering_file
from lib.binvox_rw import read_as_3d_array
torch.backends.cudnn.deterministic=True

data_root = './data/'

rendering_root = data_root + 'Rendering'
voxel_root = data_root + 'voxel'

def get_render_file(category, model_id):
    return rendering_root % (category, model_id)

def get_voxel_file(category, model_id):
    return voxel_root % (category, model_id)

base_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
    ])

# load the image transformer
centre_crop = transforms.Compose([
    transforms.RandomResizedCrop(144),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])


def npyLoader(f):
    x = np.load(f)
    return torch.from_numpy(x)

ren_dataset = datasets.ImageFolder(root=rendering_root, transform=base_transform)
vox_dataset = datasets.DatasetFolder(root=voxel_root, transform=None,loader=npyLoader,extensions='npy')


def get_train_data_loaders(idx):
    
    sub_ren_dataset = torch.utils.data.Subset(ren_dataset,idx)
    sub_vox_dataset = torch.utils.data.Subset(vox_dataset,idx)

    render_loader = torch.utils.data.DataLoader(
            sub_ren_dataset, batch_size=len(idx), shuffle=False, num_workers=4, drop_last=True)
    voxel_loader = torch.utils.data.DataLoader(
            sub_vox_dataset, batch_size=len(idx), shuffle=False, num_workers=4, drop_last=True)
    return (render_loader, voxel_loader)
