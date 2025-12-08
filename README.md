# Supabase Image Linker UI

A general-purpose Panel web application for managing images in any Supabase database table. Upload, replace, and manage images for your database records with automatic optimization and validation.

## ✨ Key Features

- 🎯 **Universal & Configurable**: Works with any Supabase table - just configure your column names
- 🖼️ **Image Management**: Upload files or URLs, automatic optimization (50-80% size reduction)
- ✅ **Status Validation**: Automatically checks which records have valid/broken images
- ⚡ **Fast Filtering**: Filter by image status (All/OK/Error) without reloading data
- 🎨 **Modern UI**: Clean, intuitive interface built with Panel
- 🔄 **Auto-Optimization**: Intelligent image compression and resizing
- 🔐 **Secure URLs**: Long-lived signed URLs (10-year expiry by default)

## 📋 Use Cases

This tool can manage images for any type of database records:

- **Properties/Listings**: Real estate, vacation rentals, hotel listings
- **Products**: E-commerce products, catalog items
- **Users/Profiles**: User avatars, profile pictures
- **Content**: Blog posts, articles, portfolio items
- **Inventory**: Equipment, assets, resources
- **And more!**

## 🚀 Quick Start

### 1. Configuration

All customization is done in `constants/config.py`. Here's what you need to configure:

```python
# ==============================================================================
# TABLE CONFIGURATION - CUSTOMIZE FOR YOUR USE CASE
# ==============================================================================

# Table name in Supabase
DATA_TABLE = "properties_CM_pub"

# Column name for the unique identifier (e.g., "id", "user_id", "product_id")
ID_COLUMN = "id"

# Column name for the image URL field (e.g., "image_url", "avatar_url", "photo_url")
IMAGE_URL_COLUMN = "image_url"

# Column name for a descriptive title/name field (e.g., "title", "name", "username")
TITLE_COLUMN = "title"

# Additional columns to display in the info panel (optional)
# Example: ["description", "price", "category"] or ["email", "full_name"]
ADDITIONAL_DISPLAY_COLUMNS = ["listing_url"]

# Label for the entity being managed (e.g., "Property", "User", "Product")
ENTITY_LABEL = "Property"
ENTITY_LABEL_PLURAL = "Properties"
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
STORAGE_BUCKET=your-bucket-name
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
panel serve app.py --autoreload --show
```

The app will open in your browser at `http://localhost:5006`

## 📖 Configuration Examples

### Example 1: E-Commerce Products

```python
DATA_TABLE = "products"
ID_COLUMN = "product_id"
IMAGE_URL_COLUMN = "product_image_url"
TITLE_COLUMN = "product_name"
ADDITIONAL_DISPLAY_COLUMNS = ["category", "price", "sku"]
ENTITY_LABEL = "Product"
ENTITY_LABEL_PLURAL = "Products"
```

### Example 2: User Profiles

```python
DATA_TABLE = "users"
ID_COLUMN = "user_id"
IMAGE_URL_COLUMN = "avatar_url"
TITLE_COLUMN = "username"
ADDITIONAL_DISPLAY_COLUMNS = ["email", "full_name", "created_at"]
ENTITY_LABEL = "User"
ENTITY_LABEL_PLURAL = "Users"
```

### Example 3: Blog Posts

```python
DATA_TABLE = "blog_posts"
ID_COLUMN = "post_id"
IMAGE_URL_COLUMN = "featured_image_url"
TITLE_COLUMN = "post_title"
ADDITIONAL_DISPLAY_COLUMNS = ["author", "published_date", "category"]
ENTITY_LABEL = "Post"
ENTITY_LABEL_PLURAL = "Posts"
```

### Example 4: Real Estate Listings

```python
DATA_TABLE = "properties_CM_pub"
ID_COLUMN = "id"
IMAGE_URL_COLUMN = "image_url"
TITLE_COLUMN = "title"
ADDITIONAL_DISPLAY_COLUMNS = ["listing_url", "price", "location"]
ENTITY_LABEL = "Property"
ENTITY_LABEL_PLURAL = "Properties"
```

## 🎯 How It Works

1. **Load Data**: The app fetches all records from your configured table
2. **Check Images**: Validates all image URLs to identify broken/missing images
3. **View & Filter**: Browse records and filter by image status (All/OK/Error)
4. **Select & Edit**: Click on any record to view details and current image
5. **Upload Images**:
   - **File Upload**: Select a file from your computer
   - **URL Upload**: Paste an image URL to download and re-upload
6. **Auto-Optimization**: Images are automatically compressed and optimized
7. **Update Database**: The record is updated with the new signed URL

## ⚡ Image Optimization

All uploaded images are automatically optimized:

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

## 🛠️ Advanced Configuration

Additional settings in `constants/config.py`:

```python
# Image Optimization
IMAGE_MAX_DIMENSION = 1920  # Max width/height for full images
IMAGE_QUALITY = 85  # JPEG quality (1-95)
THUMBNAIL_MAX_DIMENSION = 400  # Max dimension for thumbnails
THUMBNAIL_QUALITY = 75  # Thumbnail quality
ENABLE_IMAGE_OPTIMIZATION = True  # Enable/disable optimization

# UI Configuration
TABLE_PAGE_SIZE = 20  # Records per page
IMAGE_PREVIEW_WIDTH = 300
IMAGE_PREVIEW_HEIGHT = 200
ACCEPTED_IMAGE_FORMATS = ".jpg,.jpeg,.png,.webp"

# URL Configuration
SIGNED_URL_EXPIRY_YEARS = 10  # URL expiry duration
```

## 📁 Project Structure

```
supabase-img-linker-ui/
├── app.py                      # Main application entry point
├── constants/
│   └── config.py              # 🎯 All configuration settings
├── services/
│   ├── database_service.py    # Supabase database operations
│   ├── data_service.py        # Data management and filtering
│   └── image_service.py       # Image upload and processing
├── ui/
│   ├── components.py          # UI widgets and layouts
│   ├── callbacks.py           # Event handlers
│   └── styles.py              # CSS styling
├── utils/
│   ├── image_validator.py     # Image URL validation
│   ├── image_optimizer.py     # Image optimization
│   └── file_helpers.py        # File utilities
└── docs/                       # Additional documentation
```

## 🔒 Security Notes

- Use Supabase **service role key** for full database access
- The app requires write access to your table and storage bucket
- Signed URLs expire after the configured duration (default: 10 years)
- Keep your `.env` file secure and never commit it to version control

## 📚 Additional Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Image Optimization Guide](docs/IMAGE_OPTIMIZATION.md)
- [Migration Guide](docs/MIGRATION.md)

## 🐛 Troubleshooting

**Images not loading?**
- Check that your storage bucket is configured correctly
- Verify that the image URL column exists in your table
- Ensure Supabase credentials are correct in `.env`

**Optimization not working?**
- Check that `ENABLE_IMAGE_OPTIMIZATION` is set to `True`
- Verify that PIL/Pillow is installed correctly
- Check the console for optimization error messages

**Table not displaying?**
- Verify your column names match exactly (case-sensitive)
- Ensure the configured columns exist in your table
- Check the browser console for JavaScript errors

## 🤝 Contributing

This is a general-purpose tool! Feel free to:
- Report bugs or request features
- Submit pull requests
- Share configuration examples for different use cases
- Improve documentation

## 📄 License

MIT License - feel free to use this tool for any purpose!
