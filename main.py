import cv2
import sys
import logging
import argparse
from typing import List, Union
import numpy as np
from termcolor import colored
from image_analysis import (perform_ela, perform_gabor_filtering, perform_advanced_edge_detection,
                            perform_frequency_analysis, perform_texture_analysis)
from utilities import annotate_image, standardize_dimensions, convert_to_color

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_images(image: np.ndarray) -> List[np.ndarray]:
    """
    Process the images using various analysis methods.
    :param image: The input image.
    :return: List of processed images.
    """
    ela_image = perform_ela(image)
    gabor_image = perform_gabor_filtering(image)
    advanced_edge_image = perform_advanced_edge_detection(image)
    frequency_image = perform_frequency_analysis(image)
    texture_image = perform_texture_analysis(image)
    
    return [image, ela_image, gabor_image, advanced_edge_image, frequency_image, texture_image]


def main(image_path: str) -> None:
    """
    Main function to perform image analysis.
    :param image_path: Path to the image to be analyzed.
    """
    try:
        logging.info(colored(f"Reading image from {image_path}", 'blue'))
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError("Image could not be read. Check the file path.")

        if image_path.lower().endswith('.png'):
            temp_path = "temp.jpg"
            cv2.imwrite(temp_path, image, [cv2.IMWRITE_JPEG_QUALITY, 90])
            image = cv2.imread(temp_path)
        
        images = process_images(image)
        
        annotations = [
            "Original: Baseline for comparison.",
            "ELA: Bright areas may suggest tampering.",
            "Gabor: Texture patterns may indicate manipulation.",
            "Edges: Multiple edges can suggest splicing.",
            "Frequency: Inconsistencies may suggest tampering.",
            "Texture: Inconsistencies may suggest editing."
        ]

        color_images = convert_to_color(images)
        standardized_images = standardize_dimensions(color_images)
        
        for i, img in enumerate(standardized_images):
            annotate_image(img, annotations[i], "")
        
        row1 = np.hstack(standardized_images[:3])
        row2 = np.hstack(standardized_images[3:])
        combined_image = np.vstack([row1, row2])
        
        cv2.imwrite('analysis_report.png', combined_image)
        logging.info(colored('Analysis complete. Report saved as analysis_report.png', 'green'))
        
    except ValueError as ve:
        logging.error(colored(f"Value Error: {ve}", 'red'))
    except cv2.error as ce:
        logging.error(colored(f"OpenCV Error: {ce}", 'red'))
    except Exception as e:
        logging.error(colored(f"An unexpected error occurred: {e}", 'red'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EyesOpen: A Digital Forensics Tool')
    parser.add_argument('image_path', type=str, help='Path to the image to be analyzed')
    args = parser.parse_args()
    
    main(args.image_path)
