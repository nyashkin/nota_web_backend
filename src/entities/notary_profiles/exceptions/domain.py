class NotaryProfileNotFoundError(Exception):
    def __repr__(self):
        return "Notary profile not found"


class NotaryProfileIsNotUniqueError(Exception):
    def __repr__(self):
        return "Notary profile not found"
