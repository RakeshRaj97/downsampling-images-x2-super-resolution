import os
import argparse
import cv2

#parse args
parser = argparse.ArgumentParser(description='Downsize images at 2x using bicubic interpolation')
parser.add_argument("hr_img_dir", help="path to high resolution image dir")
parser.add_argument("lr_img_dir", help="path to desired output dir for downsampled images")
parser.add_argument("-k", "--keepdims", help="keep original image dimensions in downsampled images", action="store_true")
args = parser.parse_args(["hr_img_dir","lr_img_dir","-k", "--keepdims"])

hr_image_dir = args.hr_img_dir
lr_image_dir = args.lr_img_dir

#create LR image dirs
os.makedirs(lr_image_dir + "/2x", exist_ok=True)

supported_img_formats = (".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2",
                         ".png", ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tif",
                         ".tiff")
#Downsample HR images
for filename in os.listdir(hr_image_dir):
    if not filename.endswith(supported_img_formats):
        continue

    #Read HR image
    hr_img = cv2.imread(os.path.join(hr_image_dir, filename))
    hr_img_dims = (hr_img.shape[1], hr_img.shape[0])

    #Blur with Gaussian kernel of width sigma = 1
    hr_img = cv2.GaussianBlur(hr_img, (0,0), 1, 1)

    #Downsample image 2x
    lr_image_2x = cv2.resize(hr_img, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    if args.keepdims:
        lr_image_2x = cv2.resize(lr_image_2x, hr_img_dims, interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(os.path.join(lr_image_dir + "/2x", filename), lr_image_2x)