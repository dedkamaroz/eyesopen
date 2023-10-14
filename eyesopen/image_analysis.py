import cv2
import numpy as np
import pywt
import logging
from typing import List

from scipy.fftpack import fftshift, fft2
from skimage.feature import local_binary_pattern
from skimage.filters import gabor
from eyesopen.utilities import normalize_gray_image

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def perform_ela(
    image: np.ndarray,
    quality_levels: List[int] = [75, 85, 95],
    amplification_factor: int = 20,
) -> np.ndarray:
    """Perform Error Level Analysis on an image.

    Parameters:
        image (np.ndarray): The input image.
        quality_levels (List[int]): List of JPEG quality levels for ELA.
        amplification_factor (int): Factor by which to amplify the differences.

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

        for quality in quality_levels:
            _, compressed_image = cv2.imencode(
                ".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality]
            )
            compressed_image = cv2.imdecode(compressed_image, 1)
            ela_image = cv2.absdiff(image, compressed_image) * amplification_factor
            ela_images.append(ela_image)

        composite_ela = np.maximum.reduce(ela_images)
        composite_ela = cv2.applyColorMap(composite_ela, cv2.COLORMAP_JET)
        return composite_ela

    except Exception as e:
        logging.error(f"An error occurred in perform_ela: {e}")
        return None


def perform_gabor_filtering(
    image: np.ndarray, frequency: float = 0.6, theta: float = 0, bandwidth: float = 1.0
) -> np.ndarray:
    """Perform Gabor filtering on an image.

    Parameters:
        image (np.ndarray): The input image.
        frequency (float): The frequency of the Gabor filter.
        theta (float): Orientation in radians.
        bandwidth (float): The bandwidth of the Gabor filter.

    Returns:
        np.ndarray: The Gabor-filtered image.
    """
    if image is None:
        logging.warning("Received a NoneType image for Gabor filtering.")
        return None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gabor_real, gabor_imag = gabor(
        gray_image, frequency=frequency, theta=theta, bandwidth=bandwidth
    )

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


def perform_frequency_analysis(
    image: np.ndarray, wavelet_type: str = "haar", fourier_weight: float = 0.5
) -> np.ndarray:
    """
    Perform frequency analysis on an image using Fourier and Wavelet Transforms.

    Parameters:
        image (np.ndarray): The input image.
        wavelet_type (str): The type of wavelet to use for DWT. Default is "haar".
        fourier_weight (float): The weight for Fourier spectrum while combining. Default is 0.5.

    Returns:
        np.ndarray: The frequency-analyzed image.
    """
    try:
        if image is None:
            raise ValueError("Received a NoneType image for frequency analysis.")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        f_transform = fftshift(fft2(gray_image))
        magnitude_spectrum = np.log(np.abs(f_transform))

        coeffs = pywt.dwt2(gray_image, wavelet_type)
        cA, (cH, cV, cD) = coeffs
        wavelet_magnitude = np.sqrt(cH**2 + cV**2)

        wavelet_magnitude_resized = cv2.resize(
            wavelet_magnitude,
            (magnitude_spectrum.shape[1], magnitude_spectrum.shape[0]),
        )
        combined_magnitude = cv2.addWeighted(
            magnitude_spectrum,
            fourier_weight,
            wavelet_magnitude_resized,
            1 - fourier_weight,
            0,
        )
        combined_magnitude = cv2.convertScaleAbs(combined_magnitude)

        return combined_magnitude
    except Exception as e:
        logging.error(f"An error occurred in perform_frequency_analysis: {e}")
        return None


def perform_texture_analysis(
    image: np.ndarray,
    radius: int = 3,
    n_points: int = 24,
    method: str = "uniform",
) -> np.ndarray:
    """Perform texture analysis on an image using Local Binary Pattern.

    Parameters:
        image (np.ndarray): The input image.
        radius (int): The radius of the circle for LBP. Default is 3.
        n_points (int): The number of points to sample on the circle. Default is 24.
        method (str): The method to calculate the LBP. Default is "uniform".

    Returns:
        np.ndarray: The texture-analyzed image.
    """
    try:
        if image is None:
            raise ValueError("Received a NoneType image for texture analysis.")

        if not (0 < radius < 100):
            raise ValueError("Invalid radius value.")

        if not (0 < n_points < 100):
            raise ValueError("Invalid number of points.")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        lbp_image = local_binary_pattern(gray_image, n_points, radius, method=method)
        lbp_image = normalize_gray_image(lbp_image)
        return lbp_image

    except Exception as e:
        logging.error(f"An error occurred in perform_texture_analysis: {e}")
        return None


def perform_advanced_edge_detection(
    image: np.ndarray,
    kernel_size: tuple = (5, 5),
    lower_multiplier: float = 0.7,
    upper_multiplier: float = 1.3,
) -> np.ndarray:
    """Perform advanced edge detection on an image.

    Parameters:
        image (np.ndarray): The input color image.
        kernel_size (tuple): The kernel size for Gaussian blurring. Defaults to (5, 5).
        lower_multiplier (float): Multiplier for the lower Canny threshold. Defaults to 0.7.
        upper_multiplier (float): Multiplier for the upper Canny threshold. Defaults to 1.3.

    Returns:
        np.ndarray: The edge-detected grayscale image, or None if an error occurs.
    """
    try:
        if image is None:
            raise ValueError("Received a NoneType image for edge detection.")
        if not isinstance(image, np.ndarray):
            raise TypeError("Invalid type for image. Expected np.ndarray.")
        if not (0 < lower_multiplier < upper_multiplier < 10):
            raise ValueError("Invalid threshold multipliers.")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, kernel_size, 0)
        median_val = np.median(blurred_image)
        lower = int(max(0, lower_multiplier * median_val))
        upper = int(min(255, upper_multiplier * median_val))
        edge_image = cv2.Canny(blurred_image, lower, upper)

        return edge_image

    except Exception as e:
        logging.error(f"An error occurred in perform_advanced_edge_detection: {e}")
        return None
