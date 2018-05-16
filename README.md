# ITUscheduler
[![LICENSE](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/language-python3-blue.svg)](#)

ITU Scheduler is a Python Django Web Application that parses ITU's SIS website and allows students to create possible course schedules with up-to-date & detailed information. The project is maintained by EESTEC LC Istanbul's IT Team.

# Installation
- Install Python 3
- `pip3 install -r requirements.txt`
- Install [WeasyPrint's dependencies](http://weasyprint.readthedocs.io/en/latest/install.html)
    - MacOS: `brew install python3 cairo pango gdk-pixbuf libffi`
    - Debian / Ubuntu: `sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info`
    - [Windows](http://weasyprint.readthedocs.io/en/latest/install.html#windows)

# Usage on localhost
- `python3 manage.py makemigrations api scheduler blog`
- `python3 manage.py migrate`
- `python3 manage.py createsuperuser` to create a super-admin user
- `python3 manage.py runserver`
- Check 127.0.0.1:8000 on your browser & login
- Refresh database from Menu -> Database -> Refresh Course Codes & Refresh Courses

# Contribution
Everyone is welcome to contribute. [Contact](http://ituscheduler.com/contact) us if you want to be a part of the development team! Also if you find any bugs or you have some ideas / feedback, please create an issue on [GitHub](https://github.com/dorukgezici/ITUscheduler/issues).

# Todo
- [x] Parsing ITU SIS HTML
- [x] Course and Schedule classes
- [x] Check if a course is available
- [x] Check hours for collision
- [x] Create & save schedules
- [ ] Cronjob to refresh the database automatically
- [ ] Check major restrictions & prerequisites
- [ ] Generate & recommend possible schedules automatically

# Author
- EESTEC LC Istanbul IT Team [@eestecist](https://github.com/EESTECist)
- Doruk Gezici [@dorukgezici](https://github.com/dorukgezici)
- Mehmet Altuner [@mehmetaltuner](https://github.com/mehmetaltuner)

# License
This software is published under the [GPL v3 License](LICENSE).
