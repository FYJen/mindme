class API_Base(object):
    """
    """

    @classmethod
    def get(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def find(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def _to_Dict(cls, *args, **kwargs):
        raise NotImplementedError
