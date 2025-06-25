from flask import Flask, render_template, request, jsonify
import os
import datetime
import markdown
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = 'static/uploads'
MARKDOWN_FOLDER = 'content/posts'  # Hugo博客的文章目录

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MARKDOWN_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """渲染博客发布页面"""
    return render_template('index.html')

@app.route('/save-article', methods=['POST'])
def save_article():
    """保存博客文章为Markdown文件"""
    try:
        data = request.json
        filename = secure_filename(data['filename'])
        content = data['content']
        
        # 保存Markdown文件
        filepath = os.path.join(MARKDOWN_FOLDER, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            'success': True,
            'message': f'文章已成功保存到 {filepath}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/preview-markdown', methods=['POST'])
def preview_markdown():
    """预览Markdown内容"""
    try:
        content = request.json.get('content', '')
        html = markdown.markdown(content)
        return jsonify({
            'success': True,
            'html': html
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)    