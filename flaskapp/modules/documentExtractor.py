import cv2
import numpy as np
from PIL import Image, ImageOps

# Custom exception for if extractor failed to find the 4 corners of the document
class DocumentCornerExtractionError(Exception):
    pass

# Helper method for retrieving image as numpy array
def get_image_array(path):
    image = Image.open(path)
    image = ImageOps.exif_transpose(image)
    return np.array(image)

# Helper method for calculating euclidean distance between points
def calculate_average_dimensions(corners):
    # Calculate average width and height
    avg_width = int((np.linalg.norm(corners[2] - corners[0]) + np.linalg.norm(corners[3] - corners[1])) / 2)
    avg_height = int((np.linalg.norm(corners[1] - corners[0]) + np.linalg.norm(corners[3] - corners[2])) / 2)
    
    return avg_width, avg_height

# Helper method for calculating destination points
def get_dst_points(top_left_point, width, height):
    new_top_right = top_left_point + np.array([width, 0])
    new_bottom_left = top_left_point + np.array([0, height])
    new_bottom_right = top_left_point + np.array([width, height])

    return np.array([top_left_point, new_bottom_left, new_top_right, new_bottom_right], dtype=np.float32)

# Given a path to an image, this replaces it with extracted version
def extract_document(path):
    # Get image as numpy array
    image = get_image_array(path)

    # Convert to greyscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a guassian blur
    image = cv2.GaussianBlur(image, (7,7), 0)

    # Canny edge detection
    edges = cv2.Canny(image=image, threshold1=70, threshold2=140)

    # Find largest contour from edge map
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea, default=None)

    # Approximate the contour to get a 4 corners
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx_corners = cv2.approxPolyDP(largest_contour, epsilon, True)
    approx_corners = np.squeeze(approx_corners)
    
    # If a contour is found successfully
    if len(approx_corners) == 4:
        # Sort them into top-left, bottom-left, top-right, bottom-right
        approx_corners = sorted(approx_corners, key=lambda corner: corner[0])
        top_corners = sorted(approx_corners[:2], key=lambda corner: corner[1])
        bottom_corners = sorted(approx_corners[2:], key=lambda corner: corner[1])
        approx_corners = np.array((top_corners + bottom_corners), dtype=np.float32)
        
        # Calculate the destination corners
        avg_width, avg_height = calculate_average_dimensions(approx_corners)
        dst_corners = get_dst_points(approx_corners[0], avg_width, avg_height)
        
        # Affine transformations
        perspective_matrix = cv2.getPerspectiveTransform(approx_corners, dst_corners)
        result_image = cv2.warpPerspective(image, perspective_matrix, (image.shape[1], image.shape[0]))
        
        # Crop image
        min_x = int(min(dst_corners[:, 0]))
        max_x = int(max(dst_corners[:, 0]))
        min_y = int(min(dst_corners[:, 1]))
        max_y = int(max(dst_corners[:, 1]))
        
        cropped_image = result_image[min_y:max_y, min_x:max_x]
        
        # Overwrite the original image with the extracted version
        cv2.imwrite(path, cropped_image)

    else:
        raise DocumentCornerExtractionError(f"[Error] Could not get corners from image: {path}")