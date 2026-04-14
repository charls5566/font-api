from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

# 字体文件路径
FONT_DIR = os.path.join(os.path.dirname(__file__), '..')

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "ok",
        "message": "字体渲染API已启动",
        "fonts": ["滴滴活力黑-Regular.otf", "滴滴活力黑-italic.otf"],
        "usage": "POST /api/render 传入 {\"text\": \"文字\", \"font\": \"滴滴活力黑-Regular.otf\"}"
    })

@app.route('/api/render', methods=['POST'])
def render():
    try:
        data = request.get_json()
        text = data.get('text', '测试')
        font_name = data.get('font', '滴滴活力黑-Regular.otf')
        
        # 字体文件路径
        font_path = os.path.join(FONT_DIR, font_name)
        
        # 检查字体是否存在
        if not os.path.exists(font_path):
            return jsonify({"error": f"字体文件不存在: {font_name}"}), 400
        
        # 加载字体
        font = ImageFont.truetype(font_path, 48)
        
        # 计算文字大小
        img = Image.new('RGB', (1, 1), color='white')
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 创建合适大小的图片
        img = Image.new('RGB', (text_width + 40, text_height + 40), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), text, font=font, fill='black')
        
        # 转为字节流
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
