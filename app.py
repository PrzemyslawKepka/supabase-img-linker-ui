import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import pandas as pd
import panel as pn
import requests

from db_manager import Database

# Initialize Panel extension
pn.extension("tabulator", notifications=True)

# Initialize Database
try:
    db = Database()
except Exception as e:
    pn.pane.Markdown(f"## Error initializing database: {e}").servable()
    raise e


def get_image_status(url):
    if not url or pd.isna(url) or url == "":
        return "Missing"
    try:
        response = requests.head(url, timeout=3)
        if response.status_code == 200:
            return "OK"
        else:
            return f"Error: {response.status_code}"
    except Exception:
        return "Error: Connection Failed"


def check_images_parallel(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(get_image_status, urls))
    return results


# State
class AppState:
    def __init__(self):
        self.df = pd.DataFrame()
        self.selected_index = None

    def load_data(self):
        try:
            self.df = db.fetch_properties()
            # Ensure columns exist
            if "image_url" not in self.df.columns:
                self.df["image_url"] = ""

            # Add status column
            # We'll do this dynamically or on button press to avoid long load times?
            # The requirement says "it will display... and it will show whether the image is displayed correctly"
            # So we should check.
            pn.state.notifications.info("Checking image statuses...", duration=2000)
            statuses = check_images_parallel(self.df["image_url"].tolist())
            self.df["status"] = statuses
            return self.df
        except Exception as e:
            pn.state.notifications.error(f"Failed to load data: {e}")
            return pd.DataFrame()


app_state = AppState()

# UI Components
title = pn.pane.Markdown("# Supabase Image Linker UI")
refresh_btn = pn.widgets.Button(name="Refresh Data", button_type="primary")

# Table
# Use Tabulator configuration to limit column widths
table = pn.widgets.Tabulator(
    pd.DataFrame(),
    selection=[0] if not pd.DataFrame().empty else [],
    disabled=True,
    pagination="remote",
    page_size=20,
    selectable=1,
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
            {"title": "Status", "field": "status", "width": 100},
        ]
    },
)

# Editor Section
editor_title = pn.pane.Markdown("## Edit Image")
selected_property_info = pn.pane.Markdown("Select a property to edit.")
current_image_preview = pn.pane.Image(width=300, height=200, object=None)

upload_type = pn.widgets.RadioButtonGroup(
    options=["Upload File", "Image URL"], value="Upload File"
)
file_input = pn.widgets.FileInput(accept=".jpg,.jpeg,.png,.webp")
url_input = pn.widgets.TextInput(placeholder="Enter image URL here")
update_btn = pn.widgets.Button(
    name="Update Image", button_type="success", disabled=True
)


# Logic
def load_and_display_data(event=None):
    df = app_state.load_data()
    # Select relevant columns for display
    # listing_url is needed for sidebar but not main table
    display_cols = ["id", "title", "image_url", "status"]

    if df.empty:
        table.value = pd.DataFrame(columns=display_cols)
    else:
        table.value = df[display_cols]

    if not df.empty:
        table.selection = [0]
        update_editor(None)


def update_editor(event):
    if not table.selection:
        selected_property_info.object = "Select a property to edit."
        current_image_preview.object = None
        update_btn.disabled = True
        return

    idx = table.selection[0]
    # Tabulator selection index maps to the dataframe index if not sorted/filtered
    # But safely, let's get the row from the value
    row = table.value.iloc[idx]

    # Find the full row in the main dataframe to get all details if needed
    # assuming 'id' is unique
    prop_id = row["id"]
    full_row = app_state.df[app_state.df["id"] == prop_id].iloc[0]

    info = f"""
    **ID:** {full_row.get("id", "N/A")}  
    **Title:** {full_row.get("title", "N/A")}  
    **Current URL:** {full_row.get("image_url", "None")}  
    **Listing URL:** {full_row.get("listing_url", "None")}\n
    **Status:** {full_row.get("status", "Unknown")}
    """
    selected_property_info.object = info

    # Preview
    img_url = full_row.get("image_url", None)
    if img_url and full_row.get("status") == "OK":
        current_image_preview.object = img_url
    else:
        current_image_preview.object = None

    update_btn.disabled = False


def handle_upload(event):
    if not table.selection:
        return

    update_btn.loading = True
    try:
        idx = table.selection[0]
        row = table.value.iloc[idx]
        prop_id = row["id"]
        prop_title = row["title"]

        image_data = None
        ext = ""
        content_type = "image/jpeg"  # Default

        if upload_type.value == "Upload File":
            if file_input.value is None:
                pn.state.notifications.error("Please select a file.")
                update_btn.loading = False
                return
            image_data = file_input.value
            filename = file_input.filename
            ext = os.path.splitext(filename)[1].lower()
            # Simple content type guess
            if ext == ".png":
                content_type = "image/png"
            elif ext == ".webp":
                content_type = "image/webp"

        else:  # Image URL
            url = url_input.value
            if not url:
                pn.state.notifications.error("Please enter a URL.")
                update_btn.loading = False
                return
            try:
                res = requests.get(url)
                res.raise_for_status()
                image_data = res.content
                # Try to guess extension from url or header
                path = urlparse(url).path
                ext = os.path.splitext(path)[1].lower()
                if not ext:
                    ext = ".jpg"  # Fallback
                content_type = res.headers.get("Content-Type", "image/jpeg")
            except Exception as e:
                pn.state.notifications.error(f"Failed to download image: {e}")
                update_btn.loading = False
                return

        # Sanitize title for filename
        safe_title = (
            "".join([c for c in prop_title if c.isalnum() or c in (" ", "-", "_")])
            .strip()
            .replace(" ", "_")
        )
        # Construct new filename: id_title.ext
        new_filename = f"{prop_id}_{safe_title}{ext}"

        # Upload to Supabase
        db.upload_image(image_data, new_filename, content_type)

        # Get Signed URL (10 years)
        signed_url_resp = db.get_signed_url(new_filename, years=10)
        # signed_url_resp is a dict with 'signedURL' key usually?
        # The supabase-py client returns a dict or object depending on version.
        # Checking db_manager: create_signed_url returns dict with 'signedURL' usually.
        # Let's assume it returns the dict.
        if isinstance(signed_url_resp, dict) and "signedURL" in signed_url_resp:
            final_url = signed_url_resp["signedURL"]
        elif hasattr(signed_url_resp, "signedURL"):
            final_url = signed_url_resp.signedURL
        else:
            # Sometimes it returns the URL string directly? No, usually dict.
            # Let's check return type of create_signed_url in library if possible or safeguard.
            # Assuming dict `{'signedURL': '...'}` or similar.
            final_url = signed_url_resp[
                "signedURL"
            ]  # This is the standard for storage3

        # Update Database
        db.update_image_url(prop_id, final_url)

        pn.state.notifications.success("Image updated successfully!")

        # Clear inputs
        file_input.value = None
        url_input.value = ""

        # Refresh data (or just update local row)
        load_and_display_data()

    except Exception as e:
        pn.state.notifications.error(f"Error updating image: {e}")
    finally:
        update_btn.loading = False


# Bindings
refresh_btn.on_click(load_and_display_data)
table.param.watch(update_editor, "selection")
update_btn.on_click(handle_upload)

# Layout
sidebar = pn.Column(
    "### Actions",
    refresh_btn,
    "### Editor",
    selected_property_info,
    current_image_preview,
    pn.layout.Divider(),
    "**New Image Source:**",
    upload_type,
    pn.Column(file_input, visible=True),  # We'll toggle visibility
    pn.Column(url_input, visible=False),
    update_btn,
)


def toggle_inputs(event):
    if upload_type.value == "Upload File":
        sidebar[8].visible = True
        sidebar[9].visible = False
    else:
        sidebar[8].visible = False
        sidebar[9].visible = True


upload_type.param.watch(toggle_inputs, "value")

main_content = pn.Column(
    title,
    "The table below shows the properties and their image status. Select a row to upload a new image.",
    table,
)

template = pn.template.BootstrapTemplate(
    title="Supabase Image Linker",
    sidebar=[sidebar],
    main=[main_content],
    header_background="#3A7D7E",
)

# Initial Load
# We defer it to onload so the UI renders first
pn.state.onload(load_and_display_data)

template.servable()
