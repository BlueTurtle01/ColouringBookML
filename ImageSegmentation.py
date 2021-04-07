import torch
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


class MaskFinder:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = "MultiInputs/" + file_name + ".jpg"

    def load_model(self):
        self.model = torch.hub.load('pytorch/vision:v0.9.0', 'fcn_resnet101', pretrained=True)

    def load_image(self):
        self.input_image = Image.open(self.file_path)
        plt.imshow(self.input_image)
        plt.show()

    def transform_image(self):
        preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        input_tensor = preprocess(self.input_image)
        self.input_batch = input_tensor.unsqueeze(0)

    def make_predictions(self):
        with torch.no_grad():
            output = self.model(self.input_batch)['out'][0]

        self.output_predictions = output.argmax(0)

    def plot_mask(self):
        # create a color palette, selecting a color for each class
        palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
        colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
        colors = (colors % 255).numpy().astype("uint8")

        # plot the semantic segmentation predictions of 21 classes in each color
        r = Image.fromarray(self.output_predictions.byte().cpu().numpy()).resize(self.input_image.size)
        r.putpalette(colors)

        plt.imshow(r)
        plt.show()


FCNResnet = MaskFinder(file_name="family")
FCNResnet.load_model()
FCNResnet.load_image()
FCNResnet.transform_image()
FCNResnet.make_predictions()
FCNResnet.plot_mask()


# model = torch.hub.load('pytorch/vision:v0.9.0', 'deeplabv3_resnet101', pretrained=True)
