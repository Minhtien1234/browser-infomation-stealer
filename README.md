# Stealer Bot - MTTOOL2025 / Bot Đánh Cắp Thông Tin - MTTOOL2025

![Discord](https://img.shields.io/badge/Discord-Bot-blue?logo=discord)
![Python](https://img.shields.io/badge/Python-3.8%2B-green?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![Language](https://img.shields.io/badge/English-Vietnamese-orange)

## 📌 Description / Mô Tả

**English**: Stealer Bot is a Discord bot designed to collect system information, browser data, and WiFi network details. The bot automatically sends information to a specified Discord channel when activated.

**Tiếng Việt**: Stealer Bot là một bot Discord được thiết kế để thu thập thông tin hệ thống, dữ liệu trình duyệt và thông tin mạng WiFi. Bot tự động gửi thông tin đến kênh Discord được chỉ định khi được kích hoạt.

## ⚡ Features / Tính Năng

### 🔍 System Information Collection / Thu Thập Thông Tin Hệ Thống
- **PC Information**: Username, Hostname, Model, OS, Product Key
- **Hardware**: CPU, GPU, RAM, Screen Resolution
- **Network**: IP, Country, Proxy, MAC Address, UUID
- **Security**: List of active antivirus software

**Tiếng Việt**:
- **Thông tin PC**: Username, Hostname, Model, Hệ điều hành, Product Key
- **Phần cứng**: CPU, GPU, RAM, Độ phân giải màn hình
- **Mạng**: IP, Quốc gia, Proxy, MAC Address, UUID
- **Bảo mật**: Danh sách phần mềm antivirus đang hoạt động

### 🌐 Browser Data Extraction / Thu Thập Dữ Liệu Trình Duyệt
**Supported Browsers / Trình duyệt được hỗ trợ:**
- Google Chrome, Microsoft Edge, Brave
- Opera, Opera GX, Vivaldi
- Yandex, CocCoc, and many others

**Data Collected / Dữ liệu thu thập:**
- 🔑 Saved passwords
- 📚 Browsing history
- 🍪 Cookies
- 💳 Credit card information

**Tiếng Việt**:
- 🔑 Mật khẩu đã lưu
- 📚 Lịch sử duyệt web
- 🍪 Cookies
- 💳 Thông tin thẻ tín dụng

### 📶 WiFi Information / Thông Tin WiFi
- List of saved WiFi networks and passwords
- Router information (IP, MAC, Manufacturer)

**Tiếng Việt**:
- Danh sách mạng WiFi đã lưu và mật khẩu
- Thông tin router (IP, MAC, Nhà sản xuất)

## 🚀 Installation / Cài Đặt

### 1. System Requirements / Yêu Cầu Hệ Thống
- Windows 10/11
- Python 3.8+
- Administrator privileges (recommended)

**Tiếng Việt**:
- Windows 10/11
- Python 3.8+
- Quyền Administrator (khuyến nghị)

### 2. Install Dependencies / Cài Đặt Thư Viện
```bash
pip install discord.py pycryptodome screeninfo pycountry psutil pypiwin32 requests
```

### 3. Bot Configuration / Cấu Hình Bot
1. Create a bot on [Discord Developer Portal](https://discord.com/developers/applications)
2. Copy the token and replace it in the code file:
```python
DISCORD_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
```

**Tiếng Việt**:
1. Tạo bot trên [Discord Developer Portal](https://discord.com/developers/applications)
2. Sao chép token và thay thế trong file code:
```python
DISCORD_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
```

### 4. Bot Permissions / Cấp Quyền Cho Bot
- **View Channels**
- **Send Messages**
- **Attach Files**

**Tiếng Việt**:
- **Xem kênh**
- **Gửi tin nhắn**
- **Đính kèm tệp**

## 🎮 Usage / Sử Dụng

### Automatic Startup / Tự Động Khởi Động
When the bot is run, it will automatically:
- Send notification "stealer bot ON - MTTOOL2025" to the specified channel
- Be ready to receive commands

**Tiếng Việt**:
Khi bot được chạy, nó sẽ tự động:
- Gửi thông báo "stealer bot ON - MTTOOL2025" đến kênh được chỉ định
- Sẵn sàng nhận lệnh

### Discord Commands / Lệnh Discord
```bash
?stealer1
```

**When this command is received, the bot will:**
1. Collect all system information
2. Extract data from browsers
3. Send results as files and messages

**Tiếng Việt**:
**Khi nhận được lệnh này, bot sẽ:**
1. Thu thập toàn bộ thông tin hệ thống
2. Trích xuất dữ liệu từ trình duyệt
3. Gửi kết quả dưới dạng file và tin nhắn

## 📁 File Structure / Cấu Trúc File

```
stealer_bot.py          # Main file / File chính
requirements.txt        # Dependencies list / Danh sách thư viện
README.md              # Usage guide / Hướng dẫn sử dụng
```

## ⚠️ Important Notes / Lưu Ý Quan Trọng

### Legal / Pháp Lý
- **For educational and testing purposes only**
- Requires permission from system owner
- Comply with local privacy and security laws

**Tiếng Việt**:
- **Chỉ sử dụng cho mục đích giáo dục và kiểm thử**
- Cần có sự cho phép của chủ sở hữu hệ thống
- Tuân thủ luật pháp địa phương về bảo mật và quyền riêng tư

### Security / Bảo Mật
- Protect bot token carefully
- Use in controlled environments
- Delete sensitive data after use

**Tiếng Việt**:
- Bảo vệ token bot cẩn thận
- Sử dụng trong môi trường kiểm soát
- Xóa dữ liệu nhạy cảm sau khi sử dụng

## 🔧 Troubleshooting / Khắc Phục Sự Cố

### Common Issues / Lỗi Thường Gặp
1. **Invalid token**: Check token on Discord Developer Portal
2. **Missing permissions**: Ensure bot has sufficient channel permissions
3. **Missing libraries**: Run pip install again

**Tiếng Việt**:
1. **Token không hợp lệ**: Kiểm tra lại token trên Discord Developer Portal
2. **Thiếu quyền**: Đảm bảo bot có đủ quyền trong kênh
3. **Thư viện thiếu**: Chạy lại lệnh pip install

### Activity Check / Kiểm Tra Hoạt Động
- Bot online and displays "stealer bot ON - MTTOOL2025"
- Can use `?stealer1` command without errors

**Tiếng Việt**:
- Bot online và hiển thị "stealer bot ON - MTTOOL2025"
- Có thể sử dụng lệnh `?stealer1` mà không báo lỗi

## 📞 Support / Hỗ Trợ

**Developer**: MTTOOL2025  
**Contact**: Via Discord or support channel

**Tiếng Việt**:
**Nhà phát triển**: MTTOOL2025  
**Liên hệ**: Qua Discord hoặc kênh hỗ trợ

---

**⚠️ WARNING / CẢNH BÁO**: 
Using this tool for illegal purposes is against the law. The developer is not responsible for misuse.

**Sử dụng công cụ này cho mục đích trái phép là vi phạm pháp luật. Người phát triển không chịu trách nhiệm cho việc sử dụng sai mục đích.**

## 🔄 Version History / Lịch Sử Phiên Bản

### v1.0.0 (2025-09-28)
- Initial release / Phát hành đầu tiên
- Full system information collection / Thu thập đầy đủ thông tin hệ thống
- Multi-browser support / Hỗ trợ đa trình duyệt
- Undetect / Khó phát hiện

## 📄 License / Giấy Phép

This project is for educational purposes only. Use responsibly.

**Tiếng Việt**:
Dự án này chỉ dành cho mục đích giáo dục. Sử dụng có trách nhiệm.
