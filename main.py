from fastapi import FastAPI, HTTPException
import httpx
from datetime import datetime

app = FastAPI()

# Hàm chuyển đổi Unix timestamp thành chuỗi ngày tháng năm
def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Định nghĩa endpoint để lấy dữ liệu từ API tỷ giá hối đoái
@app.get("/data")
async def get_exchange_rates():
    try:
        # Lấy thời gian hiện tại
        current_time = datetime.utcnow().strftime('%Y-%m-%d')
        
        # Gửi yêu cầu GET đến API tỷ giá hối đoái
        response = httpx.get("https://api.exchangerate-api.com/v4/latest/USD")
        # Kiểm tra xem yêu cầu có thành công không
        if response.status_code == 200:
            # Lấy dữ liệu JSON từ phản hồi của API tỷ giá hối đoái
            data = response.json()
            # Trích xuất tỷ giá của VND từ khóa "VND"
            vnd_rate = data["rates"]["VND"]
            # Trích xuất thời gian cập nhật và định dạng lại
            time_last_updated = format_timestamp(data["time_last_updated"])
            # Trích xuất 15 giá trị đầu tiên từ từ khóa "rates"
            first_15_rates = {currency: rate for currency, rate in list(data["rates"].items())[:15]}
            # Thêm tỷ giá của VND vào từ khóa "rates"
            first_15_rates["VND"] = vnd_rate
            return {"current_time": current_time, "time_last_updated": time_last_updated, "rates": first_15_rates}
        else:
            # Nếu yêu cầu không thành công, ném ra một HTTPException với mã lỗi tương ứng
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch exchange rates")
    except Exception as e:
        # Xử lý các lỗi khác có thể xảy ra, ví dụ như lỗi mạng
        raise HTTPException(status_code=500, detail=str(e))

# Nếu chạy script này trực tiếp, khởi động máy chủ FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
