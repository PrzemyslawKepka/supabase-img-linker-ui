# Supabase Image Linker UI

A modular Panel web application for managing property images with Supabase integration.

## Project Structure

The application follows best practices with clear separation of concerns:

```
supabase-img-linker-ui/
├── app.py                          # Main entry point (orchestration only)
├── constants/                      # Configuration
│   └── config.py                   # Centralized configuration
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
│   └── file_helpers.py            # File operations
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Architecture

### Separation of Concerns

1. **Configuration Layer** (`constants/config.py`)
   - All configuration constants in one place
   - Environment variable management
   - Easy to modify settings without touching code

2. **Services Layer** (`services/`)
   - **DatabaseService**: Handles all Supabase interactions
   - **DataService**: Manages application state and data filtering (optimized)
   - **ImageService**: Processes image uploads and URL generation

3. **UI Layer** (`ui/`)
   - **UIComponents**: Widget creation and layout
   - **UICallbacks**: Event handling and business logic integration
   - **Styles**: CSS styling separated from logic

4. **Utils Layer** (`utils/`)
   - Reusable utility functions
   - Image validation with parallel processing
   - File helpers for sanitization and content type detection

### Key Optimizations

1. **Faster Filtering**: 
   - Status filter no longer reloads data from database
   - Filters are applied to in-memory DataFrame
   - Dramatically reduces response time for filter changes

2. **Parallel Image Checking**:
   - Uses ThreadPoolExecutor for concurrent URL validation
   - Configurable worker count (default: 10)
   - Significantly faster initial load

3. **Modular Architecture**:
   - Easy to test individual components
   - Clear dependencies between modules
   - Simple to extend or modify functionality

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
STORAGE_BUCKET=property-images
```

## Running the Application

```bash
panel serve app.py
```

Or for development with auto-reload:

```bash
panel serve app.py --autoreload
```

## Features

- ✅ View all properties with image status
- ✅ Filter by status (All/OK/Error)
- ✅ Upload images via file or URL
- ✅ Automatic image validation
- ✅ Real-time preview
- ✅ Responsive UI with Bootstrap template

## Module Details

### constants/config.py
Centralized configuration management. Modify settings here instead of hardcoding values throughout the application.

### services/database_service.py
Handles all Supabase operations:
- Fetching properties
- Updating image URLs
- Uploading to storage
- Generating signed URLs

### services/data_service.py
Manages application data state:
- In-memory data caching
- Optimized filtering (no DB reload)
- Status management

### services/image_service.py
Processes image operations:
- File uploads
- URL-based downloads
- Filename sanitization
- Content type detection

### ui/components.py
Defines all UI widgets:
- Table configuration
- Editor components
- Upload controls
- Layout creation

### ui/callbacks.py
Handles all UI events:
- Data loading/refreshing
- Filter changes (optimized)
- Upload processing
- Editor updates

### ui/styles.py
CSS stylesheets for custom styling:
- Status filter button colors
- Custom component styling

### utils/image_validator.py
Image URL validation:
- Parallel checking for performance
- Timeout handling
- Status determination

### utils/file_helpers.py
File operation utilities:
- Filename sanitization
- Extension extraction
- Content type mapping

## Best Practices Implemented

1. **Single Responsibility Principle**: Each module has one clear purpose
2. **Dependency Injection**: Services are injected into callbacks
3. **Configuration Management**: All constants in one place
4. **Error Handling**: Proper exception handling throughout
5. **Type Hints**: For better code clarity and IDE support
6. **Documentation**: Comprehensive docstrings
7. **Performance**: Optimized filtering and parallel processing

## Migration from Old Structure

The old `db_manager.py` has been superseded by `services/database_service.py` with the same functionality but better organization. The application maintains 100% feature parity with the previous version.

## Contributing

When adding new features:
1. Add configuration to `constants/config.py`
2. Implement business logic in appropriate service
3. Create UI components in `ui/components.py`
4. Add event handlers in `ui/callbacks.py`
5. Keep `app.py` minimal (orchestration only)

## License

[Your License Here]
