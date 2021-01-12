# ITUscheduler
[![LICENSE](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/language-python3-blue.svg)](#)

ITU Scheduler is a Python Django Web Application that parses ITU's SIS website and allows students to create possible course schedules with up-to-date & detailed information. The project is maintained by [@dorukgezici](https://github.com/dorukgezici).

# Installation
- Install Python 3
- `pip3 install -r requirements.txt`

# Usage on localhost
- `python3 manage.py makemigrations api scheduler blog`
- `python3 manage.py migrate`
- `python3 manage.py createsuperuser` to create a super-admin user
- `python3 manage.py runserver`
- Check 127.0.0.1:8000 on your browser & login
- Refresh database from Menu -> Database -> Refresh Course Codes & Refresh Courses

# Contribution
Everyone is welcome to contribute. [Contact](mailto:info@gamerarena.com) us if you want to be a part of the development team! Also if you find any bugs or you have some ideas / feedback, please create an issue on [GitHub](https://github.com/dorukgezici/ITUscheduler/issues).

# Todo
- [x] Parsing ITU SIS HTML
- [x] Course and Schedule classes
- [x] Check if a course is available
- [x] Check hours for collision
- [x] Create & save schedules
- [x] Upload old semesters by HTML file
- [x] Task queue to refresh the database automatically
- [ ] Check major restrictions & prerequisites
- [ ] Generate & recommend possible schedules automatically

# Author
- Doruk Gezici [@dorukgezici](https://github.com/dorukgezici)
- Mehmet Altuner [@mehmetaltuner](https://github.com/mehmetaltuner)

# License
This software is published under the [GPL v3 License](LICENSE).
