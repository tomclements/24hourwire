#!/usr/bin/env python3
"""
Generate Open Graph image for 24HourWire social sharing.
Run this script on your server to create the og-image.jpg file.

Requirements: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_og_image():
    # OG image dimensions (optimal for Facebook/Twitter)
    width = 1200
    height = 630
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='#0A2540')
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect
    for y in range(height):
        # Gradient from dark blue to slightly lighter blue
        r = int(10 + (y / height) * 15)
        g = int(37 + (y / height) * 30)
        b = int(64 + (y / height) * 40)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Try to load fonts (fallback to default if not available)
    try:
        # Try system fonts
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        tagline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        try:
            # Try common macOS fonts
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            tagline_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        except:
            # Fallback to default
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            tagline_font = ImageFont.load_default()
    
    # Draw logo icon (simplified wire/network icon)
    center_x = width // 2
    icon_y = 150
    
    # Draw connecting nodes (representing the wire/network)
    node_color = '#0066cc'
    line_color = '#1E3A5F'
    
    # Central node
    draw.ellipse([center_x-20, icon_y-20, center_x+20, icon_y+20], fill=node_color)
    
    # Surrounding nodes
    positions = [
        (center_x-80, icon_y-40),
        (center_x+80, icon_y-40),
        (center_x-60, icon_y+50),
        (center_x+60, icon_y+50),
        (center_x, icon_y-80),
    ]
    
    for pos in positions:
        draw.line([center_x, icon_y, pos[0], pos[1]], fill=line_color, width=3)
        draw.ellipse([pos[0]-12, pos[1]-12, pos[0]+12, pos[1]+12], fill=node_color)
    
    # Title
    title = "24HourWire"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 320), title, font=title_font, fill='#FFFFFF')
    
    # Subtitle
    subtitle = "The Latest News from All Angles"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 410), subtitle, font=subtitle_font, fill='#CBD5E1')
    
    # Tagline
    tagline = "Unbiased. Multi-perspective. Always current."
    bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = bbox[2] - bbox[0]
    tagline_x = (width - tagline_width) // 2
    draw.text((tagline_x, 480), tagline, font=tagline_font, fill='#718096')
    
    # Save the image
    output_path = 'news/static/news/images/og-image.jpg'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save with high quality
    img.save(output_path, 'JPEG', quality=95, optimize=True)
    print(f"OG image created: {output_path}")
    print(f"Dimensions: {width}x{height}")
    
    return output_path

if __name__ == '__main__':
    create_og_image()
