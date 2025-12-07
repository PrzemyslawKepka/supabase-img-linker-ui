"""
Data service module.
Manages application data state and filtering operations.
"""

import pandas as pd
import panel as pn

from services.database_service import DatabaseService
from utils.image_validator import check_images_parallel


class DataService:
    """Service for managing application data and state."""

    def __init__(self, db_service: DatabaseService):
        """
        Initialize the data service.

        Args:
            db_service: Database service instance for data operations
        """
        self.db_service = db_service
        self.df = pd.DataFrame()

    def load_data(self) -> pd.DataFrame:
        """
        Load properties data from database and check image statuses.

        Returns:
            DataFrame with properties and their image statuses
        """
        try:
            self.df = self.db_service.fetch_properties()

            # Ensure image_url column exists
            if "image_url" not in self.df.columns:
                self.df["image_url"] = ""

            # Check image statuses in parallel
            pn.state.notifications.info("Checking image statuses...", duration=2000)
            statuses = check_images_parallel(self.df["image_url"].tolist())
            self.df["status"] = statuses

            return self.df
        except Exception as e:
            pn.state.notifications.error(f"Failed to load data: {e}")
            return pd.DataFrame()

    def get_filtered_data(self, status_filter: str) -> pd.DataFrame:
        """
        Get filtered data based on status filter.
        This method is optimized to avoid reloading data from the database.

        Args:
            status_filter: Filter value ("All", "OK", or "Error")

        Returns:
            Filtered DataFrame
        """
        if self.df.empty:
            return pd.DataFrame()

        filtered_df = self.df.copy()

        if status_filter == "OK":
            filtered_df = filtered_df[filtered_df["status"] == True]
        elif status_filter == "Error":
            filtered_df = filtered_df[filtered_df["status"] == False]

        return filtered_df

    def get_display_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get DataFrame with only display columns.

        Args:
            df: Source DataFrame

        Returns:
            DataFrame with display columns only
        """
        display_cols = ["id", "title", "image_url", "status"]
        if df.empty:
            return pd.DataFrame(columns=display_cols)
        return df[display_cols].sort_values(by="id", ascending=True)

    def get_property_by_id(self, property_id: int) -> pd.Series:
        """
        Get a specific property by its ID.

        Args:
            property_id: The property ID to retrieve

        Returns:
            Series containing the property data
        """
        return self.df[self.df["id"] == property_id].iloc[0]

    def refresh_property_status(self, property_id: int) -> None:
        """
        Refresh the image status for a specific property.

        Args:
            property_id: The property ID to refresh
        """
        idx = self.df[self.df["id"] == property_id].index[0]
        url = self.df.loc[idx, "image_url"]

        from utils.image_validator import get_image_status

        new_status = get_image_status(url)
        self.df.loc[idx, "status"] = new_status
