# Class that provides general utils.
class GeneralUtils:
    @staticmethod
    def convert_object_id_to_str(current_object):
        current_object['id'] = str(current_object['_id'])
        del current_object['_id']

