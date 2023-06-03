class DatabaseError(Exception):
    pass

class DuplicateEntryError(DatabaseError):
    pass

class NotFoundError(DatabaseError):
    pass

class CredentialsError(Exception):
    pass
