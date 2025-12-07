# Supabase Image Linker UI

This is a Panel application to manage property images in Supabase.

## Setup

1.  **Environment Variables**:
    The `.env` file has been created with placeholders. Please copy the `SUPABASE_URL` and `SUPABASE_KEY` from your `property-map` project's `.env` file into `supabase-img-linker-ui/.env`.
    Ensure `STORAGE_BUCKET` is set correctly (default is `property-images`).

2.  **Install Dependencies**:
    ```bash
    cd supabase-img-linker-ui
    pip install -r requirements.txt
    ```

## Running the App

Run the app using the Panel server:

```bash
panel serve app.py --autoreload --show
```

## Features

-   **View Properties**: Lists all properties from the `properties_CM_pub` table.
-   **Check Images**: Automatically checks if the current `image_url` is valid (Green/Red status).
-   **Filter by Status**: Quickly filter properties by image status (All/OK/Error).
-   **Upload Image**:
    -   Select a property in the table.
    -   Choose "Upload File" to upload a local image.
    -   Choose "Image URL" to download and re-upload an image from a web link.
    -   **Automatic Optimization**: Images are automatically compressed and optimized (typically 50-80% size reduction).
    -   The image is uploaded to Supabase Storage.
    -   A signed URL (valid for 10 years) is generated.
    -   The database is updated with the new URL.

## Image Optimization ⚡

All uploaded images are automatically optimized for faster loading:

- **Smart Resizing**: Large images (>1920px) are resized proportionally
- **Format Conversion**: All images converted to optimized JPEG
- **Quality Optimization**: 85% JPEG quality for optimal balance
- **Size Reduction**: Typically 50-80% smaller file sizes
- **Faster Loading**: 5-8x faster load times for large images

**Example**: A 2MB image becomes ~300KB (85% reduction) 🎉

### Optimizing Existing Images

To optimize images already in Supabase:

```bash
# Preview what would be optimized
python scripts/optimize_existing_images.py --dry-run

# Optimize all images
python scripts/optimize_existing_images.py
```

See [docs/IMAGE_OPTIMIZATION.md](docs/IMAGE_OPTIMIZATION.md) for detailed information.

## Troubleshooting

If you encounter issues with git commits, ensure your working directory is clean or that you have staged changes.
