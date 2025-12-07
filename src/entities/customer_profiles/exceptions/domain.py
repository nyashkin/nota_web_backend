class CustomerProfileNotFoundException(Exception):
    def __repr__(self):
        return "Customer profile not found"


class CustomerProfileIsNotUniqueException(Exception):
    def __repr__(self):
        return "Customer profile not found"
