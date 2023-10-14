import cv2
import sys
import logging
import argparse
import click
from typing import List, Union
import numpy as np
from termcolor import colored
from eyesopen.image_analysis import (
    perform_ela,
    perform_gabor_filtering,
    perform_advanced_edge_detection,
    perform_frequency_analysis,
    perform_texture_analysis,
)
from eyesopen.utilities import annotate_image, standardize_dimensions, convert_to_color

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


# Define the main function as a Click command
@click.command()
@click.argument("image_path", type=click.Path(exists=True), required=True)
@click.option(
    "--lct",
    default=0.7,
    help="Multiplier for the lower Canny threshold for Edge Detection.",
)
@click.option(
    "--uct",
    default=1.3,
    help="Multiplier for the upper Canny threshold for Edge Detection.",
)
@click.option(
    "--r",
    default=3,
    help="The radius of the circle for Local Binary Pattern (LBP) used in Texture Analysis.",
)
@click.option(
    "--np",
    "n_points",
    default=24,
    help="The number of points to sample on the circle for LBP in Texture Analysis.",
)
@click.option(
    "--m",
    default="uniform",
    type=click.Choice(["uniform", "default", "ror", "var"]),
    help="The method to calculate the LBP in Texture Analysis.",
)
@click.option(
    "--wt",
    default="haar",
    type=click.Choice(["haar", "db1", "db2", "coif1", "bior1.3"]),
    help="The type of wavelet to use for Discrete Wavelet Transform in Frequency Analysis.",
)
@click.option(
    "--fw",
    default=0.5,
    help="The weight for the Fourier spectrum in Frequency Analysis.",
)
@click.option(
    "--gf",
    default=0.6,
    help="The spatial frequency of the sinusoidal factor in the Gabor filter kernel.",
)
@click.option(
    "--gt",
    default=0,
    help="The orientation of the normal to the parallel stripes of the Gabor function.",
)
@click.option(
    "--gb", default=1.0, help='The bandwidth or "width" of the Gabor function.'
)
@click.option(
    "--ela-ql",
    default=[75, 85, 95],
    multiple=True,
    type=int,
    help="List of JPEG quality levels to use for Error Level Analysis.",
)
@click.option(
    "--ela-af", default=20, help="Amplification factor for Error Level Analysis."
)
def main(image_path, lct, uct, r, n_points, m, wt, fw, gf, gt, gb, ela_ql, ela_af):
    """
    EyesOpen: Digital Image Forensic Analysis Tool

    Usage:
        eyesopen [OPTIONS] IMAGE_PATH

    Description:
        Conducts multiple forms of image analysis including Error Level Analysis (ELA), Gabor Filtering, Edge Detection, Frequency Analysis, and Texture Analysis.

    Required Arguments:
        IMAGE_PATH          The path to the image to be analyzed.

    Optional Arguments:
        --lct FLOAT         Lower Canny threshold for Edge Detection. Default: 0.7
        --uct FLOAT         Upper Canny threshold for Edge Detection. Default: 1.3
        --gf FLOAT          Frequency for Gabor Filtering. Default: 0.6
        --gt FLOAT          Orientation for Gabor Filtering. Default: 0
        --gb FLOAT          Bandwidth for Gabor Filtering. Default: 1.0
        --ela-ql INT...     JPEG quality levels for ELA. Default: [75, 85, 95]
        --ela-af INT        Amplification factor for ELA. Default: 20

    Examples:
        Basic Usage:        eyesopen /path/to/image.jpg
        Advanced Usage:     eyesopen /path/to/image.jpg --lct 0.5 --uct 1.5 --gf 0.8

    For more details, refer to the README.
    """
    try:
        logging.info(colored(f"Reading image from {image_path}", "blue"))
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Image could not be read. Check the file path.")

        images = process_images(
            image,
            ela_quality_levels=ela_ql,
            ela_amplification_factor=ela_af,
            gabor_frequency=gf,
            gabor_theta=gt,
            gabor_bandwidth=gb,
            lower_canny_threshold=lct,
            upper_canny_threshold=uct,
            lbp_radius=r,
            lbp_n_points=n_points,
            lbp_method=m,
            wavelet_type=wt,
            fourier_weight=fw,
        )

        # Prepare specifications for each algorithm based on the parameters used.
        specs = [
            "Analysis done with EyesOpen tool on GitHub",  # Original image, no specs needed
            f"Quality Levels - {ela_ql}, Amplification Factor - {ela_af}",
            f"Frequency - {gf}, Theta - {gt}, Bandwidth - {gb}",
            f"Lower Canny Threshold - {lct}, Upper Canny Threshold - {uct}",
            f"Wavelet Type - {wt}, Fourier Weight - {fw}",
            f"LBP Radius - {r}, LBP Points - {np}, LBP Method - {m}",
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
    if len(sys.argv) == 1:
        with click.Context(main) as ctx:
            click.echo(main.get_help(ctx))
    else:
        main()
