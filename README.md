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
-   **Upload Image**:
    -   Select a property in the table.
    -   Choose "Upload File" to upload a local image.
    -   Choose "Image URL" to download and re-upload an image from a web link.
    -   The image is uploaded to Supabase Storage.
    -   A signed URL (valid for 10 years) is generated.
    -   The database is updated with the new URL.

## Troubleshooting

If you encounter issues with git commits, ensure your working directory is clean or that you have staged changes.
