import cv2
import os

def display_side_by_side(orig, enhanced, detected, window_name="Low-Light Detection", scale=0.5):
    """
    Displays the original, enhanced, and detected images side-by-side.
    """
    # Resize to have the same height
    h1, w1 = orig.shape[:2]
    h2, w2 = enhanced.shape[:2]
    h3, w3 = detected.shape[:2]
    
    target_h = min(h1, h2, h3)
    
    orig_resized = cv2.resize(orig, (int(w1 * target_h / h1), target_h))
    enhanced_resized = cv2.resize(enhanced, (int(w2 * target_h / h2), target_h))
    detected_resized = cv2.resize(detected, (int(w3 * target_h / h3), target_h))
    
    # Concatenate horizontally
    combined = cv2.hconcat([orig_resized, enhanced_resized, detected_resized])
    
    # Scale down for display to fit on screen
    display_img = cv2.resize(combined, (int(combined.shape[1] * scale), int(combined.shape[0] * scale)))
    
    cv2.imshow(window_name, display_img)
    return combined

def save_output(image, output_path):
    """
    Saves the image to the specified path, creating directories if needed.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)
    print(f"Output saved to {output_path}")
