from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import urlparse
import re
import time
import threading
import uuid

app = Flask(__name__)

# Lưu trữ progress của các batch check
batch_progress = {}

def is_shopify_store(url):
    """
    Kiểm tra xem URL có phải là Shopify store hay không
    """
    try:
        # Chuẩn hóa URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Thực hiện request với timeout
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        # Các dấu hiệu nhận biết Shopify
        shopify_indicators = {
            'domain': False,
            'headers': False,
            'meta_tags': False,
            'scripts': False,
            'powered_by': False
        }
        
        reasons = []
        
        # 1. Kiểm tra domain
        parsed_url = urlparse(response.url)
        domain = parsed_url.netloc.lower()
        if 'myshopify.com' in domain:
            shopify_indicators['domain'] = True
            reasons.append("Domain chứa 'myshopify.com'")
        
        # 2. Kiểm tra headers
        server_header = response.headers.get('Server', '').lower()
        if 'shopify' in server_header:
            shopify_indicators['headers'] = True
            reasons.append("Server header chứa 'Shopify'")
        
        powered_by = response.headers.get('X-Powered-By', '').lower()
        if 'shopify' in powered_by:
            shopify_indicators['powered_by'] = True
            reasons.append("X-Powered-By header chứa 'Shopify'")
        
        # 3. Kiểm tra nội dung HTML
        html_content = response.text.lower()
        
        # Kiểm tra meta tags
        shopify_meta_patterns = [
            r'<meta[^>]*name=["\']generator["\'][^>]*content=["\'][^"\']*shopify[^"\']*["\'][^>]*>',
            r'<meta[^>]*content=["\'][^"\']*shopify[^"\']*["\'][^>]*name=["\']generator["\'][^>]*>'
        ]
        
        for pattern in shopify_meta_patterns:
            if re.search(pattern, html_content):
                shopify_indicators['meta_tags'] = True
                reasons.append("Meta tag generator chứa 'Shopify'")
                break
        
        # Kiểm tra scripts và CSS của Shopify
        shopify_script_patterns = [
            r'cdn\.shopify\.com',
            r'shopify\.s\.js',
            r'shopifycdn\.com',
            r'shopify-features',
            r'shopify\.theme',
            r'shopify\.payment',
            r'window\.shopify',
            r'shopify\.analytics'
        ]
        
        for pattern in shopify_script_patterns:
            if re.search(pattern, html_content):
                shopify_indicators['scripts'] = True
                reasons.append(f"Tìm thấy script/resource Shopify: {pattern}")
                break
        
        # Tính toán kết quả
        is_shopify = any(shopify_indicators.values())
        confidence = sum(shopify_indicators.values()) / len(shopify_indicators) * 100
        
        return {
            'is_shopify': is_shopify,
            'confidence': round(confidence, 1),
            'indicators': shopify_indicators,
            'reasons': reasons,
            'final_url': response.url,
            'status_code': response.status_code
        }
        
    except requests.exceptions.Timeout:
        return {
            'error': 'Timeout - Website không phản hồi trong thời gian cho phép',
            'is_shopify': False
        }
    except requests.exceptions.RequestException as e:
        return {
            'error': f'Lỗi kết nối: {str(e)}',
            'is_shopify': False
        }
    except Exception as e:
        return {
            'error': f'Lỗi không xác định: {str(e)}',
            'is_shopify': False
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'Vui lòng nhập URL'})
    
    result = is_shopify_store(url)
    return jsonify(result)

def process_batch_urls(batch_id, urls):
    """Xử lý batch URLs trong background thread"""
    results = []
    non_shopify_urls = []
    shopify_urls = []
    errors = []
    
    batch_progress[batch_id] = {
        'current': 0,
        'total': len(urls),
        'completed': False,
        'current_url': '',
        'results': {
            'results': results,
            'non_shopify_urls': non_shopify_urls,
            'shopify_urls': shopify_urls,
            'errors': errors,
            'summary': {}
        }
    }
    
    for i, url in enumerate(urls, 1):
        batch_progress[batch_id]['current'] = i
        batch_progress[batch_id]['current_url'] = url
        
        try:
            print(f"[{i}/{len(urls)}] Đang kiểm tra: {url}")
            result = is_shopify_store(url)
            result['original_url'] = url
            result['index'] = i
            
            if result.get('error'):
                errors.append(result)
                print(f"[{i}/{len(urls)}] ❌ Lỗi: {url} - {result.get('error')}")
            elif result.get('is_shopify'):
                shopify_urls.append(result)
                print(f"[{i}/{len(urls)}] ✅ Shopify: {url} ({result.get('confidence', 0)}%)")
            else:
                non_shopify_urls.append(result)
                print(f"[{i}/{len(urls)}] ❌ Không phải Shopify: {url}")
                
            results.append(result)
            
        except Exception as e:
            error_result = {
                'original_url': url,
                'index': i,
                'error': f'Lỗi không xác định: {str(e)}',
                'is_shopify': False
            }
            errors.append(error_result)
            results.append(error_result)
            print(f"[{i}/{len(urls)}] ❌ Exception: {url} - {str(e)}")
    
    # Cập nhật kết quả cuối cùng
    summary = {
        'total': len(urls),
        'shopify_count': len(shopify_urls),
        'non_shopify_count': len(non_shopify_urls),
        'error_count': len(errors)
    }
    
    batch_progress[batch_id]['completed'] = True
    batch_progress[batch_id]['results'] = {
        'results': results,
        'non_shopify_urls': non_shopify_urls,
        'shopify_urls': shopify_urls,
        'errors': errors,
        'summary': summary
    }
    
    print(f"✅ Hoàn thành batch {batch_id}: {len(urls)} URLs")

@app.route('/check-batch', methods=['POST'])
def check_batch_urls():
    data = request.get_json()
    urls_text = data.get('urls', '').strip()
    
    if not urls_text:
        return jsonify({'error': 'Vui lòng nhập danh sách URLs'})
    
    # Tách URLs từ text, loại bỏ dòng trống
    urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
    
    if not urls:
        return jsonify({'error': 'Không tìm thấy URL hợp lệ'})
    
    # Tạo batch ID và bắt đầu xử lý trong background
    batch_id = str(uuid.uuid4())
    thread = threading.Thread(target=process_batch_urls, args=(batch_id, urls))
    thread.daemon = True
    thread.start()
    
    return jsonify({'batch_id': batch_id, 'total': len(urls)})

@app.route('/batch-progress/<batch_id>')
def get_batch_progress(batch_id):
    if batch_id not in batch_progress:
        return jsonify({'error': 'Batch không tồn tại'}), 404
    
    progress = batch_progress[batch_id]
    return jsonify({
        'current': progress['current'],
        'total': progress['total'],
        'completed': progress['completed'],
        'current_url': progress['current_url'],
        'percentage': round((progress['current'] / progress['total']) * 100, 1) if progress['total'] > 0 else 0,
        'results': progress['results'] if progress['completed'] else None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 