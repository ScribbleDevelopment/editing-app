"""
Scribble Studio Ultimate Pro - Backend Pipeline
----------------------------------------------
Provides image preprocessing, advanced background removal hooks,
and batch filter transformations.
"""

import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

class ScribbleProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGBA")

    def adjust_brightness(self, factor: float):
        """Adjusts image brightness (factor: 0.0 to 2.0)."""
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def adjust_contrast(self, factor: float):
        """Adjusts image contrast."""
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def adjust_saturation(self, factor: float):
        """Adjusts color saturation."""
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(factor)
        return self

    def apply_gaussian_blur(self, radius: float):
        """Applies a smooth Gaussian blur filter."""
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
        return self

    def smart_chroma_key(self, tolerance: int = 50):
        """Removes background matching corner pixel colors."""
        data = np.array(self.image)
        r_bg, g_bg, b_bg = data[0, 0][:3]
        
        red, green, blue, alpha = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
        
        distance = np.sqrt((red.astype(float) - r_bg)**2 + 
                           (green.astype(float) - g_bg)**2 + 
                           (blue.astype(float) - b_bg)**2)
        
        mask = distance < tolerance
        data[:, :, 3][mask] = 0
        
        self.image = Image.fromarray(data, "RGBA")
        return self

    def save(self, output_path: str):
        """Saves the processed image to disk."""
        self.image.save(output_path, "PNG")
        print(f"[ScribbleStudio] Successfully saved processed image to {output_path}")

if __name__ == "__main__":
    print("Scribble Studio Python Pipeline Initialized.")