# EyesOpen: Image Forensic Analysis Tool

## Introduction

EyesOpen is an image forensic analysis tool that empowers users to conduct in-depth examinations of digital images. In a world where digital manipulation is becoming increasingly sophisticated, EyesOpen aims to uncover traces of manipulation or identify unique image characteristics.

## Installation

To get started with EyesOpen, follow these installation steps:

1. Clone the EyesOpen repository to your local machine:

   ```bash
   git clone https://github.com/Sublations/EyesOpen.git
   ```

2. Navigate to the EyesOpen directory:

   ```bash
   cd EyesOpen
   ```

3. Create a virtual environment and activate it (ensure you have Python 3.x installed):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To analyze an image using EyesOpen, simply run the following command:

```bash
python main.py path/to/image
```

This will generate an image report saved as `analysis_report.png` in the same directory as your image.

![Sample Image](sample.jpg)
![Sample Image](analysis_report.png)

## Methods of Analysis

EyesOpen offers a variety of advanced analysis methods to thoroughly examine digital images. Here's an overview of these methods:

### Error Level Analysis (ELA)

Error Level Analysis (ELA) is a technique used to reveal areas within an image that have different levels of compression or error rates. This can be a strong indicator of image manipulation. In EyesOpen, ELA is performed by comparing the original image with JPEG-compressed versions at different quality levels and highlighting the differences. Regions with differing brightness levels in the ELA image could signify tampering.

### Gabor Filtering

Gabor filtering is employed to analyze the texture and frequency characteristics of an image. EyesOpen allows you to apply Gabor filtering to an image, highlighting features that may not be immediately visible. Adjust the frequency parameter to reveal different aspects of the image's texture.

### Frequency Analysis

Frequency analysis exposes the inherent frequency components of an image and can unveil hidden details or inconsistencies. EyesOpen applies a 2D Haar wavelet transform to the grayscale image to transition into the frequency domain. The resulting image will highlight frequency components; inconsistencies or noise in these components could be indicative of tampering.

### Texture Analysis

Texture analysis aims to reveal inconsistencies in the texture patterns, which can occur due to cloning or airbrushing. EyesOpen employs the Local Binary Pattern (LBP) algorithm to perform this analysis. In the texture-analyzed image, look for areas where the texture suddenly changes or appears unnatural, as this could indicate tampering.

### Advanced Edge Detection

This method focuses on highlighting the object boundaries within an image. Any tampering with an image, like object insertion or removal, often leaves irregular or broken edges. EyesOpen uses the Canny edge detection algorithm on a blurred grayscale image to highlight these edges. In the resulting image, pay attention to any irregular or fragmented edges as these could be telltale signs of image manipulation.

## License

EyesOpen is released under the [GNU GENERAL PUBLIC LICENSE V3](LICENSE).

---

EyesOpen is developed and maintained by CIG.
