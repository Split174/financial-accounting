"""
module contains the main exception for inheritance
"""
class SeviceError(Exception):
    """
    The main exception for inheritance
    """
    service = None

    def __init__(self, *args):
        super().__init__(self.service, *args)
