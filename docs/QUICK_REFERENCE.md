# Quick Reference Guide

## Running the Application

```bash
# Standard
panel serve app.py

# With auto-reload (development)
panel serve app.py --autoreload

# Custom port
panel serve app.py --port 5006

# Show in browser
panel serve app.py --show
```

## Project Structure at a Glance

```
📦 supabase-img-linker-ui
├── 📄 app.py                    ← Start here: Main entry point
│
├── 📁 constants/                ← Configuration
│   └── config.py                → 🎯 CUSTOMIZE HERE: Table & columns
│
├── 📁 services/                 ← Business Logic
│   ├── database_service.py      → Supabase operations
│   ├── data_service.py          → Data management + filtering
│   └── image_service.py         → Image uploads & optimization
│
├── 📁 ui/                       ← User Interface
│   ├── components.py            → Widget definitions
│   ├── callbacks.py             → Event handlers
│   └── styles.py                → CSS styling
│
└── 📁 utils/                    ← Utilities
    ├── image_validator.py       → Check image URLs
    ├── image_optimizer.py       → Image optimization
    └── file_helpers.py          → File operations
```

## Making It Work With Your Table 🎯

**All configuration is in `constants/config.py`** - just update these settings:

```python
# Your table and columns
DATA_TABLE = "your_table_name"
ID_COLUMN = "your_id_column"           # e.g., "id", "user_id", "product_id"
IMAGE_URL_COLUMN = "your_image_column" # e.g., "image_url", "avatar_url"
TITLE_COLUMN = "your_title_column"     # e.g., "title", "name", "username"
ADDITIONAL_DISPLAY_COLUMNS = ["col1"]  # Optional extra columns to show
ENTITY_LABEL = "Your Entity"           # e.g., "User", "Product", "Property"
ENTITY_LABEL_PLURAL = "Your Entities"  # e.g., "Users", "Products"
```

**That's it!** No code changes needed.

## Common Configuration Examples

### E-Commerce Products
```python
DATA_TABLE = "products"
ID_COLUMN = "product_id"
IMAGE_URL_COLUMN = "product_image_url"
TITLE_COLUMN = "product_name"
ADDITIONAL_DISPLAY_COLUMNS = ["category", "price", "sku"]
ENTITY_LABEL = "Product"
ENTITY_LABEL_PLURAL = "Products"
```

### User Profiles
```python
DATA_TABLE = "users"
ID_COLUMN = "user_id"
IMAGE_URL_COLUMN = "avatar_url"
TITLE_COLUMN = "username"
ADDITIONAL_DISPLAY_COLUMNS = ["email", "full_name"]
ENTITY_LABEL = "User"
ENTITY_LABEL_PLURAL = "Users"
```

### Blog Posts
```python
DATA_TABLE = "blog_posts"
ID_COLUMN = "post_id"
IMAGE_URL_COLUMN = "featured_image_url"
TITLE_COLUMN = "post_title"
ADDITIONAL_DISPLAY_COLUMNS = ["author", "published_date"]
ENTITY_LABEL = "Post"
ENTITY_LABEL_PLURAL = "Posts"
```

## Common Tasks

### 1. Change Your Table/Columns
**File**: `constants/config.py`
```python
# Update these variables (see examples above)
DATA_TABLE = "your_table"
ID_COLUMN = "your_id"
IMAGE_URL_COLUMN = "your_image_field"
TITLE_COLUMN = "your_title_field"
```

### 2. Adjust Page Size
**File**: `constants/config.py`
```python
TABLE_PAGE_SIZE = 20  # Change this number
```

### 3. Configure Image Optimization
**File**: `constants/config.py`
```python
ENABLE_IMAGE_OPTIMIZATION = True  # Enable/disable
IMAGE_MAX_DIMENSION = 1920  # Max width/height
IMAGE_QUALITY = 85  # JPEG quality (1-95)
```

### 4. Adjust Image Check Timeout
**File**: `constants/config.py`
```python
IMAGE_CHECK_TIMEOUT = 3  # Seconds
IMAGE_CHECK_MAX_WORKERS = 10  # Parallel workers
```

### 5. Change Header Color
**File**: `constants/config.py`
```python
HEADER_BACKGROUND_COLOR = "#3A7D7E"  # Your color
```

### 6. Add More Display Columns
**File**: `constants/config.py`
```python
ADDITIONAL_DISPLAY_COLUMNS = ["column1", "column2", "column3"]
```

## Module Import Guide

### Using Database Service
```python
from services.database_service import DatabaseService

db = DatabaseService()
df = db.fetch_records()  # Uses configured table
db.update_image_url(record_id, url)  # Uses configured column
```

### Using Data Service
```python
from services.data_service import DataService

data = DataService(db_service)
data.load_data()
filtered = data.get_filtered_data("OK")
```

### Using Image Service
```python
from services.image_service import ImageService

img_svc = ImageService(db_service)
url = img_svc.process_file_upload(id, title, file_data, filename)
```

### Using Utilities
```python
from utils.image_validator import check_images_parallel
from utils.image_optimizer import ImageOptimizer
from utils.file_helpers import sanitize_filename

statuses = check_images_parallel(url_list)
optimizer = ImageOptimizer()
safe_name = sanitize_filename("My File #123!")
```

## Debugging

### Check imports
```bash
python -c "import app"
```

### Check specific module
```bash
python -c "from services.data_service import DataService; print('OK')"
```

### View Panel logs
```bash
panel serve app.py --log-level debug
```

## Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| **Table Configuration** | | |
| `DATA_TABLE` | `properties_CM_pub` | Database table name |
| `ID_COLUMN` | `id` | Unique identifier column |
| `IMAGE_URL_COLUMN` | `image_url` | Image URL column |
| `TITLE_COLUMN` | `title` | Title/name column |
| `ADDITIONAL_DISPLAY_COLUMNS` | `["listing_url"]` | Extra columns to show |
| `ENTITY_LABEL` | `Property` | Singular label |
| `ENTITY_LABEL_PLURAL` | `Properties` | Plural label |
| **Environment Variables** | | |
| `SUPABASE_URL` | (env) | Supabase project URL |
| `SUPABASE_KEY` | (env) | Supabase API key |
| `STORAGE_BUCKET` | `property-images` | Storage bucket name |
| **UI Configuration** | | |
| `TABLE_PAGE_SIZE` | `20` | Rows per page |
| `IMAGE_PREVIEW_WIDTH` | `300` | Preview width (px) |
| `IMAGE_PREVIEW_HEIGHT` | `200` | Preview height (px) |
| **Image Optimization** | | |
| `ENABLE_IMAGE_OPTIMIZATION` | `True` | Enable optimization |
| `IMAGE_MAX_DIMENSION` | `1920` | Max dimension (px) |
| `IMAGE_QUALITY` | `85` | JPEG quality (1-95) |
| **Performance** | | |
| `IMAGE_CHECK_TIMEOUT` | `3` | URL check timeout (sec) |
| `IMAGE_CHECK_MAX_WORKERS` | `10` | Parallel workers |
| `SIGNED_URL_EXPIRY_YEARS` | `10` | URL expiry time |
| **Styling** | | |
| `HEADER_BACKGROUND_COLOR` | `#3A7D7E` | Header color |

## Performance Tips

1. **Slow initial load?**
   - Reduce `IMAGE_CHECK_MAX_WORKERS` if hitting rate limits
   - Increase for faster checking (if API allows)

2. **Slow filtering?**
   - Should be instant with new architecture
   - If not, check that `filter_data()` is bound to filter changes

3. **Memory issues?**
   - Reduce `TABLE_PAGE_SIZE`
   - Implement pagination in data service

4. **Large images?**
   - Enable `ENABLE_IMAGE_OPTIMIZATION = True`
   - Adjust `IMAGE_MAX_DIMENSION` and `IMAGE_QUALITY`

## Troubleshooting

### "No module named 'dotenv'"
```bash
pip install -r requirements.txt
```

### "Supabase credentials not found"
Create `.env` file with:
```
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
STORAGE_BUCKET=your_bucket
```

### "Failed to load data"
- Check Supabase credentials
- Verify table name in `constants/config.py`
- Ensure configured columns exist in your table
- Check network connection

### "Column not found" error
- Verify column names in `constants/config.py` match exactly (case-sensitive)
- Check that `ID_COLUMN`, `IMAGE_URL_COLUMN`, `TITLE_COLUMN` exist in your table
- Run `SELECT * FROM your_table LIMIT 1` to see available columns

### Filter not working
- Verify `filter_data()` is bound in `callbacks.py`
- Check console for errors
- Try refresh button

### Upload failing
- Check storage bucket permissions
- Verify bucket name in `.env`
- Check file size limits
- Ensure image optimization dependencies are installed

### Images not optimizing
- Verify `ENABLE_IMAGE_OPTIMIZATION = True`
- Check that PIL/Pillow is installed: `pip install Pillow`
- Check console for optimization errors

## Getting Help

1. Check `README.md` for comprehensive configuration examples
2. Check `ARCHITECTURE.md` for detailed module documentation
3. Review inline documentation in each module
4. See configuration examples in README for different use cases

## Key Benefits Recap

✅ **Universal** - Works with any Supabase table  
✅ **Configurable** - All settings in one file  
✅ **Fast filtering** - No database reload on filter changes  
✅ **Auto-optimization** - 50-80% image size reduction  
✅ **Modular design** - Easy to maintain and extend  
✅ **No hardcoding** - Everything driven by configuration  

---

*Last updated: December 2025*
