import os

import cloudinary
import cloudinary.uploader


class CloudinaryHelper:
    def __init__(self, auth_param):
        self.saving_folder_name = 'buzzistore'
        self.cloud_name = auth_param['cloud_name']
        self.client = cloudinary
        self.client.config(
            cloud_name=auth_param['cloud_name'],
            api_key=auth_param['api_key'],
            api_secret=auth_param['api_secret'],
        )

    def upload_file(self, path_to_img):
        filename = os.path.basename(path_to_img)
        filename_without_ext, _ = os.path.splitext(filename)
        public_id = self.saving_folder_name + '/' + filename_without_ext
        self.client.uploader.upload(path_to_img, public_id=public_id, unique_filename=False, resource_type = "raw")

        return self._get_url(filename)

    def _get_url(self, filename):
        return (
            f'https://res.cloudinary.com/{self.cloud_name}'
            + f'/raw/upload/v1612014771/{self.saving_folder_name}/{filename}'
        )


if __name__ == "__main__":
    auth_param = {}
    cld_helper = CloudinaryHelper(auth_param)
    img_path = 'C:\\Users\\user\\Desktop\\src\\bluestack\\todo\\블레이드앤소울레볼루션\\블레이드앤소울레볼루션_1.jpg'
    url = cld_helper.upload_img(img_path)
    print(url)