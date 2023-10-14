import cv2
import sys
import logging
import argparse
from typing import List, Union
import numpy as np
from termcolor import colored
from image_analysis import (
    perform_ela,
    perform_gabor_filtering,
    perform_advanced_edge_detection,
    perform_frequency_analysis,
    perform_texture_analysis,
)
from utilities import annotate_image, standardize_dimensions, convert_to_color

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_images(
    image: np.ndarray,
    ela_quality_levels: List[int],
    ela_amplification_factor: int,
    gabor_frequency: float,
    gabor_theta: float,
    gabor_bandwidth: float,
    lower_canny_threshold: float,
    upper_canny_threshold: float,
    lbp_radius: int,
    lbp_n_points: int,
    lbp_method: str,
    wavelet_type: str,
    fourier_weight: float,
) -> List[np.ndarray]:
    """
    Process the images using various analysis methods.
    :param image: The input image.
    :param ela_quality_levels: List of quality levels for ELA.
    :param ela_amplification_factor: Amplification factor for ELA.
    :param gabor_frequency: Frequency for the Gabor filter.
    :param gabor_theta: Orientation for the Gabor filter.
    :param gabor_bandwidth: Bandwidth for the Gabor filter.
    :param lower_canny_threshold: Lower threshold multiplier for Canny edge detection.
    :param upper_canny_threshold: Upper threshold multiplier for Canny edge detection.
    :param lbp_radius: Radius for LBP.
    :param lbp_n_points: Number of points for LBP.
    :param lbp_method: Method for LBP.
    :param wavelet_type: Type of wavelet for frequency analysis.
    :param fourier_weight: Fourier weight for frequency analysis.
    :return: List of processed images.
    """

    ela_image = perform_ela(
        image,
        quality_levels=ela_quality_levels,
        amplification_factor=ela_amplification_factor,
    )

    gabor_image = perform_gabor_filtering(
        image,
        frequency=gabor_frequency,
        theta=gabor_theta,
        bandwidth=gabor_bandwidth,
    )

    advanced_edge_image = perform_advanced_edge_detection(
        image,
        lower_multiplier=lower_canny_threshold,
        upper_multiplier=upper_canny_threshold,
    )

    frequency_image = perform_frequency_analysis(
        image,
        wavelet_type=wavelet_type,
        fourier_weight=fourier_weight,
    )

    texture_image = perform_texture_analysis(
        image,
        radius=lbp_radius,
        n_points=lbp_n_points,
        method=lbp_method,
    )

    return [
        image,
        ela_image,
        gabor_image,
        advanced_edge_image,
        frequency_image,
        texture_image,
    ]


# Main function
def main(image_path: str, args: argparse.Namespace) -> None:
    """
    Main function to perform image analysis.
    :param image_path: Path to the image to be analyzed.
    :param args: Parsed command-line arguments.
    """
    try:
        logging.info(colored(f"Reading image from {image_path}", "blue"))
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Image could not be read. Check the file path.")

        images = process_images(
            image,
            ela_quality_levels=args.ela_ql,
            ela_amplification_factor=args.ela_af,
            gabor_frequency=args.gf,
            gabor_theta=args.gt,
            gabor_bandwidth=args.gb,
            lower_canny_threshold=args.lct,
            upper_canny_threshold=args.uct,
            lbp_radius=args.r,
            lbp_n_points=args.np,
            lbp_method=args.m,
            wavelet_type=args.wt,
            fourier_weight=args.fw,
        )

        # Prepare specifications for each algorithm based on the parameters used.
        specs = [
            "Analysis done with EyesOpen tool on GitHub",  # Original image, no specs needed
            f"Quality Levels - {args.ela_ql}, Amplification Factor - {args.ela_af}",
            f"Frequency - {args.gf}, Theta - {args.gt}, Bandwidth - {args.gb}",
            f"Lower Canny Threshold - {args.lct}, Upper Canny Threshold - {args.uct}",
            f"Wavelet Type - {args.wt}, Fourier Weight - {args.fw}",
            f"LBP Radius - {args.r}, LBP Points - {args.np}, LBP Method - {args.m}",
        ]

        # Annotations with a scientific tone
        annotations = [
            "Original: Baseline for Comparative Analysis",
            "ELA: Deviations in Error Levels for Tamper Detection",
            "Gabor: Frequency-domain Texture Anomalies",
            "Edges: Irregular Boundaries Suggestive of Splicing",
            "Frequency: Spectral Inconsistencies for Forgery Identification",
            "Texture: Local Binary Pattern Discrepancies Indicative of Editing",
        ]

        color_images = convert_to_color(images)
        standardized_images = standardize_dimensions(color_images)

        for i, img in enumerate(standardized_images):
            annotate_image(img, annotations[i], specs[i])

        row1 = np.hstack(standardized_images[:3])
        row2 = np.hstack(standardized_images[3:])
        combined_image = np.vstack([row1, row2])

        cv2.imwrite("analysis_report.png", combined_image)
        logging.info(
            colored("Analysis complete. Report saved as analysis_report.png", "green")
        )

    except ValueError as ve:
        logging.error(colored(f"Value Error: {ve}", "red"))
    except cv2.error as ce:
        logging.error(colored(f"OpenCV Error: {ce}", "red"))
    except Exception as e:
        logging.error(colored(f"An unexpected error occurred: {e}", "red"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        EyesOpen: A Digital Forensics Tool for Image Analysis.
        This tool allows you to run various image forensic algorithms to check for signs of tampering.
        It provides several methods like Error Level Analysis (ELA), Gabor Filtering, Edge Detection,
        Frequency Analysis, and Texture Analysis.
        """
    )
    parser.add_argument(
        "image_path",
        type=str,
        help="Path to the image that you want to analyze. E.g., /path/to/image.jpg",
    )
    parser.add_argument(
        "--lct",
        type=float,
        default=0.7,
        help="""
        Multiplier for the lower Canny threshold for Edge Detection.
        The lower threshold is calculated as (multiplier * median_value_of_image).
        Default is 0.7. E.g., --lct 0.7
        """,
    )
    parser.add_argument(
        "--uct",
        type=float,
        default=1.3,
        help="""
        Multiplier for the upper Canny threshold for Edge Detection.
        The upper threshold is calculated as (multiplier * median_value_of_image).
        Default is 1.3. E.g., --uct 1.3
        """,
    )
    parser.add_argument(
        "--r",
        type=int,
        default=3,
        help="""
        The radius of the circle for Local Binary Pattern (LBP) used in Texture Analysis.
        Default is 3. A higher value increases computation time and detail.
        E.g., --r 3
        """,
    )
    parser.add_argument(
        "--np",
        type=int,
        default=24,
        help="""
        The number of points to sample on the circle for LBP in Texture Analysis.
        Default is 24. Must be an integer that is at least twice the radius.
        E.g., --np 24
        """,
    )
    parser.add_argument(
        "--m",
        type=str,
        default="uniform",
        choices=["uniform", "default", "ror", "var"],
        help="""
        The method to calculate the LBP in Texture Analysis.
        Options are: 'uniform', 'default', 'ror', 'var'.
        Default is 'uniform'. E.g., --m uniform
        """,
    )

    parser.add_argument(
        "--wt",
        type=str,
        default="haar",
        choices=["haar", "db1", "db2", "coif1", "bior1.3"],
        help="""
        The type of wavelet to use for Discrete Wavelet Transform in Frequency Analysis.
        Options are: 'haar', 'db1', 'db2', 'coif1', 'bior1.3'.
        Default is 'haar'. E.g., --wt haar
        """,
    )
    parser.add_argument(
        "--fw",
        type=float,
        default=0.5,
        help="""
        The weight for the Fourier spectrum in Frequency Analysis.
        The final spectrum is a weighted sum of Fourier and Wavelet spectrums.
        Must be a float between 0 and 1. Default is 0.5. E.g., --fw 0.5
        """,
    )
    parser.add_argument(
        "--gf",
        type=float,
        default=0.6,
        help=(
            "The spatial frequency of the sinusoidal factor in the Gabor filter kernel. "
            "This parameter is crucial for texture discrimination. "
            "Values typically range from 0 to 1. Default is 0.6."
        ),
    )
    parser.add_argument(
        "--gt",
        type=float,
        default=0,
        help=(
            "The orientation of the normal to the parallel stripes of the Gabor function, "
            "specified in radians. It defines the angle of the texture that the filter will capture. "
            "Values typically range from 0 to π. Default is 0."
        ),
    )
    parser.add_argument(
        "--gb",
        type=float,
        default=1.0,
        help=(
            "The bandwidth or 'width' of the Gabor function. It controls the spread of the filter "
            "and therefore the texture scale that the filter captures. "
            "Values typically range from 0.5 to 2.5. Default is 1.0."
        ),
    )

    parser.add_argument(
        "--ela-ql",
        type=int,
        nargs="+",
        default=[75, 85, 95],
        help=(
            "List of JPEG quality levels to use for Error Level Analysis. "
            "Each quality level is an integer between 0 and 100. "
            "Default is [75, 85, 95]."
        ),
    )
    parser.add_argument(
        "--ela-af",
        type=int,
        default=20,
        help=(
            "Amplification factor for Error Level Analysis. "
            "This factor is used to exaggerate the differences in error levels. "
            "Default is 20."
        ),
    )

    args = parser.parse_args()
    main(args.image_path, args)
