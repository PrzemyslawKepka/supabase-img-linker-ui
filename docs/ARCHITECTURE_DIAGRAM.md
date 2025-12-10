# Project Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                      (Panel Web Interface)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                          app.py                                  │
│                   (Orchestration Layer)                          │
│  • Initialize Panel                                              │
│  • Create services                                               │
│  • Create UI components                                          │
│  • Wire callbacks                                                │
│  • Start application                                             │
└───────┬─────────────────┬─────────────────┬──────────────────────┘
        │                 │                 │
        │                 │                 │
    ┌───▼────────┐     ┌──────▼──────┐    ┌────▼─────┐
    │ Constants  │     │   Services   │    │    UI    │
    └────────────┘     └──────┬──────┘    └────┬─────┘
                          │                │
                          │                │
        ┌─────────────────┼────────────────┼──────────────────┐
        │                 │                │                  │
   ┌────▼──────┐    ┌─────▼────┐    ┌────▼────┐    ┌────────▼──────┐
   │ Database  │    │   Data   │    │  Image  │    │  Components   │
   │  Service  │    │ Service  │    │ Service │    │  & Callbacks  │
   └─────┬─────┘    └─────┬────┘    └────┬────┘    └───────┬───────┘
         │                │              │                  │
         │                │              │                  │
         └────────────────┼──────────────┼──────────────────┘
                          │              │
                     ┌────▼──────┐  ┌────▼────┐
                     │   Utils   │  │ Styles  │
                     │  Package  │  │         │
                     └───────────┘  └─────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
    ┌─────▼──────┐  ┌─────▼──────┐  ┌────▼────┐
    │   Image    │  │    File    │  │ Helpers │
    │ Validator  │  │  Helpers   │  │         │
    └────────────┘  └────────────┘  └─────────┘
```

## Module Dependency Graph

```
app.py
│
├─→ constants/
│   └─→ config.py (no dependencies)
│
├─→ services/
│   │
│   ├─→ database_service.py
│   │   └─→ constants/config.py
│   │
│   ├─→ data_service.py
│   │   ├─→ database_service.py
│   │   ├─→ utils/image_validator.py
│   │   └─→ constants/config.py
│   │
│   └─→ image_service.py
│       ├─→ database_service.py
│       ├─→ utils/file_helpers.py
│       └─→ constants/config.py
│
├─→ ui/
│   │
│   ├─→ components.py
│   │   ├─→ constants/config.py
│   │   └─→ styles.py
│   │
│   └─→ callbacks.py
│       ├─→ ui/components.py
│       ├─→ services/data_service.py
│       └─→ services/image_service.py
│
└─→ utils/
    │
    ├─→ image_validator.py
    │   └─→ constants/config.py
    │
    └─→ file_helpers.py (no dependencies)
```

## Data Flow Diagram

### Initial Load Flow
```
User Opens App
      │
      ▼
   app.py
      │
      ├─→ Initialize services
      │   ├─→ DatabaseService (connects to Supabase)
      │   ├─→ DataService (creates state)
      │   └─→ ImageService (ready for uploads)
      │
      ├─→ Create UI
      │   ├─→ UIComponents (widgets)
      │   └─→ UICallbacks (event handlers)
      │
      └─→ onload: load_and_display_data()
            │
            ├─→ DataService.load_data()
            │   ├─→ DatabaseService.fetch_properties()
            │   │   └─→ Supabase Query
            │   │
            │   └─→ check_images_parallel()
            │       └─→ Concurrent URL checks
            │
            └─→ Update table with data
```

### Filter Change Flow (OPTIMIZED)
```
User Changes Filter
      │
      ▼
UICallbacks.filter_data()  ⚡ Fast path
      │
      ├─→ DataService.get_filtered_data()
      │   └─→ Filter in-memory DataFrame
      │       (No database call!)
      │       (No URL checks!)
      │
      └─→ Update table with filtered data
```

### Upload Flow
```
User Uploads Image
      │
      ▼
UICallbacks.handle_upload()
      │
      ├─→ Validate inputs
      │
      ├─→ ImageService.process_file_upload() or process_url_upload()
      │   │
      │   ├─→ Sanitize filename (utils/file_helpers)
      │   │
      │   ├─→ DatabaseService.upload_image()
      │   │   └─→ Supabase Storage
      │   │
      │   ├─→ DatabaseService.get_signed_url()
      │   │   └─→ Supabase Storage
      │   │
      │   └─→ DatabaseService.update_image_url()
      │       └─→ Supabase Database
      │
      └─→ Refresh data and update UI
```

## Layer Architecture

```
┌──────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                        │
│  ┌────────────────┐  ┌──────────────────────────────┐   │
│  │ ui/components  │  │    ui/callbacks              │   │
│  │                │  │                              │   │
│  │ • Widgets      │  │ • Event handlers             │   │
│  │ • Layouts      │  │ • User interactions          │   │
│  │ • Styling      │  │ • UI state management        │   │
│  └────────────────┘  └──────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Data      │  │   Image     │  │  Database   │     │
│  │  Service    │  │  Service    │  │  Service    │     │
│  │             │  │             │  │             │     │
│  │ • State     │  │ • Uploads   │  │ • Queries   │     │
│  │ • Filtering │  │ • URLs      │  │ • Updates   │     │
│  │ • Transform │  │ • Process   │  │ • Storage   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                     UTILITY LAYER                         │
│  ┌──────────────┐  ┌──────────────────────────────┐     │
│  │    Image     │  │       File Helpers           │     │
│  │  Validator   │  │                              │     │
│  │              │  │ • Sanitization               │     │
│  │ • URL check  │  │ • Extension handling         │     │
│  │ • Parallel   │  │ • Content type detection     │     │
│  └──────────────┘  └──────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                 CONFIGURATION LAYER                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │          constants/config.py                      │   │
│  │                                                   │   │
│  │ • Environment variables                           │   │
│  │ • Application constants                           │   │
│  │ • Performance settings                            │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Supabase   │  │   Supabase   │  │   External   │  │
│  │   Database   │  │   Storage    │  │   Image URLs │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Component Interaction Sequence

### Scenario: User Filters by "OK" Status

```sequence
User                UI Components         Callbacks           Data Service      Table Widget
 │                      │                    │                    │                  │
 │  Click "OK"         │                    │                    │                  │
 ├─────────────────────>│                    │                    │                  │
 │                      │                    │                    │                  │
 │                      │  filter_data()     │                    │                  │
 │                      ├───────────────────>│                    │                  │
 │                      │                    │                    │                  │
 │                      │                    │ get_filtered_data("OK")              │
 │                      │                    ├───────────────────>│                  │
 │                      │                    │                    │                  │
 │                      │                    │                    │ Filter DataFrame │
 │                      │                    │                    │ (in memory)      │
 │                      │                    │                    │<─────────────────│
 │                      │                    │                    │                  │
 │                      │                    │  filtered_df       │                  │
 │                      │                    │<───────────────────┤                  │
 │                      │                    │                    │                  │
 │                      │                    │ get_display_columns()                 │
 │                      │                    ├───────────────────>│                  │
 │                      │                    │  display_df        │                  │
 │                      │                    │<───────────────────┤                  │
 │                      │                    │                    │                  │
 │                      │  update value      │                    │                  │
 │                      │<───────────────────┤                    │                  │
 │                      │                    │                    │                  │
 │                      │                              Update data                   │
 │                      ├───────────────────────────────────────────────────────────>│
 │                      │                    │                    │                  │
 │  Updated table       │                    │                    │                  │
 │<─────────────────────┤                    │                    │                  │
 │                      │                    │                    │                  │

Total Time: ~50ms ⚡
(No database queries, no network calls)
```

### Scenario: User Clicks Refresh Button

```sequence
User                Callbacks          Data Service      Database Service    Supabase
 │                      │                    │                    │              │
 │  Click Refresh      │                    │                    │              │
 ├─────────────────────>│                    │                    │              │
 │                      │                    │                    │              │
 │                      │  load_data()       │                    │              │
 │                      ├───────────────────>│                    │              │
 │                      │                    │                    │              │
 │                      │                    │ fetch_properties() │              │
 │                      │                    ├───────────────────>│              │
 │                      │                    │                    │              │
 │                      │                    │                    │   Query DB   │
 │                      │                    │                    ├─────────────>│
 │                      │                    │                    │              │
 │                      │                    │                    │   data       │
 │                      │                    │                    │<─────────────┤
 │                      │                    │       data         │              │
 │                      │                    │<───────────────────┤              │
 │                      │                    │                    │              │
 │                      │                    │  (check URLs in parallel)         │
 │                      │                    │                    │              │
 │                      │        data        │                    │              │
 │                      │<───────────────────┤                    │              │
 │                      │                    │                    │              │
 │  Updated table       │                    │                    │              │
 │<─────────────────────┤                    │                    │              │
 │                      │                    │                    │              │

Total Time: ~2000ms
(Full database refresh when explicitly requested)
```

## File Size Distribution

```
UI Layer (40%)
├── callbacks.py    ████████████████████  220 lines
└── components.py   ███████████████       150 lines

Services Layer (31%)
├── image_service.py  █████████████       130 lines
├── data_service.py   ██████████          95 lines
└── database_service.py ████████          80 lines

Utils Layer (11%)
├── file_helpers.py     ██████            65 lines
└── image_validator.py  █████             45 lines

Other (18%)
├── app.py                  ███████       67 lines
├── constants/config.py     █████         50 lines
└── styles.py               ███           25 lines
```

## Key Design Patterns Used

1. **Dependency Injection**: Services injected into callbacks
2. **Single Responsibility**: Each class/module has one clear purpose
3. **Strategy Pattern**: Different upload strategies (file vs URL)
4. **Observer Pattern**: Panel's watch mechanism for reactive updates
5. **Factory Pattern**: Component creation methods
6. **Facade Pattern**: Services provide simple interface to complex operations
7. **Repository Pattern**: DatabaseService abstracts data access

---

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Easy testability
- ✅ Maintainable codebase
- ✅ Scalable design
- ✅ Performance optimizations
- ✅ Professional structure
