"""
UI components module.
Defines all Panel widgets and UI elements.
"""

import pandas as pd
import panel as pn

from constants.config import (
    ACCEPTED_IMAGE_FORMATS,
    IMAGE_PREVIEW_HEIGHT,
    IMAGE_PREVIEW_WIDTH,
    STATUS_FILTER_DEFAULT,
    STATUS_FILTER_OPTIONS,
    TABLE_PAGE_SIZE,
    UPLOAD_TYPE_DEFAULT,
    UPLOAD_TYPE_OPTIONS,
)
from ui.styles import FILTER_STYLESHEET


class UIComponents:
    """Container for all UI components with centralized creation."""

    def __init__(self):
        """Initialize all UI components."""
        # Header components
        self.title = pn.pane.Markdown("# Supabase Image Linker UI")
        self.subtitle = pn.pane.Markdown(
            "The table below shows the properties and their image status. "
            "Select a row to upload a new image."
        )

        # Control components
        self.refresh_btn = pn.widgets.Button(name="Refresh Data", button_type="primary")

        self.status_filter = pn.widgets.RadioButtonGroup(
            name="Status Filter",
            options=STATUS_FILTER_OPTIONS,
            value=STATUS_FILTER_DEFAULT,
            button_type="default",
        )
        # Apply custom styling
        self.status_filter.stylesheets = [FILTER_STYLESHEET]

        # Table component
        self.table = self._create_table()

        # Editor components
        self.editor_title = pn.pane.Markdown("## Edit Image")
        self.selected_property_info = pn.pane.Markdown("Select a property to edit.")
        self.current_image_preview = pn.pane.Image(
            width=IMAGE_PREVIEW_WIDTH, height=IMAGE_PREVIEW_HEIGHT, object=None
        )

        # Upload components
        self.upload_type = pn.widgets.RadioButtonGroup(
            options=UPLOAD_TYPE_OPTIONS, value=UPLOAD_TYPE_DEFAULT
        )
        self.file_input = pn.widgets.FileInput(accept=ACCEPTED_IMAGE_FORMATS)
        self.url_input = pn.widgets.TextInput(placeholder="Enter image URL here")
        self.update_btn = pn.widgets.Button(
            name="Update Image", button_type="success", disabled=True
        )

    def _create_table(self) -> pn.widgets.Tabulator:
        """
        Create and configure the data table widget.

        Returns:
            Configured Tabulator widget
        """
        return pn.widgets.Tabulator(
            pd.DataFrame(),
            selection=[0] if not pd.DataFrame().empty else [],
            disabled=True,
            pagination="remote",
            page_size=TABLE_PAGE_SIZE,
            selectable=1,
            show_index=False,
            configuration={
                "columns": [
                    {"title": "ID", "field": "id", "width": 60},
                    {"title": "Title", "field": "title", "width": 200},
                    {
                        "title": "Image URL",
                        "field": "image_url",
                        "formatter": "link",
                        "width": 450,
                    },
                    {
                        "title": "Status",
                        "field": "status",
                        "width": 100,
                        "formatter": "tickCross",
                        "formatterParams": {
                            "allowEmpty": True,
                            "allowTruthy": True,
                            "tickElement": "<span style='color:green; font-weight:bold;'>OK</span>",
                            "crossElement": "<span style='color:red; font-weight:bold;'>Error</span>",
                        },
                    },
                ]
            },
        )

    def create_sidebar(self) -> pn.Column:
        """
        Create the sidebar layout with all editor components.

        Returns:
            Panel Column containing sidebar elements
        """
        return pn.Column(
            "### Actions",
            self.refresh_btn,
            "### Editor",
            self.selected_property_info,
            self.current_image_preview,
            pn.layout.Divider(),
            "**New Image Source:**",
            self.upload_type,
            pn.Column(self.file_input, visible=True),  # Index 8
            pn.Column(self.url_input, visible=False),  # Index 9
            self.update_btn,
        )

    def create_main_content(self) -> pn.Column:
        """
        Create the main content layout.

        Returns:
            Panel Column containing main content elements
        """
        return pn.Column(
            self.title,
            self.subtitle,
            "**Filter by Status:**",
            self.status_filter,
            self.table,
        )

    def create_new_file_input(self) -> pn.widgets.FileInput:
        """
        Create a fresh file input widget.
        Used to reset the file input after upload.

        Returns:
            New FileInput widget
        """
        return pn.widgets.FileInput(accept=ACCEPTED_IMAGE_FORMATS)
