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
        lines = f.readlines()
    
    # Parse content into sections
    html_sections = []
    current_section = []
    section_type = None
    
    for line in lines:
        line = line.rstrip('\n')
        
        # Skip the first two lines (title and subtitle - handled separately)
        if not html_sections and not current_section:
            if line.strip() in ['俺物語１話', '내이야기 1 화']:
                continue
        
        # Detect section headers
        if line.strip() == '줄거리':
            if current_section:
                html_sections.append(('content', current_section))
            current_section = [line]
            section_type = 'story'
        elif '🎧' in line or 'しゃどーいんぐ' in line:
            if current_section:
                html_sections.append((section_type, current_section))
            current_section = [line]
            section_type = 'shadowing'
        elif '💬フリートーク' in line:
            if current_section:
                html_sections.append((section_type, current_section))
            current_section = [line]
            section_type = 'freetalk'
        elif '📖 単語' in line or '단어' in line:
            if current_section:
                html_sections.append((section_type, current_section))
            current_section = [line]
            section_type = 'vocabulary'
        else:
            current_section.append(line)
    
    # Add last section
    if current_section:
        html_sections.append((section_type, current_section))
    
    # Convert each section to HTML
    html_content = ""
    
    for section_type, section_lines in html_sections:
        section_text = '\n'.join(section_lines)
        
        # First, handle line breaks in furigana patterns
        section_text = re.sub(r'([一-龯々])\n[（(]([ぁ-んァ-ン\s]+)[）)]', r'\1（\2）', section_text)
        
        # Pattern to match kanji followed by furigana in parentheses
        pattern = r'([一-龯々]+)[（(]([ぁ-んァ-ン\s]+)[）)]'
        
        def replace_with_ruby(match):
            kanji = match.group(1)
            furigana = match.group(2)
            return f'<ruby>{kanji}<rt>{furigana}</rt></ruby>'
        
        # Apply the conversion multiple times
        for _ in range(3):
            new_text = re.sub(pattern, replace_with_ruby, section_text)
            if new_text == section_text:
                break
            section_text = new_text
        
        # Make Korean text bold (text after 👉 or standalone Korean lines)
        # Pattern for lines starting with 👉 followed by Korean
        section_text = re.sub(r'(👉\s*)([가-힣\s]+[가-힣][^\n]*)', r'\1<strong class="korean-bold">\2</strong>', section_text)
        
        # Pattern for standalone Korean lines (not starting with symbols)
        section_text = re.sub(r'^([가-힣][가-힣\s.,!?]+)$', r'<strong class="korean-bold">\1</strong>', section_text, flags=re.MULTILINE)
        
        # Pattern for Korean after "단어" or vocabulary items
        section_text = re.sub(r'(—\s*)([가-힣\s]+)', r'\1<strong class="korean-bold">\2</strong>', section_text)
        
        # Escape HTML for the section
        section_html = html.escape(section_text)
        
        # Restore ruby tags and bold tags
        section_html = section_html.replace('&lt;ruby&gt;', '<ruby>')
        section_html = section_html.replace('&lt;/ruby&gt;', '</ruby>')
        section_html = section_html.replace('&lt;rt&gt;', '<rt>')
        section_html = section_html.replace('&lt;/rt&gt;', '</rt>')
        section_html = section_html.replace('&lt;strong class=&quot;korean-bold&quot;&gt;', '<strong class="korean-bold">')
        section_html = section_html.replace('&lt;/strong&gt;', '</strong>')
        
        # Wrap in appropriate section div
        if section_type == 'story':
            html_content += f'<div class="section-box story-section">\n<h2 class="section-header">📖 줄거리</h2>\n<pre class="section-content">{section_html}</pre>\n</div>\n\n'
        elif section_type == 'shadowing':
            html_content += f'<div class="section-box shadowing-section">\n<h2 class="section-header">🎧 しゃどーいんぐ表現</h2>\n<pre class="section-content">{section_html}</pre>\n</div>\n\n'
        elif section_type == 'freetalk':
            html_content += f'<div class="section-box freetalk-section">\n<h2 class="section-header">💬 フリートーク</h2>\n<pre class="section-content">{section_html}</pre>\n</div>\n\n'
        elif section_type == 'vocabulary':
            html_content += f'<div class="section-box vocabulary-section">\n<h2 class="section-header">📖 単語</h2>\n<pre class="section-content">{section_html}</pre>\n</div>\n\n'
        else:
            html_content += f'<div class="section-box">\n<pre class="section-content">{section_html}</pre>\n</div>\n\n'
    
    # Create HTML document with improved design
    html_doc = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>俺物語１話 - 내이야기 1 화</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: "Yu Mincho", "Hiragino Mincho ProN", "MS Mincho", serif;
            line-height: 2.2;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
            background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
            font-size: 18px;
            color: #2c3e50;
        }}
        
        .title {{
            font-size: 42px;
            text-align: center;
            margin-bottom: 15px;
            color: #2c3e50;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        
        .subtitle {{
            font-size: 30px;
            text-align: center;
            margin-bottom: 35px;
            color: #34495e;
            font-weight: 500;
        }}
        
        .cover-image {{
            display: block;
            margin: 0 auto 50px auto;
            max-width: 450px;
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            transition: transform 0.3s ease;
        }}
        
        .cover-image:hover {{
            transform: scale(1.02);
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
        
        .section-box {{
            margin-bottom: 50px;
            padding: 35px;
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border-left: 6px solid #3498db;
        }}
        
        .story-section {{
            border-left-color: #9b59b6;
        }}
        
        .shadowing-section {{
            border-left-color: #3498db;
        }}
        
        .freetalk-section {{
            border-left-color: #e67e22;
        }}
        
        .vocabulary-section {{
            border-left-color: #27ae60;
        }}
        
        .section-header {{
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #ecf0f1;
        }}
        
        .section-content {{
            white-space: pre-wrap;
            font-family: inherit;
            font-size: inherit;
            line-height: 2.5;
        }}
        
        .korean-bold {{
            font-weight: bold;
            color: #27ae60;
            font-family: "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
        }}
        
        .emoji {{
            font-size: 22px;
            vertical-align: middle;
        }}
        
        @media print {{
            body {{
                font-size: 16px;
                background: white;
                padding: 20px;
            }}
            
            .section-box {{
                box-shadow: none;
                border: 1px solid #ddd;
                page-break-inside: avoid;
                margin-bottom: 30px;
                padding: 25px;
            }}
            
            .cover-image {{
                max-width: 350px;
            }}
            
            .section-content {{
                line-height: 2.2;
            }}
        }}
        
        @media (max-width: 768px) {{
            body {{
                font-size: 16px;
                padding: 20px 15px;
            }}
            
            .title {{
                font-size: 32px;
            }}
            
            .subtitle {{
                font-size: 24px;
            }}
            
            .section-box {{
                padding: 25px 20px;
            }}
            
            .section-header {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <h1 class="title">俺物語１話</h1>
    <h2 class="subtitle">내이야기 1 화</h2>
    <img src="cover.png" alt="Cover Image" class="cover-image">
    
    {html_content}
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
