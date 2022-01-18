import random
from typing import Dict, List, Tuple

import faker.providers
from django.core.management.base import BaseCommand
from faker import Faker

from core.models import School, Student

TITLES: List = ["MR", "MRS", "MISS", "MS"]

GENDERS: List = ["MALE", "FEMALE"]


class Provider(faker.providers.BaseProvider):
    def student_titles(self) -> List:
        return self.random_element(TITLES)

    def student_genders(self) -> List:
        return self.random_element(GENDERS)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args: Tuple, **kwargs: Dict) -> None:

        faker: Faker = Faker()
        faker.add_provider(Provider)

        for _ in range(10):
            school: School = School.objects.create(
                name=faker.company()[:20].rstrip(),
                code=f"A{random.randint(1000, 9999)}",
                location=faker.city(),
                student_max_number=random.randint(10, 20),
            )

            for _ in range(10):
                Student.objects.create(
                    title=faker.student_titles(),
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    age=random.randint(5, 15),
                    gender=faker.student_genders(),
                    school=school,
                )
