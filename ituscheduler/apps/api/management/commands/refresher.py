import threading
import requests
from django.core.management.base import BaseCommand
from ituscheduler.settings.secrets import SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD


LOGIN_URL = "https://ituscheduler.com/accounts/login/"
API_URL = "https://ituscheduler.com/api/db/refresh/courses"


class ITUschedulerSession:
    def __init__(self):
        self.session = requests.session()
        self.session.get(LOGIN_URL)
        token = self.session.cookies["csrftoken"]
        self.session.post(
            LOGIN_URL,
            data={
                "username": SUPERADMIN_USERNAME,
                "password": SUPERADMIN_PASSWORD,
                "csrfmiddlewaretoken": token
            },
            headers={"Referer": LOGIN_URL}
        )


class ITUschedulerRefresher(threading.Thread):
    def __init__(self, session, major_codes):
        super().__init__()
        self.session = session
        self.major_codes = major_codes

    def run(self):
        payload = {"major_codes[]": self.major_codes}
        r = self.session.post(
            API_URL,
            data=payload,
            headers={"referer": API_URL}
        )
        print(r.status_code, r.text)


class Command(BaseCommand):
    help = "Refresh ITUscheduler's database from SIS for all major codes."

    def handle(self, *args, **options):
        session = ITUschedulerSession().session
        major_codes = ['AKM', 'ALM', 'ATA', 'BEB', 'BED', 'BEN', 'BIL', 'BIO', 'BLG', 'BLS', 'BUS', 'CAB', 'CEV', 'CHE', 'CHZ', 'CIE', 'CIN', 'CMP', 'COM', 'DAN', 'DEN', 'DFH', 'DGH', 'DNK', 'DUI', 'EAS', 'ECN', 'ECO', 'EHA', 'EHB', 'EHN', 'EKO', 'ELE', 'ELH', 'ELK', 'ELT', 'END', 'ENE', 'ENG', 'ENR', 'ESL', 'ESM', 'ETK', 'EUT', 'FIZ', 'FRA', 'FZK', 'GED', 'GEM', 'GEO', 'GID', 'GLY', 'GMI', 'GMK', 'GSB', 'GSN', 'GUV', 'GVT', 'HSS', 'HUK', 'ICM', 'ILT', 'IML', 'ING', 'INS', 'ISE', 'ISH', 'ISL', 'ISP', 'ITA', 'ITB', 'JDF', 'JEF', 'JEO', 'JPN', 'KIM', 'KMM', 'KMP', 'KON', 'LAT', 'MAD', 'MAK', 'MAL', 'MAT', 'MCH', 'MEK', 'MEN', 'MET', 'MIM', 'MKN', 'MOD', 'MRE', 'MRT', 'MST', 'MTH', 'MTK', 'MTM', 'MTO', 'MTR', 'MUH', 'MUK', 'MUT', 'MUZ', 'NAE', 'NTH', 'PAZ', 'PEM', 'PET', 'PHE', 'PHY', 'RES', 'RUS', 'SBP', 'SEN', 'SES', 'SNT', 'SPA', 'STA', 'STI', 'TDW', 'TEB', 'TEK', 'TEL', 'TER', 'TES', 'THO', 'TRZ', 'TUR', 'UCK', 'ULP', 'UZB', 'YTO']

        for major_code in major_codes:
            refresher = ITUschedulerRefresher(session=session, major_codes=[major_code])
            refresher.run()
