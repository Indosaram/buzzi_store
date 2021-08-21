"""Cloudinary helper class"""

import os

import cloudinary
import cloudinary.uploader
import cloudinary.api


class CloudinaryHelper:
    """Cloudinary helper class"""

    def __init__(self, folder_name):
        self.saving_folder_name = folder_name
        self.cloud_name = os.getenv("CLOUDINARY_NAME")
        self.client = cloudinary
        self.client.config(
            cloud_name=self.cloud_name,
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        )

    def upload_file(self, path_to_file):
        """upload file by path"""
        public_id = self._get_public_id(path_to_file)
        response = self.client.uploader.upload(
            path_to_file,
            public_id=public_id,
            unique_filename=False,
            resource_type="raw",
        )

        return response["secure_url"]

    def get_url(self, filename):
        """Return url of a file in cloudinary"""
        public_id = self._get_public_id(filename)
        result = (
            cloudinary.Search().expression(f"public_id={public_id}").execute()
        )
        return result["resources"][0]["secure_url"]

    def _get_public_id(self, filename):
        public_id = f"{self.saving_folder_name}/{os.path.basename(filename)}"
        return public_id
