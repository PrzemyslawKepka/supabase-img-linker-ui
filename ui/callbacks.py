"""
UI callbacks module.
Contains all event handlers and callback functions for UI interactions.
"""

import panel as pn

from services.data_service import DataService
from services.image_service import ImageService
from ui.components import UIComponents


class UICallbacks:
    """Manages all UI event callbacks and interactions."""

    def __init__(
        self, ui: UIComponents, data_service: DataService, image_service: ImageService
    ):
        """
        Initialize callbacks with required services.

        Args:
            ui: UI components instance
            data_service: Data service for managing application data
            image_service: Image service for upload operations
        """
        self.ui = ui
        self.data_service = data_service
        self.image_service = image_service
        self.sidebar = None  # Will be set after layout creation

    def set_sidebar(self, sidebar: pn.Column):
        """
        Set the sidebar reference for component updates.

        Args:
            sidebar: The sidebar Column layout
        """
        self.sidebar = sidebar

    def load_and_display_data(self, event=None):
        """
        Load data from database and display in table with current filter.
        This is optimized to only reload from DB when explicitly refreshed.

        Args:
            event: Panel event (optional)
        """
        # Only load from database if explicitly refreshed or data is empty
        if event is not None or self.data_service.df.empty:
            self.data_service.load_data()

        # Apply filter (optimized - no DB reload)
        filtered_df = self.data_service.get_filtered_data(self.ui.status_filter.value)
        display_df = self.data_service.get_display_columns(filtered_df)

        # Update table
        self.ui.table.value = display_df

        # Handle selection
        if not self.ui.table.value.empty:
            self.ui.table.selection = [0]
            self.update_editor(None)
        else:
            self.ui.table.selection = []
            self.update_editor(None)

    def filter_data(self, event):
        """
        Filter displayed data without reloading from database.
        Optimized for fast filtering.

        Args:
            event: Panel event from filter change
        """
        filtered_df = self.data_service.get_filtered_data(self.ui.status_filter.value)
        display_df = self.data_service.get_display_columns(filtered_df)

        # Update table
        self.ui.table.value = display_df

        # Reset selection to first row if available
        if not self.ui.table.value.empty:
            self.ui.table.selection = [0]
            self.update_editor(None)
        else:
            self.ui.table.selection = []
            self.update_editor(None)

    def update_editor(self, event):
        """
        Update editor panel based on table selection.

        Args:
            event: Panel event from table selection
        """
        if not self.ui.table.selection:
            self.ui.selected_property_info.object = "Select a property to edit."
            self.ui.current_image_preview.object = None
            self.ui.update_btn.disabled = True
            return

        idx = self.ui.table.selection[0]
        row = self.ui.table.value.iloc[idx]

        # Get full row data from data service
        prop_id = row["id"]
        full_row = self.data_service.get_property_by_id(prop_id)

        # Update image preview
        img_url = full_row.get("image_url", None)
        status = full_row.get("status")

        if img_url and status:
            self.ui.current_image_preview.object = img_url
        else:
            self.ui.current_image_preview.object = None

        # Update info display
        status_text = "OK" if status else "Error/Missing"
        info = f"""
        **ID:** {full_row.get("id", "N/A")}  
        **Title:** {full_row.get("title", "N/A")}  
        **Current URL:** {full_row.get("image_url", "None")}  
        **Listing URL:** {full_row.get("listing_url", "None")}\n
        **Status:** {status_text}
        """
        self.ui.selected_property_info.object = info

        # Enable update button
        self.ui.update_btn.disabled = False

    def handle_upload(self, event):
        """
        Handle image upload (file or URL).

        Args:
            event: Panel event from upload button
        """
        if not self.ui.table.selection:
            return

        self.ui.update_btn.loading = True

        try:
            # Get selected property info
            idx = self.ui.table.selection[0]
            row = self.ui.table.value.iloc[idx]
            prop_id = row["id"]
            prop_title = row["title"]

            # Process upload based on type
            if self.ui.upload_type.value == "Upload File":
                self._handle_file_upload(prop_id, prop_title)
            else:
                self._handle_url_upload(prop_id, prop_title)

            # Success notification
            pn.state.notifications.success("Image updated successfully!")

            # Clear inputs and refresh
            self._clear_inputs()
            self._refresh_after_upload()

        except Exception as e:
            pn.state.notifications.error(f"Error updating image: {e}")
        finally:
            self.ui.update_btn.loading = False

    def _handle_file_upload(self, prop_id: int, prop_title: str):
        """Handle file upload."""
        if self.ui.file_input.value is None:
            raise ValueError("Please select a file.")

        self.image_service.process_file_upload(
            prop_id, prop_title, self.ui.file_input.value, self.ui.file_input.filename
        )

    def _handle_url_upload(self, prop_id: int, prop_title: str):
        """Handle URL upload."""
        if not self.ui.url_input.value:
            raise ValueError("Please enter a URL.")

        self.image_service.process_url_upload(
            prop_id, prop_title, self.ui.url_input.value
        )

    def _clear_inputs(self):
        """Clear upload inputs after successful upload."""
        # Replace file input to force clear
        new_file_input = self.ui.create_new_file_input()
        if self.sidebar:
            self.sidebar[8][0] = new_file_input
            self.ui.file_input = new_file_input

        # Clear URL input
        self.ui.url_input.value = ""

    def _refresh_after_upload(self):
        """Refresh data after upload maintaining selection."""
        current_selection = self.ui.table.selection
        self.load_and_display_data()

        # Restore selection if possible
        if current_selection:
            self.ui.table.selection = current_selection

    def toggle_inputs(self, event):
        """
        Toggle visibility of file/URL inputs based on upload type.

        Args:
            event: Panel event from upload type change
        """
        if not self.sidebar:
            return

        if self.ui.upload_type.value == "Upload File":
            self.sidebar[8].visible = True  # File input container
            self.sidebar[9].visible = False  # URL input container
        else:
            self.sidebar[8].visible = False
            self.sidebar[9].visible = True

    def bind_callbacks(self):
        """Bind all callbacks to their respective UI components."""
        # Refresh button triggers full data reload
        self.ui.refresh_btn.on_click(self.load_and_display_data)

        # Filter uses optimized filtering without DB reload
        self.ui.status_filter.param.watch(self.filter_data, "value")

        # Table selection updates editor
        self.ui.table.param.watch(self.update_editor, "selection")

        # Upload button
        self.ui.update_btn.on_click(self.handle_upload)

        # Upload type toggle
        self.ui.upload_type.param.watch(self.toggle_inputs, "value")
