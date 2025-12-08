"""
Configuration Examples for Different Use Cases

Copy one of these configurations to constants/config.py to adapt
the application to your specific needs.
"""

# ==============================================================================
# EXAMPLE 1: E-COMMERCE PRODUCTS
# ==============================================================================

# DATA_TABLE = "products"
# ID_COLUMN = "product_id"
# IMAGE_URL_COLUMN = "product_image_url"
# TITLE_COLUMN = "product_name"
# ADDITIONAL_DISPLAY_COLUMNS = ["category", "price", "sku", "stock_quantity"]
# ENTITY_LABEL = "Product"
# ENTITY_LABEL_PLURAL = "Products"

# ==============================================================================
# EXAMPLE 2: USER PROFILES / AVATARS
# ==============================================================================

# DATA_TABLE = "users"
# ID_COLUMN = "user_id"
# IMAGE_URL_COLUMN = "avatar_url"
# TITLE_COLUMN = "username"
# ADDITIONAL_DISPLAY_COLUMNS = ["email", "full_name", "created_at"]
# ENTITY_LABEL = "User"
# ENTITY_LABEL_PLURAL = "Users"

# ==============================================================================
# EXAMPLE 3: BLOG POSTS
# ==============================================================================

# DATA_TABLE = "blog_posts"
# ID_COLUMN = "post_id"
# IMAGE_URL_COLUMN = "featured_image_url"
# TITLE_COLUMN = "post_title"
# ADDITIONAL_DISPLAY_COLUMNS = ["author", "published_date", "category", "status"]
# ENTITY_LABEL = "Post"
# ENTITY_LABEL_PLURAL = "Posts"

# ==============================================================================
# EXAMPLE 4: REAL ESTATE PROPERTIES (DEFAULT)
# ==============================================================================

# DATA_TABLE = "properties_CM_pub"
# ID_COLUMN = "id"
# IMAGE_URL_COLUMN = "image_url"
# TITLE_COLUMN = "title"
# ADDITIONAL_DISPLAY_COLUMNS = ["listing_url", "price", "location"]
# ENTITY_LABEL = "Property"
# ENTITY_LABEL_PLURAL = "Properties"

# ==============================================================================
# EXAMPLE 5: TEAM MEMBERS
# ==============================================================================

# DATA_TABLE = "team_members"
# ID_COLUMN = "member_id"
# IMAGE_URL_COLUMN = "photo_url"
# TITLE_COLUMN = "full_name"
# ADDITIONAL_DISPLAY_COLUMNS = ["role", "department", "email"]
# ENTITY_LABEL = "Team Member"
# ENTITY_LABEL_PLURAL = "Team Members"

# ==============================================================================
# EXAMPLE 6: INVENTORY ITEMS
# ==============================================================================

# DATA_TABLE = "inventory"
# ID_COLUMN = "item_id"
# IMAGE_URL_COLUMN = "item_image_url"
# TITLE_COLUMN = "item_name"
# ADDITIONAL_DISPLAY_COLUMNS = ["serial_number", "location", "condition", "last_checked"]
# ENTITY_LABEL = "Item"
# ENTITY_LABEL_PLURAL = "Items"

# ==============================================================================
# EXAMPLE 7: RESTAURANT MENU ITEMS
# ==============================================================================

# DATA_TABLE = "menu_items"
# ID_COLUMN = "dish_id"
# IMAGE_URL_COLUMN = "dish_image_url"
# TITLE_COLUMN = "dish_name"
# ADDITIONAL_DISPLAY_COLUMNS = ["category", "price", "description", "allergens"]
# ENTITY_LABEL = "Dish"
# ENTITY_LABEL_PLURAL = "Dishes"

# ==============================================================================
# EXAMPLE 8: PORTFOLIO PROJECTS
# ==============================================================================

# DATA_TABLE = "portfolio_projects"
# ID_COLUMN = "project_id"
# IMAGE_URL_COLUMN = "thumbnail_url"
# TITLE_COLUMN = "project_title"
# ADDITIONAL_DISPLAY_COLUMNS = ["client", "completion_date", "project_url", "tags"]
# ENTITY_LABEL = "Project"
# ENTITY_LABEL_PLURAL = "Projects"

# ==============================================================================
# HOW TO USE
# ==============================================================================

# 1. Choose one of the examples above that matches your use case
# 2. Uncomment the configuration (remove the # at the start of each line)
# 3. Copy it to constants/config.py, replacing the TABLE CONFIGURATION section
# 4. Adjust the values to match your actual table and column names
# 5. Run the application: panel serve app.py --autoreload --show
# 6. Enjoy your customized image management tool!

# ==============================================================================
# NOTES
# ==============================================================================

# - Column names are CASE-SENSITIVE and must match exactly
# - ID_COLUMN should be unique for each record
# - IMAGE_URL_COLUMN will store the signed URL after upload
# - TITLE_COLUMN should be human-readable (used in filenames too)
# - ADDITIONAL_DISPLAY_COLUMNS is optional (can be an empty list [])
# - ENTITY_LABEL is used in UI messages and prompts (singular)
# - ENTITY_LABEL_PLURAL is used in titles and headings (plural)
