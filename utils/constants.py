from typing import Dict

NULL_BLANK: Dict = {"null": True, "blank": True}
ALLOW_NOT_NULL: Dict = {"null": False, "blank": False}
CHAR_NULL_BLANK: Dict = {"max_length": 100, "blank": True, "null": True}
CHAR_NOT_NULL_BLANK: Dict = {"max_length": 100, "blank": False, "null": False}
READ_ONLY_REQUIRED_FALSE: Dict = {"read_only": True, "required": False}
ALLOW_BLANK_REQUIRED_FALSE: Dict = {"allow_blank": True, "required": False}
MINIMUM_AGE: int = 10
MAXIMUM_AGE: int = 20
