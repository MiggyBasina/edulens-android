import os
from PIL import Image, ImageDraw

def create_assets():
    """Create required assets for APK build"""
    
    # Create assets directory
    assets_dir = "assets"
    os.makedirs(assets_dir, exist_ok=True)
    
    # Create a simple icon (512x512)
    icon_size = (512, 512)
    icon = Image.new('RGBA', icon_size, (63, 81, 181))  # Indigo color
    draw = ImageDraw.Draw(icon)
    
    # Draw a book/education icon
    # Book body
    draw.rectangle([150, 100, 362, 412], fill=(255, 255, 255, 255))
    # Book spine
    draw.rectangle([362, 100, 412, 412], fill=(49, 27, 146, 255))
    # Pages
    for i in range(5):
        y = 120 + i * 60
        draw.line([160, y, 350, y], fill=(200, 200, 200, 255), width=2)
    
    # Save icon
    icon.save(os.path.join(assets_dir, "icon.png"))
    print(f"✅ Created: {assets_dir}/icon.png")
    
    # Create presplash (loading screen) - 1920x1080
    presplash_size = (1920, 1080)
    presplash = Image.new('RGB', presplash_size, (255, 255, 255))
    draw = ImageDraw.Draw(presplash)
    
    # Add text
    from PIL import ImageFont
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    # Center text
    text = "EduLens"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (presplash_size[0] - text_width) // 2
    y = (presplash_size[1] - text_height) // 2
    
    draw.text((x, y), text, fill=(63, 81, 181), font=font)
    draw.text((x, y + 150), "Educational Analytics", fill=(100, 100, 100), font=ImageFont.load_default().font_variant(size=60))
    
    presplash.save(os.path.join(assets_dir, "presplash.png"))
    print(f"✅ Created: {assets_dir}/presplash.png")
    
    print("\n🎯 Assets created successfully!")
    print("You can replace these with your own designs later.")

if __name__ == "__main__":
    create_assets()
