#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import html

def convert_furigana_to_html(text_file_path, output_file_path):
    """
    Convert Japanese text with furigana in parentheses to HTML with ruby tags
    """
    
    # Read the input file
    with open(text_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # First, handle line breaks in furigana patterns
    # Replace patterns like 思\n（おも）いますか？ with 思（おも）いますか？
    content = re.sub(r'([一-龯々])\n[（(]([ぁ-んァ-ン\s]+)[）)]', r'\1（\2）', content)
    
    # Pattern to match kanji followed by furigana in parentheses
    # Handles both full-width（） and half-width () parentheses
    # Only matches if parentheses contain hiragana/katakana
    pattern = r'([一-龯々]+)[（(]([ぁ-んァ-ン\s]+)[）)]'
    
    # Replace with ruby tags
    def replace_with_ruby(match):
        kanji = match.group(1)
        furigana = match.group(2)
        return f'<ruby>{kanji}<rt>{furigana}</rt></ruby>'
    
    # Apply the conversion multiple times to catch overlapping patterns
    for _ in range(3):
        html_content = re.sub(pattern, replace_with_ruby, content)
        if html_content == content:
            break
        content = html_content
    
    # Make Korean words bold
    # Pattern 1: Korean after "단어：" or "단어・" (e.g., "단어：気になる 궁금하다")
    html_content = re.sub(r'(단어[：・][^\s]+\s+)([가-힣]+)', r'\1<strong class="korean-bold">\2</strong>', html_content)
    
    # Pattern 2: Korean after "—" (e.g., "主人公 — 주인공")
    html_content = re.sub(r'(—\s*)([가-힣]+)', r'\1<strong class="korean-bold">\2</strong>', html_content)
    
    # Pattern 3: Korean after "👉" (e.g., "👉 이 케이크 달아 보여요.")
    html_content = re.sub(r'(👉\s*)([가-힣][^\n]+)', r'\1<strong class="korean-bold">\2</strong>', html_content)
    
    # Escape HTML entities for the rest of the content
    # But first, protect our ruby tags and bold tags
    ruby_pattern = r'<ruby>.*?</rt></ruby>'
    ruby_matches = re.findall(ruby_pattern, html_content, re.DOTALL)
    
    bold_pattern = r'<strong class="korean-bold">.*?</strong>'
    bold_matches = re.findall(bold_pattern, html_content, re.DOTALL)
    
    # Replace ruby tags with placeholders
    placeholders = []
    for i, match in enumerate(ruby_matches):
        placeholder = f'__RUBY_PLACEHOLDER_{i}__'
        placeholders.append((placeholder, match))
        html_content = html_content.replace(match, placeholder, 1)
    
    # Replace bold tags with placeholders
    for i, match in enumerate(bold_matches):
        placeholder = f'__BOLD_PLACEHOLDER_{i}__'
        placeholders.append((placeholder, match))
        html_content = html_content.replace(match, placeholder, 1)
    
    # Escape HTML
    html_content = html.escape(html_content)
    
    # Restore ruby tags and bold tags
    for placeholder, tag in placeholders:
        html_content = html_content.replace(placeholder, tag)
    
    # Create HTML document with improved design
    html_doc = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>俺物語１話 - 내이야기 1 화</title>
    <style>
        body {{
            font-family: "Yu Mincho", "Hiragino Mincho ProN", "MS Mincho", serif;
            line-height: 2.8;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px;
            background-color: #fefefe;
            font-size: 18px;
        }}
        
        .title {{
            font-size: 36px;
            text-align: center;
            margin-bottom: 10px;
            color: #2c3e50;
            font-weight: bold;
        }}
        
        .subtitle {{
            font-size: 28px;
            text-align: center;
            margin-bottom: 30px;
            color: #34495e;
        }}
        
        .cover-image {{
            display: block;
            margin: 0 auto 40px auto;
            max-width: 400px;
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        ruby {{
            ruby-align: center;
        }}
        
        rt {{
            font-size: 0.5em;
            color: #e74c3c;
            font-weight: normal;
            font-family: "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
        }}
        
        .content-section {{
            margin-bottom: 40px;
            padding: 30px;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }}
        
        .expression-box {{
            background-color: #ecf0f1;
            padding: 20px;
            border-left: 5px solid #3498db;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .example-box {{
            background-color: #f8f9fa;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }}
        
        .korean-bold {{
            font-weight: bold;
            color: #27ae60;
            font-family: "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
        }}
        
        .number {{
            font-weight: bold;
            color: #e67e22;
            font-size: 20px;
        }}
        
        .emoji {{
            font-size: 20px;
            vertical-align: middle;
        }}
        
        p {{
            margin-bottom: 15px;
        }}
        
        @media print {{
            body {{
                font-size: 16px;
                background-color: white;
                padding: 20px;
            }}
            .content-section {{
                box-shadow: none;
                border: 1px solid #ddd;
                page-break-inside: avoid;
            }}
            .cover-image {{
                max-width: 300px;
            }}
        }}
    </style>
</head>
<body>
    <h1 class="title">俺物語１話</h1>
    <h2 class="subtitle">내이야기 1 화</h2>
    <img src="cover.png" alt="Cover Image" class="cover-image">
    
    <div class="content-section">
        <pre style="white-space: pre-wrap; font-family: inherit; font-size: inherit;">{html_content}</pre>
    </div>
</body>
</html>'''
    
    # Write the output file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_doc)
    
    print(f"Conversion complete! HTML saved to: {output_file_path}")

if __name__ == "__main__":
    input_file = "b1.txt"
    output_file = "b1_furigana.html"
    convert_furigana_to_html(input_file, output_file)
