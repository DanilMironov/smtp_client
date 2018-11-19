import zipfile
import re
import os


class Ziper:

    @staticmethod
    def make_zip(address, zip_path, is_folder=False):
        if is_folder:
            with zipfile.ZipFile(zip_path, 'w') as new_zip:
                for folder, subfolder, files in os.walk(address):
                    for file in files:
                        new_zip.write(os.path.join(folder, file),
                                      compress_type=zipfile.ZIP_DEFLATED)
        else:
            with zipfile.ZipFile(zip_path, 'w') as new_zip:
                new_zip.write(address, compress_type=zipfile.ZIP_DEFLATED)

    @staticmethod
    def get_zip_path(address):
        suffix = re.search(r'\\?([ _0-9а-яА-Я\w]+)([^\\]\w+)?$',
                           address).group(1)
        try:
            zip_folder = re.search(r'(.+)(\\([ _0-9а-яА-Я\w]+)(.\w+)?$)',
                                   address)[1] + '\\'
        except TypeError:
            zip_folder = ''
        zip_path = '{0}{1}.zip'.format(zip_folder, suffix)
        is_folder = address.endswith(suffix)
        Ziper.make_zip(address, zip_path, is_folder)
        return zip_path
