"""
Canvas Agent 配置文件

包含所有配置项和常量定义
"""

import os
from typing import Optional


class Config:
    """配置类"""
    
    # AI模型配置
    OPENAI_BASE_URL = "http://35.220.164.252:3888/v1/"
    OPENAI_API_KEY = "sk-CnqCf4NENTwZwLLQJwPuH4ZZ1uIGIRJSyTStRkSXNV1Hb2Kj"
    OPENAI_MODEL = "moonshotai/kimi-k2"
    
    # 文件路径配置
    OUTLINE_FILE = "outline.json"
    PREVIEW_FILE = "slides_preview.md"
    FINAL_SLIDES_FILE = "final_slides.md"
    
    # 生成参数
    MAX_SLIDE_COUNT = 100
    MIN_SLIDE_COUNT = 1
    DEFAULT_TEMPERATURE = 0.7
    
    # Moffee配置
    DEFAULT_THEME = "custom"
    DEFAULT_LAYOUT = "content"
    
    # 工作流配置
    THREAD_ID = "canvas_workflow_1"
    
    @classmethod
    def get_openai_config(cls) -> dict:
        """获取OpenAI配置"""
        return {
            "base_url": cls.OPENAI_BASE_URL,
            "api_key": cls.OPENAI_API_KEY
        }
    
    @classmethod
    def get_model_config(cls) -> dict:
        """获取模型配置"""
        return {
            "model": cls.OPENAI_MODEL,
            "temperature": cls.DEFAULT_TEMPERATURE
        }
    
    @classmethod
    def get_moffee_frontmatter(cls, theme: Optional[str] = None, 
                              layout: Optional[str] = None,
                              aspect_ratio: Optional[str] = None) -> str:
        """获取Moffee前置配置"""
        return f"""---
theme: {theme or cls.DEFAULT_THEME}
layout: {layout or cls.DEFAULT_LAYOUT}
aspect_ratio: "{aspect_ratio or cls.DEFAULT_ASPECT_RATIO}"
---

"""


# 环境变量支持
def load_config_from_env():
    """从环境变量加载配置"""
    if os.getenv("CANVAS_OPENAI_BASE_URL"):
        Config.OPENAI_BASE_URL = os.getenv("CANVAS_OPENAI_BASE_URL")
    
    if os.getenv("CANVAS_OPENAI_API_KEY"):
        Config.OPENAI_API_KEY = os.getenv("CANVAS_OPENAI_API_KEY")
    
    if os.getenv("CANVAS_OPENAI_MODEL"):
        Config.OPENAI_MODEL = os.getenv("CANVAS_OPENAI_MODEL")


# 加载环境变量配置
load_config_from_env()