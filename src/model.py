import torch
import torch.nn as nn
from torchvision import models

def get_resnet18_feature_extractor():
    model = models.resnet18(pretrained=True)

    # Remove final classification layer
    model = nn.Sequential(*list(model.children())[:-1])

    for param in model.parameters():
        param.requires_grad = False  # freeze weights

    model.eval()
    return model
