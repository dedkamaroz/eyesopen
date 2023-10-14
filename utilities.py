import cv2
import numpy as np
import logging
from typing import List, Union

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def annotate_image(image: np.ndarray, text: str, spec: str = "") -> None:
    """
    Annotate an image with text and algorithmic specifications.
    :param image: The image to annotate.
    :param text: The annotation text.
    :param spec: The algorithmic specifications.
    """
    if image is None:
        logging.error("Received a NoneType image for annotation.")
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    h, w = image.shape[:2]
    cv2.rectangle(image, (0, h - 40), (w, h), (0, 0, 0), -1)
    cv2.putText(image, text, (10, h - 20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    if spec:
        cv2.putText(image, spec, (10, h - 5), font, 0.4, (255, 255, 0), 1, cv2.LINE_AA)


def standardize_dimensions(images: List[np.ndarray]) -> List[np.ndarray]:
    """
    Standardize the dimensions of a list of images.
    :param images: The list of images to standardize.
    :return: List of standardized images.
    """
    if not images:
        logging.warning("Received an empty list for standardization.")
        return []

    h, w = images[0].shape[:2]
    return [cv2.resize(img, (w, h)) for img in images]


def convert_to_color(images: List[np.ndarray]) -> List[np.ndarray]:
    """
    Convert grayscale images to color images.
    :param images: The list of images to convert.
    :return: List of color images.
    """
    color_images = []
    for img in images:
        if img is None:
            logging.warning(
                "Encountered a NoneType image during color conversion. Skipping."
            )
            continue

        if len(img.shape) == 2:
            color_images.append(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))
        else:
            color_images.append(img)
    return color_images


def normalize_gray_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize a grayscale image.
    :param image: The grayscale image to normalize.
    :return: Normalized image.
    """
    if image is None:
        logging.warning("Received a NoneType image for normalization.")
        return None

    return cv2.normalize(
        image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U
    )
