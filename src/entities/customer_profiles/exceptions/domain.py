class CustomerProfileNotFoundError(Exception):
    def __repr__(self):
        return "Customer profile not found"


class CustomerProfileIsNotUniqueError(Exception):
    def __repr__(self):
        return "Customer profile not found"
