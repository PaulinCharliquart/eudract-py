class EudractError(Exception):
    """Base exception for all eudract-py errors."""


class StudyNotFoundError(EudractError):
    """Raised when a study cannot be found for the given EudraCT number."""
