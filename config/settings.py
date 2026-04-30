import os
import yaml

class Settings:
    def __init__(self, config_file="config.yaml"):
        self.config_file = config_file
        self.settings = self.load_config()
    
    def load_config(self):
        """加载配置文件，如果不存在则创建默认配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"[!] 配置文件加载失败: {e}")
                return {}
        else:
            self.create_default_config()
            return {}
    
    def create_default_config(self):
        """创建默认配置文件"""
        default_config = {
            "ai": {
                "engine": "doubao",
                "openai_model": "gpt-4",
                "qwen_model": "qwen-turbo",
                "zhipu_model": "glm-4",
                "ollama_model": "llama3"
            },
            "scan": {
                "default_ports": "22,80,443,8080,3306,5432,8443,6379,27017",
                "scan_timeout": 60
            }
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
            print(f"[+] 已创建默认配置文件: {self.config_file}")
        except Exception as e:
            print(f"[!] 创建配置文件失败: {e}")
