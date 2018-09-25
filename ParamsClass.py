class Params:
    def __init__(self, access_token, api_version):
        self.options = {}
        self.options.update({'v': api_version, 'access_token': access_token})

    def get_package(self):
        return self.options

    def add_fields(self, params_dict):
        self.options.update(params_dict)
