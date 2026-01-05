import os
from PIL import Image
import torch
from torchvision import transforms

# ImageNet normalization
image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def load_image(image_path):
    img = Image.open(image_path).convert("RGB")
    return image_transform(img)
