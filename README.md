# EyesOpen: Image Forensic Analysis Tool

## Introduction

EyesOpen is a comprehensive image forensic analysis tool designed for professionals and enthusiasts alike. In today's world where digital tampering is becoming increasingly sophisticated, EyesOpen equips you with the tools needed to uncover traces of manipulation or to identify unique characteristics within digital images.

## Installation

### Pip

1. **Install using pip**

   ```bash
   pip install eyesopen
   ```

2. **Example Usage**

   ```bash
   EyesOpen /path/to/image/
   ```

### From Source

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Sublations/EyesOpen.git
   ```

2. **Navigate to the Directory**

   ```bash
   cd EyesOpen
   ```

3. **Create and Activate a Virtual Environment** (Python 3.x required)

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Basic Usage

The simplest way to use EyesOpen is to run the following command:

```bash
python src/main.py path/to/image
```

This will generate a comprehensive image report saved as `analysis_report.png` in the current directory.

![Analysis Report](https://github.com/sublations/eyesopen/blob/main/analysis_report.png)

## Advanced Usage

EyesOpen offers a multitude of parameters for fine-grained control over each analysis method. Understanding these parameters can help you tailor the tool to your specific needs.

### Examples

1. **Advanced Edge Detection with Custom Canny Thresholds**

   ```bash
   python src/main.py path/to/image --lct 0.5 --uct 1.5
   ```

   Adjusting the Canny thresholds can help you detect faint or sharp edges more effectively.

2. **Custom Gabor Filter Parameters**

   ```bash
   python src/main.py path/to/image --gf 0.8 --gt 0.5 --gb 1.2
   ```

   Customize the Gabor filter to focus on specific frequencies and orientations in the image, aiding in texture discrimination.

3. **Different Wavelet for Frequency Analysis**

   ```bash
   python src/main.py path/to/image --wt db2
   ```

   Changing the wavelet type can highlight different frequency components, possibly revealing hidden tampering.

### Parameters

- `--lct` and `--uct`: These adjust the lower and upper Canny thresholds for Edge Detection. Change these if the default settings either miss edges or detect too many irrelevant edges.

- `--gf`, `--gt`, and `--gb`: These control the frequency, orientation, and bandwidth of the Gabor filter. Adjust these to focus on particular aspects of texture or frequency in the image.

- `--wt`: Controls the type of wavelet used in Frequency Analysis. Different wavelets can highlight different aspects of the image's frequency components.

- `--ela-ql` and `--ela-af`: Control the quality levels and amplification factor for Error Level Analysis (ELA). Different amplification factors and quality levels can make subtle tampering more obvious.

## In-Depth Analysis Methods

- **Error Level Analysis (ELA)**: ELA highlights differences in error levels across the image, which can indicate tampering. Areas of the image that have been altered may show different error levels than the rest of the image.

- **Gabor Filtering**: This method is excellent for revealing hidden textures or patterns in an image. Adjusting parameters like frequency, theta, and bandwidth can help identify specific types of texture manipulation.

- **Frequency Analysis**: This method highlights the frequency components of an image. A sudden noise or inconsistency in these components could indicate that the image has been tampered with.

- **Texture Analysis**: Utilizes Local Binary Pattern (LBP) algorithms to identify inconsistencies in texture. These could occur due to cloning or airbrushing techniques.

- **Advanced Edge Detection**: This focuses on identifying object boundaries. Tampering techniques like object insertion or removal often leave irregular or broken edges, which can be highlighted through this method.

## License

EyesOpen is released under the [GNU GENERAL PUBLIC LICENSE V3](LICENSE)
