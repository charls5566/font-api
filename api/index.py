from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "ok",
        "message": "字体渲染API已启动",
        "usage": "POST /api/render 传入 {\"text\": \"文字\", \"font\": \"default.ttf\"}"
    })

@app.route('/api/render', methods=['POST'])
def render():
    try:
        data = request.get_json()
        text = data.get('text', '测试')
        
        # 创建图片
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # 使用默认字体
        font = ImageFont.load_default()
        
        # 绘制文字
        draw.text((20, 30), text, font=font, fill='black')
        
        # 转为字节流
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
