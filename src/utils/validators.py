# src/utils/validators.py

from functools import wraps
from datetime import date, time, datetime
from decimal import Decimal
import re


class Validators:

    # ============================================================
    # STRING VALIDATOR
    # ============================================================

    @staticmethod
    def string(max_length=None, required=True):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Validate required fields
                if required and (
                    value is None
                    or (
                        isinstance(value, str)
                        and value.strip() == ""
                    )
                ):
                    raise ValueError("This field is required.")

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Validate data type
                if not isinstance(value, str):
                    raise ValueError(
                        "The value must be a string."
                    )

                # Remove unnecessary spaces
                value = value.strip()

                # Validate maximum length
                if (
                    max_length is not None
                    and len(value) > max_length
                ):
                    raise ValueError(
                        f"The value cannot exceed "
                        f"{max_length} characters."
                    )

                return func(self, value)

            return wrapper

        return decorator

    # ============================================================
    # TEXT VALIDATOR
    # ============================================================

    @staticmethod
    def text(
        max_length=None,
        required=True,
        allow_special_characters=True
    ):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Validate required fields
                if required and (
                    value is None
                    or (
                        isinstance(value, str)
                        and value.strip() == ""
                    )
                ):
                    raise ValueError("This field is required.")

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Validate data type
                if not isinstance(value, str):
                    raise ValueError(
                        "The value must be a string."
                    )

                # Remove unnecessary spaces
                value = value.strip()

                # Validate maximum length
                if (
                    max_length is not None
                    and len(value) > max_length
                ):
                    raise ValueError(
                        f"The value cannot exceed "
                        f"{max_length} characters."
                    )

                # Validate special characters
                if not allow_special_characters:

                    if not re.match(
                        r"^[a-zA-ZÀ-ÿ0-9\s]+$",
                        value
                    ):
                        raise ValueError(
                            "The value contains invalid characters."
                        )

                return func(self, value)

            return wrapper

        return decorator

    # ============================================================
    # INTEGER VALIDATOR
    # ============================================================

    @staticmethod
    def integer(
        min_value=None,
        max_value=None,
        required=True
    ):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Validate integer type
                if not isinstance(value, int) or isinstance(value, bool):
                    raise ValueError(
                        "The value must be an integer."
                    )

                # Validate minimum value
                if (
                    min_value is not None
                    and value < min_value
                ):
                    raise ValueError(
                        f"The value must be greater than "
                        f"or equal to {min_value}."
                    )

                # Validate maximum value
                if (
                    max_value is not None
                    and value > max_value
                ):
                    raise ValueError(
                        f"The value must be less than "
                        f"or equal to {max_value}."
                    )

                return func(self, value)

            return wrapper

        return decorator

    # ============================================================
    # DECIMAL VALIDATOR
    # ============================================================

    @staticmethod
    def decimal(
        min_value=None,
        max_value=None,
        required=True
    ):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Try to convert the value to Decimal
                try:
                    value = Decimal(str(value))
                except Exception:
                    raise ValueError(
                        "The value must be numeric."
                    )

                # Validate minimum value
                if (
                    min_value is not None
                    and value < Decimal(str(min_value))
                ):
                    raise ValueError(
                        f"The value must be greater than "
                        f"or equal to {min_value}."
                    )

                # Validate maximum value
                if (
                    max_value is not None
                    and value > Decimal(str(max_value))
                ):
                    raise ValueError(
                        f"The value must be less than "
                        f"or equal to {max_value}."
                    )

                return func(self, value)

            return wrapper

        return decorator

    # ============================================================
    # BOOLEAN VALIDATOR
    # ============================================================

    @staticmethod
    def boolean(required=True):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Validate boolean type
                if not isinstance(value, bool):
                    raise ValueError(
                        "The value must be boolean."
                    )

                return func(self, value)

            return wrapper

        return decorator

    # ============================================================
    # EMAIL VALIDATOR
    # ============================================================

    @staticmethod
    def email(max_length=150, required=True):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Validate required fields
                if required and (
                    value is None
                    or (
                        isinstance(value, str)
                        and value.strip() == ""
                    )
                ):
                    raise ValueError(
                        "Email is required."
                    )

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Validate data type
                if not isinstance(value, str):
                    raise ValueError(
                        "Email must be a string."
                    )

                # Remove unnecessary spaces
                value = value.strip()

                # Validate email length
                if len(value) > max_length:
                    raise ValueError(
                        f"Email cannot exceed "
                        f"{max_length} characters."
                    )

                # Basic email format validation
                email_pattern = (
                    r"^[A-Za-z0-9._%+-]+@"
                    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
                )

                if not re.match(
                    email_pattern,
                    value
                ):
                    raise ValueError(
                        "Invalid email format."
                    )

                return func(self, value)

            return wrapper

        return decorator

    # ============================================================
    # DATE VALIDATOR
    # ============================================================

    @staticmethod
    def date(required=True):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Validate date type
                if not isinstance(value, date):
                    raise ValueError(
                        "The value must be a valid date."
                    )

                return func(self, value)

            return wrapper

        return decorator

    # ============================================================
    # TIME VALIDATOR
    # ============================================================

    @staticmethod
    def time(required=True):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Validate time type
                if not isinstance(value, time):
                    raise ValueError(
                        "The value must be a valid time."
                    )

                return func(self, value)

            return wrapper

        return decorator

    # ============================================================
    # DATETIME VALIDATOR
    # ============================================================

    @staticmethod
    def datetime(required=True):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Validate datetime type
                if not isinstance(value, datetime):
                    raise ValueError(
                        "The value must be a valid datetime."
                    )

                return func(self, value)

            return wrapper

        return decorator

    # ============================================================
    # SQL INJECTION VALIDATOR
    # ============================================================

    @staticmethod
    def sql_safe(required=True):

        def decorator(func):

            @wraps(func)
            def wrapper(self, value):

                # Validate required fields
                if required and (
                    value is None
                    or (
                        isinstance(value, str)
                        and value.strip() == ""
                    )
                ):
                    raise ValueError(
                        "This field is required."
                    )

                # Allow None when the field is optional
                if value is None and not required:
                    return func(self, value)

                # Validate data type
                if not isinstance(value, str):
                    raise ValueError(
                        "The value must be a string."
                    )

                # Remove unnecessary spaces
                value = value.strip()

                # SQL keywords and patterns commonly associated
                # with SQL injection attempts
                sql_patterns = [
                    r"--",
                    r"/\*",
                    r"\*/",
                    r"\bOR\b",
                    r"\bAND\b",
                    r"\bSELECT\b",
                    r"\bINSERT\b",
                    r"\bUPDATE\b",
                    r"\bDELETE\b",
                    r"\bDROP\b",
                    r"\bALTER\b",
                    r"\bCREATE\b",
                    r"\bUNION\b",
                    r"\bEXEC\b",
                    r"\bEXECUTE\b",
                    r"\bTRUNCATE\b"
                ]

                # Check for dangerous SQL patterns
                for pattern in sql_patterns:

                    if re.search(
                        pattern,
                        value,
                        re.IGNORECASE
                    ):
                        raise ValueError(
                            "The value contains a potentially "
                            "dangerous SQL pattern."
                        )

                # Characters commonly used to manipulate SQL queries
                dangerous_characters = [
                    "'",
                    '"',
                    ";",
                    "`"
                ]

                # Check for dangerous characters
                for character in dangerous_characters:

                    if character in value:
                        raise ValueError(
                            "The value contains invalid characters."
                        )

                return func(self, value)

            return wrapper

        return decorator