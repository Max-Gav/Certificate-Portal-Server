import os
import aiobcrypt
import base64


# Class that provides general utils.
class GeneralUtils:
    def convert_object_id_to_str(self, object):
        object['id'] = str(object['_id'])
        del object['_id']

