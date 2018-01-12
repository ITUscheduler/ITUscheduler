# ITUscheduler
[![LICENSE](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/language-python3-blue.svg)](#)

ITU Scheduler is a Python Django Web Application that parses ITU's SIS website and allows students to create possible course schedules.

# Installation
- Install Python 3
- `pip3 install -r requirements.txt`

# Usage on localhost
- `python3 manage.py makemigrations api scheduler`
- `python3 manage.py migrate`
- `python3 manage.py createsuperuser` to create a super-admin user
- `python3 manage.py runserver`
- Check 127.0.0.1:8000 on your browser & login
- Refresh database from Menu -> Database -> Refresh Course Codes & Refresh Courses

# Contribution
Everyone is welcome to join and make pull requests. [Contact](http://ituscheduler.com/contact) us!

# Todo
- [x] Parsing ITU SIS HTML
- [x] Course and Schedule classes
- [x] Check if a course is available
- [x] Check hours for collision
- [x] Create & save schedules
- [ ] Check major restrictions & prerequisites
- [ ] Generate & recommend possible schedules automatically

# Author
- EESTEC LC Istanbul IT Team [@eestecist](https://github.com/EESTECist)
- Doruk Gezici [@dorukgezici](https://github.com/dorukgezici)
- Mehmet Altuner [@mehmetaltuner](https://github.com/mehmetaltuner)

# License
This software is published under the [GPL v3 License](LICENSE).
