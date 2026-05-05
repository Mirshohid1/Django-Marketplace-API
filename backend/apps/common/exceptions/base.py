class DomainError(Exception):
    code = "domain_error"
    message = "A domain error occurred"
    status_code = 400
    details = None

    def __init__(self, message=None, *, details=None):
        if message:
            self.message = message
        if details is not None:
            self.details = details
        super().__init__(self.message)


class ValidationError(DomainError):
    code = "validation_error"
    message = "Invalid data"
    status_code = 400


class NotFoundError(DomainError):
    code = "not_found"
    message = "Object not found"
    status_code = 404


class ConflictError(DomainError):
    code = "conflict"
    message = "Conflict"
    status_code = 409


class PermissionDeniedError(DomainError):
    code = "permission_denied"
    message = "Permission denied"
    status_code = 403
