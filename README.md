# 🛍️ Shopify Store URL Checker

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/thredeisacoder/Shopify-Store-Url-Checker.svg)](https://github.com/thredeisacoder/Shopify-Store-Url-Checker/stargazers)

> 🔍 **Powerful web application to detect Shopify stores with intelligent analysis and batch processing capabilities**

A modern, responsive web application built with Flask that analyzes websites to determine if they are Shopify stores. Features both single URL checking and unlimited batch processing with real-time progress tracking.

## ✨ Features

### 🎯 Core Functionality
- **🔍 Single URL Check**: Quick analysis of individual websites
- **📋 Batch Processing**: Unlimited bulk URL checking with no restrictions
- **⚡ Real-time Progress**: Live progress bar and current URL tracking
- **📊 Detailed Analysis**: Confidence scoring and detection reasoning
- **🎨 Modern UI**: Beautiful gradient design with responsive layout

### 🔍 Detection Methods
- **🌐 Domain Analysis**: Detects `myshopify.com` subdomains
- **📡 Server Headers**: Analyzes `Server` and `X-Powered-By` headers
- **🏷️ Meta Tags**: Checks for Shopify generator meta tags
- **📦 Resource Detection**: Identifies Shopify CDN assets and scripts
- **🔧 API Signatures**: Recognizes Shopify-specific JavaScript patterns

### 📈 Advanced Features  
- **📝 Detailed Logging**: Console output with processing status
- **🚫 No Limits**: Process unlimited URLs in batch mode
- **⏱️ Background Processing**: Non-blocking batch operations
- **🔄 Auto-categorization**: Separates Shopify/Non-Shopify/Error results
- **📱 Mobile Responsive**: Works perfectly on all devices

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** 
- **pip** package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/thredeisacoder/Shopify-Store-Url-Checker.git
cd Shopify-Store-Url-Checker
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser** and visit: http://localhost:5000

## 🎮 Usage

### Single URL Check
1. Navigate to the **"Kiểm tra đơn lẻ"** tab
2. Enter a website URL (e.g., `shop.tesla.com`)
3. Click **"Kiểm tra"** or press Enter
4. View detailed results with confidence score

### Batch Processing  
1. Switch to **"Kiểm tra hàng loạt"** tab
2. Paste URLs (one per line) - **no limit!**
3. Click **"Kiểm tra hàng loạt"**
4. Watch real-time progress with current URL display
5. Review categorized results

### Sample URLs for Testing

**✅ Shopify Stores:**
```
shop.tesla.com
shop.kylie.com  
shop.gymshark.com
shopify.com
allbirds.com
```

**❌ Non-Shopify Sites:**
```
amazon.com
ebay.com
walmart.com
target.com
google.com
```

## 🏗️ Project Structure

```
Shopify-Store-Url-Checker/
│
├── app.py                 # Flask application & detection logic
├── requirements.txt       # Python dependencies  
├── README.md             # Project documentation
├── LICENSE               # MIT license
└── templates/
    └── index.html        # Frontend interface & JavaScript
```

## 🔧 Technical Details

### Backend (Python Flask)
- **Multi-threaded processing** for batch operations
- **UUID-based session tracking** for progress monitoring  
- **Comprehensive error handling** with detailed logging
- **RESTful API endpoints** for frontend communication

### Frontend (HTML/CSS/JavaScript)
- **Responsive design** with CSS Grid and Flexbox
- **Real-time progress updates** via polling
- **Modern UI components** with smooth animations
- **Tab-based navigation** for different modes

### Detection Algorithm
The application uses a **5-factor analysis system**:

1. **Domain Check** → `myshopify.com` presence
2. **Server Headers** → Shopify signatures  
3. **Meta Generator** → Shopify meta tags
4. **CDN Resources** → `cdn.shopify.com` assets
5. **JavaScript APIs** → Shopify-specific objects

**Confidence Score** = (Detected Factors / Total Factors) × 100%

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application interface |
| `/check` | POST | Single URL analysis |
| `/check-batch` | POST | Start batch processing |
| `/batch-progress/<id>` | GET | Get batch progress status |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)  
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Changelog

### v1.0.0 (Current)
- ✅ Single URL checking with detailed analysis
- ✅ Unlimited batch processing 
- ✅ Real-time progress tracking
- ✅ Modern responsive UI
- ✅ Comprehensive logging system

## 🐛 Troubleshooting

### Common Issues

**PowerShell Execution Policy Error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Port Already in Use:**
```python
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Connection Errors:**
- Check internet connectivity
- Verify firewall/antivirus settings  
- Try different URLs to isolate issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**thredeisacoder**
- GitHub: [@thredeisacoder](https://github.com/thredeisacoder)
- Repository: [Shopify-Store-Url-Checker](https://github.com/thredeisacoder/Shopify-Store-Url-Checker)

## ⭐ Support

If you find this project helpful, please give it a ⭐ on [GitHub](https://github.com/thredeisacoder/Shopify-Store-Url-Checker)!

---

<div align="center">
  <strong>🛍️ Built with ❤️ for the e-commerce community</strong>
</div> 