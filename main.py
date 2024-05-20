from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Định nghĩa endpoint để lấy dữ liệu từ API tỷ giá hối đoái
@app.get("/data")
async def get_exchange_rates():
    try:
        # Gửi yêu cầu GET đến API tỷ giá hối đoái
        response = httpx.get("https://api.exchangerate-api.com/v4/latest/USD")
        # Kiểm tra xem yêu cầu có thành công không
        if response.status_code == 200:
            # Trả về dữ liệu JSON từ phản hồi của API tỷ giá hối đoái
            return response.json()
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
