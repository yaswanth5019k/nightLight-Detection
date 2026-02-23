import cv2
import numpy as np

def apply_gamma_correction(image, gamma=0.5):
    """
    Apply gamma correction to an image to enhance dark regions.
    gamma < 1.0 will make the image brighter.
    """
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def apply_clahe(image):
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE).
    Converts image to LAB color space, applies CLAHE to L-channel, and converts back.
    """
    # Convert from BGR to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Create a CLAHE object
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    
    # Apply CLAHE to L-channel
    cl = clahe.apply(l)
    
    # Merge channels back and convert to BGR
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return enhanced_img

def enhance_low_light_image(image, use_gamma=True, use_clahe=True, gamma_val=0.5):
    """
    Combines gamma correction and CLAHE for low light enhancement.
    """
    enhanced = image.copy()
    
    # Optional basic noise reduction to remove speckles in dark areas
    enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 5, 5, 7, 21)
    
    if use_gamma:
        enhanced = apply_gamma_correction(enhanced, gamma=gamma_val)
        
    if use_clahe:
        enhanced = apply_clahe(enhanced)
        
    return enhanced
