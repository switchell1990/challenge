from core.models import School
from utils.constants import MAXIMUM_AGE, MINIMUM_AGE


def age_validation_check(age: int) -> bool:
    return (age < MINIMUM_AGE) or (age > MAXIMUM_AGE)


def is_max_student_count(school: School) -> bool:
    return bool(school.student.count() == school.student_max_number)
