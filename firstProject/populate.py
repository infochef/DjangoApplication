import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firstProject.settings")

import django
django.setup()
from firstapp.models import *
# from django.core.management import execute_from_command_line
import random
from faker import Faker

fake = Faker()
topics = ['Search', 'Social', 'Twitter', 'Facebook', 'Instagram', 'YouTube']

def add_topic():
    t = Topic.objects.get_or_create(topics=random.choice(topics))[0]
    t.save()
    return t

def populate_db(N=5):
    for entry in range(N):

        top = add_topic()

        fakeurl = fake.url()
        fakedate = fake.date()
        fakecompany = fake.company()

        webpg = Webpage.objects.get_or_create(topic=top, url=fakeurl, name=fakecompany)[0]

        acc_rec = AccessRecord.objects.get_or_create(name=webpg, date=fakedate)[0]

# execute_from_command_line(sys.argv)


if __name__ == '__main__':
    print('Populating Script!!')
    populate_db(20)
    print('Populating Completed!')
