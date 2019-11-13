import torch
import os
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable 
from PIL import Image

model = models.resnet18(pretrained=True)

layer = model._modules.get('avgpool')

model.eval()

scaler = transforms.Scale((224, 224))
normalize = transforms.Normalize(mean=transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225]))

to_tensor = transforms.ToTensor()

def get_vector(image_name):
	img = Image.open(image_name)
	t_img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
	my_embedding = torch.zeros(512)
	def copy_data(m, i, o):
		my_embedding.copy_(o.data)
	h = layer.register_forward_hook(copy_data)
	model(t_img)
	h.remove()
	return my_embedding
def main():
	for file in os.listdir('0'):
		print(file)
if __name__ == '__main__':
	main()