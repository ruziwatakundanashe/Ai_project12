# Facebook Reel Generator

A simple tool to create engaging Facebook reels with animations, text effects, and transitions.

## Features

- **Image Slideshow**: Create animated slideshows with transition effects
- **Quote with Background**: Generate quote videos with custom backgrounds
- **Text Animation**: Create animated text sequences
- Automatic video sizing for Facebook Reels (1080x1920)
- Built-in transitions and effects
- Easy-to-use interface

## Setup

1. Install Python requirements:
```powershell
python -m pip install -r requirements.txt
```

2. Run the app:
```powershell
streamlit run reel_generator.py
```

## How to Use

1. Choose a template from the sidebar:
   - Image Slideshow
   - Quote with Background
   - Text Animation

2. For Image Slideshow:
   - Upload multiple images
   - Set transition duration
   - Click "Generate Slideshow"

3. For Quote with Background:
   - Enter your quote text
   - Optionally upload a background image
   - Set duration
   - Click "Generate Quote Reel"

4. For Text Animation:
   - Enter text (one line per animation)
   - Set duration per text
   - Click "Generate Animation"

5. Download your generated reel and upload to Facebook!

## Tips for Better Reels

- Use high-quality images (minimum 1080x1920 pixels)
- Keep videos between 15-60 seconds
- Use contrasting colors for text
- Keep text concise and readable
- Test different templates and effects

## Requirements

- Python 3.8 or higher
- Streamlit
- MoviePy
- Pillow
- Internet connection for running the app

## Notes

- Videos are generated in MP4 format
- Temporary files are automatically cleaned up
- All processing is done locally on your machine