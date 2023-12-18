from colorsys import rgb_to_hls
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from colorpanel import ColorPanel

class ColorController:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.panels = {
            'CMYK': ColorPanel('CMYK', root, self),
            'RGB': ColorPanel('RGB', root, self),
            'HLS': ColorPanel('HLS', root, self)
        }

    def rgb_color(self, rgb):
        # Ensure that 'rgb' is a tuple with three elements.
        if isinstance(rgb, list) and len(rgb) == 3:
            return '#%02x%02x%02x' % tuple(rgb)
        else:
            raise ValueError("RGB color must be a list of three elements.")

    def changeglobalcolor(self, source_format: str, color: list):
        # Update the background only if the source format is 'RGB'.
        if source_format == 'RGB':
            self.root.configure(bg=self.rgb_color(color))
        else:
            self.root.configure(bg=self.rgb_color(self.convertcolor(source_format,'RGB',color)))

        for format, panel in self.panels.items():
            if format != source_format:
                # Ensure that the converted color has the correct number of elements.
                converted_color = self.convertcolor(source_format, format, color)
                if len(converted_color) == len(panel.strings):
                    panel.changecolor(converted_color, global_change=True)
                else:
                    print(f"Converted color does not match the expected number of elements for {format}.")


    def convertcolor(self, source_format: str, target_format: str, color: list) -> list:
        # Basic conversion logic for demonstration purposes.
        if source_format == 'BUTTON':
            source_format = 'RGB'
        if source_format == 'RGB' and target_format == 'CMYK':
            return self.rgb_to_cmyk(color)
        elif source_format == 'CMYK' and target_format == 'RGB':
            return self.cmyk_to_rgb(color)
        elif source_format == 'RGB' and target_format == 'HLS':
            return self.rgb_to_hls(color)  # Not accurate, placeholder for demonstration.
        elif source_format == 'HLS' and target_format == 'RGB':
            return self.hls_to_rgb(color)  # Not accurate, placeholder for demonstration.
        elif source_format == 'HLS' and target_format == 'CMYK':
            return self.hls_to_cmyk(color)  # Not accurate, placeholder for demonstration.
        elif source_format == 'CMYK' and target_format == 'HLS':
            return self.cmyk_to_hls(color)  # Not accurate, placeholder for demonstration.
        return color  # If the conversion is not supported, return the original color.

    def rgb_to_cmyk(self, rgb):
        c = 1 - (rgb[0] / 255)
        m = 1 - (rgb[1] / 255)
        y = 1 - (rgb[2] / 255)
        k = min(c, m, y)
        if k < 1:
            c = (c - k) / (1 - k)
            m = (m - k) / (1 - k)
            y = (y - k) / (1 - k)
        return [c * 100, m * 100, y * 100, k * 100]

    def cmyk_to_rgb(self, cmyk):
        c, m, y, k = [value / 100 for value in cmyk]
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        return [int(r), int(g), int(b)]

    def rgb_to_hls(self, rgb):
        r,g,b = tuple(rgb)
        r /= 255
        g /= 255
        b /= 255
        vmax = max(r, g, b)
        vmin = min(r, g, b)
        h = (vmax + vmin) / 2
        s = (vmax + vmin) / 2
        l = (vmax + vmin) / 2

        if vmax == vmin:
            return (0, 0, l * 100)

        d = vmax - vmin
        if l > 0.5: 
            s = d / (2 - vmax - vmin) 
        else:
            s = d / (vmax + vmin)
        if (vmax == r):
            if g < b:
                h = (g - b) / d + 6
            else:
                h = (g - b) / d + 0
        if (vmax == g):
            h = (b - r) / d + 2
        if (vmax == b):
            h = (r - g) / d + 4
        h /= 6

        return [h * 100, s * 100, l * 100]


    def hls_to_rgb(self, hls):
        h,l,s = tuple(hls)

        h/=100
        l/=100
        s/=100

        r,g,b = 0,0,0

        if s == 0:
            r = g = b = l
        else:
            if l < 0.5:
                q = l * (1 + s)
            else:
                q = l + s - l * s
            p = 2 * l - q
            r = self.hlsToRgb(p, q, h + 1/3)
            g = self.hlsToRgb(p, q, h)
            b = self.hlsToRgb(p, q, h - 1/3)

        return [round(r * 255), round(g * 255), round(b * 255)]
    
    def hlsToRgb(self,p, q, t):
        if (t < 0): t += 1
        if (t > 1): t -= 1
        if (t < 1/6): return p + (q - p) * 6 * t
        if (t < 1/2): return q
        if (t < 2/3): return p + (q - p) * (2/3 - t) * 6
        return p
    
    def hls_to_cmyk(self, hls):
        rgb = self.hls_to_rgb(hls)
        return self.rgb_to_cmyk(rgb)

    def cmyk_to_hls(self, cmyk):
        rgb = self.cmyk_to_rgb(cmyk)
        return self.rgb_to_hls(rgb)
