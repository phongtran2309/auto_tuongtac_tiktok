import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Thông tin cấu hình
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '1I0MW2BaP8h7nCmuL7KGuIIb_UJU_JXCGjW_BtD_DqH0'  # Thay bằng ID thật

def get_date_sheet_names():
    sheet_names = []
    start_date = datetime(2025, 4, 10)  # Tháng 3 là 3, không cần trừ 1 trong Python
    today = datetime.today()
    d = start_date

    while d <= today:
        sheet_names.append(f"{d.day}/{d.month}")
        d += timedelta(days=1)

    return sheet_names
SHEET_NAMES = get_date_sheet_names();

# Tạo kết nối với Google Sheets API
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=creds)

# Tạo folder tổng
root_folder = 'tong_acc'
os.makedirs(root_folder, exist_ok=True)

for sheet_name in SHEET_NAMES:
    try:
        # Lấy dữ liệu cột A (email) và F (người gửi)
        range_str = f"{sheet_name}!A2:F"
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_str
        ).execute()

        values = result.get('values', [])
        if not values:
            continue

        # Gom email theo từng người gửi
        sender_map = {}
        for row in values:
            email = row[0].strip() if len(row) > 0 else ''
            sender = row[5].strip() if len(row) > 5 else ''

            if sender and email:
                sender_map.setdefault(sender, []).append(email)

        # Lưu email vào từng folder tương ứng người gửi
        for sender, emails in sender_map.items():
            sender_folder = os.path.join(root_folder, sender)
            os.makedirs(sender_folder, exist_ok=True)

            # Thay dấu '/' bằng dấu '-'
            safe_sheet_name = sheet_name.replace('/', '-')
            filename = os.path.join(sender_folder, f"{safe_sheet_name}.txt")

            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(emails))

        print(f"✅ Đã xử lý sheet: {sheet_name}")

    except Exception as e:
        print(f"❌ Lỗi sheet {sheet_name}: {e}")

print("🎉 Hoàn tất.")
