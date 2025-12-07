"""
Supabase Image Linker UI - Main Application
A Panel web application for managing property images with Supabase integration.

This is the main entry point that orchestrates all modules.
"""

import panel as pn

from constants.config import HEADER_BACKGROUND_COLOR
from services.data_service import DataService
from services.database_service import DatabaseService
from services.image_service import ImageService
from ui.callbacks import UICallbacks
from ui.components import UIComponents


def initialize_app():
    """
    Initialize the Panel application with all required services.

    Returns:
        Tuple of (template, callbacks) for the app
    """
    # Initialize Panel extension
    pn.extension("tabulator", notifications=True)

    # Initialize services
    try:
        db_service = DatabaseService()
        data_service = DataService(db_service)
        image_service = ImageService(db_service)
    except Exception as e:
        pn.pane.Markdown(f"## Error initializing services: {e}").servable()
        raise e

    # Initialize UI components
    ui = UIComponents()

    # Initialize callbacks
    callbacks = UICallbacks(ui, data_service, image_service)

    # Create layouts
    sidebar = ui.create_sidebar()
    main_content = ui.create_main_content()

    # Set sidebar reference in callbacks for dynamic updates
    callbacks.set_sidebar(sidebar)

    # Bind all callbacks
    callbacks.bind_callbacks()

    # Create template
    template = pn.template.BootstrapTemplate(
        title="Supabase Image Linker",
        sidebar=[sidebar],
        main=[main_content],
        header_background=HEADER_BACKGROUND_COLOR,
    )

    return template, callbacks


# Initialize and run the application
template, callbacks = initialize_app()

# Load initial data on app start
pn.state.onload(callbacks.load_and_display_data)

# Make template servable
template.servable()
