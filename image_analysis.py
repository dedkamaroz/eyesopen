import cv2
import numpy as np
import pywt
import logging
from scipy.fftpack import fftshift, fft2
from skimage.feature import local_binary_pattern
from skimage.filters import gabor
from utilities import normalize_gray_image

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def perform_ela(image: np.ndarray) -> np.ndarray:
    """Perform Error Level Analysis on an image.

    Parameters:
        image (np.ndarray): The input image.

    Returns:
        np.ndarray: The ELA-processed image.
    """
    try:
        if image is None:
            raise ValueError("Received a NoneType image for ELA.")

        if not isinstance(image, np.ndarray):
            raise TypeError("Invalid type for image. Expected np.ndarray.")

        ela_images = []
        original_shape = image.shape

        for quality in [75, 85, 95]:
            _, compressed_image = cv2.imencode(
                ".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality]
            )
            compressed_image = cv2.imdecode(compressed_image, 1)
            ela_image = (
                cv2.absdiff(image, compressed_image) * 20
            )  # Amplification factor
            ela_images.append(ela_image)

        composite_ela = np.maximum.reduce(ela_images)
        composite_ela = cv2.applyColorMap(composite_ela, cv2.COLORMAP_JET)
        return composite_ela

    except Exception as e:
        logging.error(f"An error occurred in perform_ela: {e}")
        return None


def perform_gabor_filtering(image: np.ndarray, frequency=0.6) -> np.ndarray:
    """Perform Gabor filtering on an image.

    Parameters:
        image (np.ndarray): The input image.
        frequency (float): The frequency of the Gabor filter.

    Returns:
        np.ndarray: The Gabor-filtered image.
    """
    if image is None:
        logging.warning("Received a NoneType image for Gabor filtering.")
        return None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gabor_real, gabor_imag = gabor(gray_image, frequency=frequency)

    if gabor_real is None or gabor_imag is None:
        logging.error("Gabor function returned None.")
        return None

    if gabor_real.size == 0 or gabor_imag.size == 0:
        logging.error("Gabor function returned an empty array.")
        return None

    gabor_image = np.sqrt(gabor_real**2 + gabor_imag**2).astype(np.float32)

    min_val, max_val = np.min(gabor_image), np.max(gabor_image)

    if min_val != max_val:
        gabor_image = cv2.normalize(
            gabor_image, None, 255, 0, cv2.NORM_MINMAX, dtype=cv2.CV_8U
        )
    else:
        logging.warning(
            "Gabor image min and max values are the same, skipping normalization."
        )
        return None

    return gabor_image


def perform_frequency_analysis(image: np.ndarray) -> np.ndarray:
    """Perform frequency analysis on an image.

    Parameters:
        image (np.ndarray): The input image.

    Returns:
        np.ndarray: The frequency-analyzed image.
    """
    if image is None:
        logging.warning("Received a NoneType image for frequency analysis.")
        return None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    f_transform = fftshift(fft2(gray_image))
    magnitude_spectrum = np.log(np.abs(f_transform))

    coeffs = pywt.dwt2(gray_image, "haar")
    cA, (cH, cV, cD) = coeffs
    wavelet_magnitude = np.sqrt(cH**2 + cV**2)

    wavelet_magnitude_resized = cv2.resize(
        wavelet_magnitude, (magnitude_spectrum.shape[1], magnitude_spectrum.shape[0])
    )
    combined_magnitude = cv2.addWeighted(
        magnitude_spectrum, 0.5, wavelet_magnitude_resized, 0.5, 0
    )
    combined_magnitude = cv2.convertScaleAbs(combined_magnitude)
    return combined_magnitude


def perform_texture_analysis(image: np.ndarray) -> np.ndarray:
    """Perform texture analysis on an image.

    Parameters:
        image (np.ndarray): The input image.

    Returns:
        np.ndarray: The texture-analyzed image.
    """
    if image is None:
        logging.warning("Received a NoneType image for texture analysis.")
        return None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    radius = 3
    n_points = 8 * radius
    lbp_image = local_binary_pattern(gray_image, n_points, radius, method="uniform")
    lbp_image = normalize_gray_image(lbp_image)
    return lbp_image


def perform_advanced_edge_detection(
    image: np.ndarray, kernel_size=(5, 5)
) -> np.ndarray:
    """Perform advanced edge detection on an image.

    This function applies Gaussian blurring and Canny edge detection.
    The thresholds for Canny are determined dynamically based on the median
    of the pixel values in the grayscale image.

    Parameters:
        image (np.ndarray): The input color image.
        kernel_size (tuple, optional): The kernel size for Gaussian blurring.
                                       Defaults to (5, 5).

    Returns:
        np.ndarray: The edge-detected grayscale image, or None if an error occurs.
    """
    try:
        # Validate input
        if image is None:
            raise ValueError("Received a NoneType image for edge detection.")

        if not isinstance(image, np.ndarray):
            raise TypeError("Invalid type for image. Expected np.ndarray.")

        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred_image = cv2.GaussianBlur(gray_image, kernel_size, 0)

        # Calculate median of the grayscale image
        median_val = np.median(blurred_image)

        # Set lower and upper thresholds for Canny edge detection
        lower = int(max(0, 0.7 * median_val))
        upper = int(min(255, 1.3 * median_val))

        # Perform Canny edge detection
        edge_image = cv2.Canny(blurred_image, lower, upper)

        return edge_image

    except Exception as e:
        logging.error(f"An error occurred in perform_advanced_edge_detection: {e}")
        return None
