from google.oauth2 import service_account
from googleapiclient.discovery import build

# Khai báo thông tin kết nối
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # File JSON dịch vụ
SPREADSHEET_ID = '119uL0dOa-yhrLkgTnoPzLUGZNoHkTRpvg9plRuTxWYU' # Ví dụ: '1abcDEFghi...'

# Load credentials và khởi tạo service
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=creds)

# Mở sheet và lấy dữ liệu cột A
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Account-embedded!A2:A').execute()
values = result.get('values', [])

# Đọc danh sách email lỗi
with open('acc_loi.txt', 'r') as f:
    acc_loi = set(line.strip() for line in f if line.strip())

# Chuẩn bị các ô cần update
updates = []
for i, row in enumerate(values):
    if row and row[0].strip() in acc_loi:
        updates.append({
            "range": f"Account-embedded!D{i+2}",  # Dòng tương ứng
            "values": [["fail"]]
        })

# Gửi dữ liệu lên nếu có update
if updates:
    body = {
        "valueInputOption": "RAW",
        "data": updates
    }
    sheet.values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print("✅ Đã cập nhật xong trạng thái fail.")
else:
    print("✅ Không có email nào cần cập nhật.")
