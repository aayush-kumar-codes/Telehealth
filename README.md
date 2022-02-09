# Telehealth

## Overview

This is microservice for Telehealth application, having three language choices where Doctor can make slots for bookings and patient can book their appointments (Online or Clinical). It also contains authentication and verification of users.

## Initial setup

```python
git clone https://github.com/pythexcel/Telehealth.git
cd Telehealth
python -m venv env
source env/bin/activate (for linux)
./env/Scripts/activate (for windows)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Functionalities:

- The doctor is able to sign up and in using phone number.
- The doctor is able to set his/her available time slots for consultation.
- The doctor is able to see his/her bookings.
- The doctor is able to edit his/her personal information.
- The api have Authentication and Verification

## Routes:

- sign_up
- sign_in
- get_my_accoount
- get_my_bookings
- set_my_availavle_slot
- get_my_availability_slots
- get_my_accoount ('edit_my_profile' in edit the doctor will be able to edit his/her specialty, image, about, etc and not his/her name.)
- get_my_patients
