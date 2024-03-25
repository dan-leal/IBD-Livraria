from faker import Faker
from datetime import datetime
Faker.seed(0)

fake = Faker()
x = [fake.date_of_birth(minimum_age=18, format='%Y-%m-%d %H:%M:%S')]
formatted_date = x[0].strftime('%Y-%m-%d %H:%M:%S')
print(x[0])
