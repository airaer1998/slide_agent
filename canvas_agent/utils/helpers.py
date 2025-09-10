"""
Canvas Agent 辅助工具函数

包含各种实用工具函数
"""

import json
import os
import re
from typing import List, Dict, Any, Optional
from ..config import Config


def validate_slide_count(count: int) -> bool:
    """验证幻灯片页数是否有效"""
    return Config.MIN_SLIDE_COUNT <= count <= Config.MAX_SLIDE_COUNT


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    # 移除或替换非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 移除多余的空格和点
    filename = re.sub(r'\s+', '_', filename.strip())
    filename = filename.strip('.')
    
    return filename or "untitled"


def ensure_file_extension(filename: str, extension: str) -> str:
    """确保文件有指定的扩展名"""
    if not extension.startswith('.'):
        extension = '.' + extension
    
    if not filename.endswith(extension):
        filename += extension
    
    return filename


def save_json_safely(data: Any, filepath: str, backup: bool = True) -> bool:
    """安全地保存JSON文件"""
    try:
        # 如果需要备份且文件存在
        if backup and os.path.exists(filepath):
            backup_path = filepath + '.backup'
            with open(filepath, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
        
        # 保存新文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"[Error]: 保存JSON文件失败: {e}")
        return False


def load_json_safely(filepath: str, default: Any = None) -> Any:
    """安全地加载JSON文件"""
    try:
        if not os.path.exists(filepath):
            return default
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Error]: 加载JSON文件失败: {e}")
        return default


def extract_keywords_from_text(text: str, min_length: int = 3) -> List[str]:
    """从文本中提取关键词"""
    # 简单的关键词提取
    words = re.findall(r'\b\w+\b', text.lower())
    
    # 过滤短词和常见停用词
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may',
        'might', 'must', 'shall', 'a', 'an', 'this', 'that', 'these', 'those'
    }
    
    keywords = [word for word in words 
               if len(word) >= min_length and word not in stop_words]
    
    # 返回前10个关键词
    return list(set(keywords))[:10]


def format_slide_title(title: str, page_number: int) -> str:
    """格式化幻灯片标题"""
    if not title:
        return f"第{page_number}页"
    
    # 移除多余的空格和特殊字符
    title = re.sub(r'\s+', ' ', title.strip())
    
    # 如果标题太长，截断
    if len(title) > 50:
        title = title[:47] + "..."
    
    return title


def estimate_content_length(outline: List[Dict[str, Any]]) -> Dict[str, int]:
    """估算内容长度"""
    total_points = sum(len(slide.get('key_points', [])) for slide in outline)
    
    # 简单的长度估算
    estimated_chars = total_points * 100  # 每个要点大约100字符
    estimated_words = estimated_chars // 5  # 平均每个词5个字符
    
    return {
        "total_slides": len(outline),
        "total_points": total_points,
        "estimated_characters": estimated_chars,
        "estimated_words": estimated_words
    }


def validate_outline_structure(outline: List[Dict[str, Any]]) -> List[str]:
    """验证大纲结构，返回错误列表"""
    errors = []
    
    if not outline:
        errors.append("大纲不能为空")
        return errors
    
    for i, slide in enumerate(outline):
        slide_num = i + 1
        
        # 检查必需字段
        if 'page' not in slide:
            errors.append(f"第{slide_num}页缺少page字段")
        elif slide['page'] != slide_num:
            errors.append(f"第{slide_num}页的page字段值不正确")
        
        if 'title' not in slide:
            errors.append(f"第{slide_num}页缺少title字段")
        elif not slide['title'].strip():
            errors.append(f"第{slide_num}页的标题为空")
        
        if 'type' not in slide:
            errors.append(f"第{slide_num}页缺少type字段")
        
        if 'key_points' not in slide:
            errors.append(f"第{slide_num}页缺少key_points字段")
        elif not isinstance(slide['key_points'], list):
            errors.append(f"第{slide_num}页的key_points应该是列表")
        elif not slide['key_points']:
            errors.append(f"第{slide_num}页的key_points为空")
    
    return errors


def clean_markdown_content(content: str) -> str:
    """清理Markdown内容"""
    # 移除多余的空行
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # 移除行尾空格
    content = re.sub(r' +$', '', content, flags=re.MULTILINE)
    
    # 确保文件以换行符结尾
    if content and not content.endswith('\n'):
        content += '\n'
    
    return content


def create_backup_filename(original_path: str) -> str:
    """创建备份文件名"""
    import datetime
    
    base, ext = os.path.splitext(original_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"{base}_backup_{timestamp}{ext}"


def check_moffee_available() -> bool:
    """检查moffee是否可用"""
    try:
        import subprocess
        import os
        env = os.environ.copy()
        env['PYTHONPATH'] = '/root/code/slide_agent/moffee'
        result = subprocess.run(['moffee', '--version'], 
                              capture_output=True, text=True, timeout=5, env=env)
        return result.returncode == 0
    except Exception:
        return False