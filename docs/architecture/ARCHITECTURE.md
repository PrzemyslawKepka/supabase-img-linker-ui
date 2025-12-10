# Supabase Image Linker UI - Architecture

A modular, general-purpose Panel web application for managing images in any Supabase database table.

## Project Structure

The application follows best practices with clear separation of concerns:

```
supabase-img-linker-ui/
├── app.py                          # Main entry point (orchestration only)
├── constants/                      # Configuration
│   └── config.py                   # 🎯 Centralized configuration (customize here!)
├── services/                       # Business logic layer
│   ├── __init__.py
│   ├── database_service.py        # Database & storage operations
│   ├── data_service.py            # Data management & filtering
│   └── image_service.py           # Image upload & URL management
├── ui/                            # Presentation layer
│   ├── __init__.py
│   ├── components.py              # UI widget definitions
│   ├── styles.py                  # CSS stylesheets
│   └── callbacks.py               # Event handlers
├── utils/                         # Utility functions
│   ├── __init__.py
│   ├── image_validator.py         # Image status checking
│   ├── image_optimizer.py         # Image optimization
│   └── file_helpers.py            # File operations
├── requirements.txt               # Python dependencies
└── README.md                      # Main documentation
```

## Architecture

### Separation of Concerns

1. **Configuration Layer** (`constants/config.py`)
   - **Universal Configuration**: Define your table and column names
   - All configuration constants in one place
   - Environment variable management
   - No hardcoded table/column names in the codebase
   - Easy to adapt to any use case (users, products, properties, etc.)

2. **Services Layer** (`services/`)
   - **DatabaseService**: Handles all Supabase interactions using configured column names
   - **DataService**: Manages application state and data filtering (optimized)
   - **ImageService**: Processes image uploads, optimization, and URL generation

3. **UI Layer** (`ui/`)
   - **UIComponents**: Widget creation and layout with dynamic labels
   - **UICallbacks**: Event handling and business logic integration
   - **Styles**: CSS styling separated from logic

4. **Utils Layer** (`utils/`)
   - Reusable utility functions
   - Image validation with parallel processing
   - Image optimization with PIL/Pillow
   - File helpers for sanitization and content type detection

### Configuration-Driven Design

The application is fully configurable via `constants/config.py`:

```python
# Define your table and columns
DATA_TABLE = "your_table_name"
ID_COLUMN = "your_id_column"
IMAGE_URL_COLUMN = "your_image_column"
TITLE_COLUMN = "your_title_column"
ADDITIONAL_DISPLAY_COLUMNS = ["extra_col1", "extra_col2"]
ENTITY_LABEL = "Your Entity"
ENTITY_LABEL_PLURAL = "Your Entities"
```

**No code changes required** - just update the configuration!

### Key Optimizations

1. **Faster Filtering**: 
   - Status filter no longer reloads data from database
   - Filters are applied to in-memory DataFrame
   - Dramatically reduces response time for filter changes

2. **Parallel Image Checking**:
   - Uses ThreadPoolExecutor for concurrent URL validation
   - Configurable worker count (default: 10)
   - Significantly faster initial load

3. **Automatic Image Optimization**:
   - Smart resizing for large images (>1920px)
   - JPEG conversion with configurable quality
   - Typically 50-80% size reduction
   - Optional thumbnail generation

4. **Modular Architecture**:
   - Easy to test individual components
   - Clear dependencies between modules
   - Simple to extend or modify functionality
   - Fully configurable without code changes

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Environment Variables (`.env`)

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
STORAGE_BUCKET=your-bucket-name
```

### 2. Table Configuration (`constants/config.py`)

Customize for your specific use case:

```python
# Example: E-commerce products
DATA_TABLE = "products"
ID_COLUMN = "product_id"
IMAGE_URL_COLUMN = "product_image_url"
TITLE_COLUMN = "product_name"
ADDITIONAL_DISPLAY_COLUMNS = ["category", "price"]
ENTITY_LABEL = "Product"
ENTITY_LABEL_PLURAL = "Products"
```

## Running the Application

```bash
panel serve app.py --autoreload --show
```

## Features

- ✅ **Universal**: Works with any Supabase table
- ✅ **Configurable**: All settings in one file
- ✅ **View Records**: Display all records with image status
- ✅ **Filter by Status**: Quick filtering (All/OK/Error)
- ✅ **Upload Images**: Via file or URL
- ✅ **Auto-Optimization**: Automatic image compression
- ✅ **Validation**: Real-time image URL checking
- ✅ **Preview**: Live image preview
- ✅ **Responsive UI**: Bootstrap template

## Module Details

### constants/config.py 🎯
**The heart of customization**. All table and column mappings are defined here:
- Table name configuration
- Column name mappings (ID, title, image URL)
- Additional display columns
- Entity labels for UI
- Image optimization settings
- UI preferences

### services/database_service.py
Handles all Supabase operations using configured column names:
- Fetching records from configured table
- Updating configured image URL column
- Uploading to storage
- Generating signed URLs

### services/data_service.py
Manages application data state:
- In-memory data caching
- Optimized filtering (no DB reload)
- Status management
- Dynamic column selection based on config

### services/image_service.py
Processes image operations:
- File uploads with optimization
- URL-based downloads with optimization
- Filename generation using configured columns
- Content type detection
- Image compression and resizing

### ui/components.py
Defines all UI widgets with dynamic configuration:
- Table with configurable columns
- Dynamic column labels from config
- Editor components
- Upload controls
- Layout creation

### ui/callbacks.py
Handles all UI events using configured field names:
- Data loading/refreshing
- Filter changes (optimized)
- Upload processing
- Editor updates with dynamic info display

### ui/styles.py
CSS stylesheets for custom styling:
- Status filter button colors
- Custom component styling

### utils/image_validator.py
Image URL validation:
- Parallel checking for performance
- Timeout handling
- Status determination

### utils/image_optimizer.py
Image optimization:
- Smart resizing
- Format conversion
- Quality optimization
- Size reduction

### utils/file_helpers.py
File operation utilities:
- Generic filename generation (not tied to "properties")
- Extension extraction
- Content type mapping

## Best Practices Implemented

1. **Configuration-Driven**: All customization via config file
2. **Single Responsibility Principle**: Each module has one clear purpose
3. **Dependency Injection**: Services are injected into callbacks
4. **Configuration Management**: All constants in one place
5. **Error Handling**: Proper exception handling throughout
6. **Type Hints**: For better code clarity and IDE support
7. **Documentation**: Comprehensive docstrings
8. **Performance**: Optimized filtering and parallel processing
9. **Universality**: No hardcoded table/column names

## Use Cases

This architecture supports various use cases through configuration:

- **Properties/Listings**: Real estate, vacation rentals
- **Products**: E-commerce catalogs
- **Users**: Profile management, avatars
- **Content**: Blog posts, articles
- **Inventory**: Equipment, assets
- **Portfolio**: Projects, works

Just update `constants/config.py` to adapt to your needs!

## Contributing

When adding new features:
1. Add configuration to `constants/config.py` if needed
2. Implement business logic in appropriate service
3. Use configured column names (don't hardcode)
4. Create UI components in `ui/components.py`
5. Add event handlers in `ui/callbacks.py`
6. Keep `app.py` minimal (orchestration only)

## License

MIT License
