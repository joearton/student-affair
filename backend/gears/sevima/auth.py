import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
import os


load_dotenv()

sevima_url = os.getenv('SIAKADCLOUD_URL')
signin_url = os.getenv('SEVIMA_SIGNIN_URL')


class Auth:

    def __init__(self):
        self.session = requests.session()
        

    def get_value(self, name, attribute):
        login_page = self.session.get(signin_url)
        parser = bs(login_page.text, 'html.parser')
        token = parser.find(name, attribute)
        return token.get('value')

    
    def validate_gate_login(self, gate):
        gate = self.session.post(f"{sevima_url}/{gate}/login",
            data = {
                "oldpass": "",
                "newpass": "",
                "renewpass": "",
                "act": "",
                "sessdata": "",
                "kodemodul": gate,
                "koderole": "CLIEN",
                "kodeunit": "021035"
            }
        )
        

    def get_page(self, gate, path, method='GET', data={}):
        self.validate_gate_login(gate)
        if method == 'GET':
            r = self.session.get(f'{sevima_url}/{gate}/{path}')
        else:
            r = self.session.post(f'{sevima_url}/{gate}/{path}', data=data)
        return r.text
    
    
    def university_detail(self):
        data = auth.get_page('siakad', 'data_universitas/detail')
        soup = bs(data, 'html.parser')
        university_detail = {
            "Kode Unit": soup.select_one("#block-idunit .input-idunit").get_text(strip=True),
            "Nama Unit": soup.select_one("#block-namaunit .input-namaunit").get_text(strip=True),
            "Nama Unit (EN)": soup.select_one("#block-namauniten .input-namauniten").get_text(strip=True),
            "Nama Singkat": soup.select_one("#block-namasingkat .input-namasingkat").get_text(strip=True),
            "Jenis Perguruan Tinggi": soup.select_one("#block-jenis .input-jenis").get_text(strip=True),
            "Unit/Satuan Kerja": soup.select_one("#block-idsatker .input-idsatker").get_text(strip=True),
            "Periode Berdiri": soup.select_one("#block-idperiodeberdiri .input-idperiodeberdiri").get_text(strip=True),
            "No. SK Pendirian": soup.select_one("#block-skpendirian .input-skpendirian").get_text(strip=True),
            "Tanggal SK Pendirian": soup.select_one("#block-tglskpendirian .input-tglskpendirian").get_text(strip=True),
            "Rektor": soup.select_one("#nipketua_label").get_text(strip=True),
            "Wakil Rektor 1": soup.select_one("#nippembantu1_label").get_text(strip=True),
            "Wakil Rektor 2": soup.select_one("#nippembantu2_label").get_text(strip=True),
            "Wakil Rektor 3": soup.select_one("#nippembantu3_label").get_text(strip=True),
            "Wakil Rektor 4": soup.select_one("#nippembantu4_label").get_text(strip=True),
            "Lembaga Akreditasi": soup.select_one("#lembagaakreditasi_label").get_text(strip=True),
            "Peringkat Akreditasi": soup.select_one("#block-akreditasi .input-akreditasi").get_text(strip=True),
            "Nilai Akreditasi": soup.select_one("#block-nilaiakreditasi .number").get_text(strip=True),
            "No. SK Akreditasi": soup.select_one("#block-skakreditasi .input-skakreditasi").get_text(strip=True),
            "Tanggal SK Akreditasi": soup.select_one("#block-tglakreditasi .input-tglakreditasi").get_text(strip=True),
            "Tanggal Berlaku Akreditasi": soup.select_one("#block-tglberlaku .input-tglberlaku").get_text(strip=True),
            "Tanggal Berakhir Akreditasi": soup.select_one("#block-tglberakhir .input-tglberakhir").get_text(strip=True),
            "Visi": soup.select_one("#block-visi .input-visi p").get_text(strip=True),
            "Misi": [li.get_text(strip=True) for li in soup.select("#block-misi .input-misi ol li")],
            "Alamat": soup.select_one("#block-alamat .input-alamat").get_text(strip=True),
            "Telepon": soup.select_one("#block-telepon .input-telepon").get_text(strip=True),
            "Email": soup.select_one("#block-email .input-email").get_text(strip=True),
            "Website": soup.select_one("#block-website .input-website").get_text(strip=True),
            "Fax": soup.select_one("#block-fax .input-fax").get_text(strip=True),
        }
        return university_detail
    

    def faculty_detail(self):
        data = auth.get_page('siakad', 'list_fakultas')
        soup = bs(data, 'html.parser')
        rows = soup.find('tbody').find_all('tr')
        faculty_data = []
        for row in rows:
            columns = row.find_all('td')
            if columns:
                kode = columns[1].text.strip()
                nama_fakultas = columns[2].text.strip()
                nama_singkat = columns[3].text.strip()
                alamat = columns[4].text.strip() or None
                telepon = columns[5].text.strip() or None
                aktif = "Ya" if columns[6].find('i', {'class': 'fa-check'}) else "Tidak"
                
                # Append data to the list
                faculty_data.append({
                    "Kode": kode,
                    "Nama Fakultas": nama_fakultas,
                    "Nama Singkat": nama_singkat,
                    "Alamat": alamat,
                    "No. Telepon": telepon,
                    "Aktif?": aktif
                })
        return faculty_data


    def department_detail(self):
        department_data = []
        for page in [1,2,3]:
            data = auth.get_page('siakad', f'list_prodi/{page}')
            soup = bs(data, 'html.parser')
            rows = soup.find('tbody').find_all('tr')
            for row in rows:
                # Ambil semua kolom dalam baris
                cols = row.find_all('td')
                row_data = {
                    "Kode": cols[0].text.strip(),
                    "Nama Prodi": cols[1].text.strip(),
                    "Nama Singkat": cols[2].text.strip(),
                    "Ketua Prodi": cols[3].text.strip(),
                    "Fakultas": cols[4].text.strip(),
                    "Status": cols[5].text.strip(),
                    "id": cols[6],
                }
                department_data.append(row_data)
        return department_data


    def login(self, userid, password):
        auth_data = {
            'email'         : userid,
            'password'      : password,
            '_token'        : self.get_value('input', {'type': 'hidden', 'name': '_token'}),
            '__token'       : self.get_value('input', {'type': 'hidden', 'name': '__token'}),
            'client_id'     : self.get_value('input', {'type': 'hidden', 'name': 'client_id'}),
            'redirect_uri'  : self.get_value('input', {'type': 'hidden', 'name': 'redirect_uri'}),
        }
        login_page = self.session.post(signin_url, data = auth_data)
        if not login_page.url.endswith('login'):
            return auth_data
        return False


auth = Auth()
auth.login('client', '4pp4cc355')
print(auth.department_detail())
