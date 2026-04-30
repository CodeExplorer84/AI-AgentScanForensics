import requests
import json

class AIClient:
    def __init__(
        self,
        ai_type="doubao",
        openai_api_key=None,
        qwen_api_key=None,
        zhipu_api_key=None,
        doubao_api_key=None,
        ollama_base_url="http://localhost:11434/api",
        ollama_model="llama3",
        **kwargs
    ):
        self.ai_type = ai_type
        self.openai_api_key = openai_api_key
        self.qwen_api_key = qwen_api_key
        self.zhipu_api_key = zhipu_api_key
        self.doubao_api_key = doubao_api_key
        self.ollama_base_url = ollama_base_url
        self.ollama_model = ollama_model
        
        # API端点配置
        self.endpoints = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            "zhipu": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            "doubao": "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        }

    def chat(self, prompt):
        """统一的聊天接口"""
        ai_methods = {
            "openai": self._openai_chat,
            "qwen": self._qwen_chat,
            "zhipu": self._zhipu_chat,
            "doubao": self._doubao_chat,
            "ollama": self._ollama_chat
        }
        
        method = ai_methods.get(self.ai_type)
        if method:
            return method(prompt)
        else:
            return f"不支持的AI类型: {self.ai_type}，请选择 openai/qwen/zhipu/doubao/ollama"

    def _openai_chat(self, prompt):
        """OpenAI GPT 接口"""
        if not self.openai_api_key:
            return "错误：未配置OpenAI API_KEY，请设置环境变量 OPENAI_API_KEY"
        
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        
        try:
            resp = requests.post(
                self.endpoints["openai"],
                headers=headers,
                json=data,
                timeout=60
            )
            resp.raise_for_status()
            result = resp.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"OpenAI API调用失败: {str(e)}"

    def _qwen_chat(self, prompt):
        """通义千问 Qwen 接口"""
        if not self.qwen_api_key:
            return "错误：未配置通义千问API_KEY，请设置环境变量 DASHSCOPE_API_KEY"
        
        headers = {
            "Authorization": f"Bearer {self.qwen_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "qwen-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        
        try:
            resp = requests.post(
                self.endpoints["qwen"],
                headers=headers,
                json=data,
                timeout=60
            )
            resp.raise_for_status()
            result = resp.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"通义千问API调用失败: {str(e)}"

    def _zhipu_chat(self, prompt):
        """智谱AI Zhipu 接口"""
        if not self.zhipu_api_key:
            return "错误：未配置智谱AI API_KEY，请设置环境变量 ZHIPU_API_KEY"
        
        headers = {
            "Authorization": f"Bearer {self.zhipu_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "glm-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        
        try:
            resp = requests.post(
                self.endpoints["zhipu"],
                headers=headers,
                json=data,
                timeout=60
            )
            resp.raise_for_status()
            result = resp.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"智谱AI API调用失败: {str(e)}"

    def _doubao_chat(self, prompt):
        """豆包 Doubao 接口"""
        if not self.doubao_api_key:
            return "错误：未配置豆包API_KEY，请设置环境变量 DOUBAO_API_KEY"
        
        headers = {
            "Authorization": f"Bearer {self.doubao_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "doubao-pro-32k",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        
        try:
            resp = requests.post(
                self.endpoints["doubao"],
                headers=headers,
                json=data,
                timeout=60
            )
            resp.raise_for_status()
            result = resp.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"豆包API调用失败: {str(e)}"

    def _ollama_chat(self, prompt):
        """Ollama 本地接口"""
        url = f"{self.ollama_base_url}/chat"
        data = {
            "model": self.ollama_model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        
        try:
            resp = requests.post(url, json=data, timeout=120)
            resp.raise_for_status()
            result = resp.json()
            return result["message"]["content"]
        except Exception as e:
            return f"本地Ollama调用失败: {str(e)}"

    def analyze_vulnerability(self, vuln_info):
        """漏洞分析"""
        prompt = f"""你是网络安全专家，请对以下漏洞进行专业分析：
漏洞信息：{vuln_info}
请输出：
1. 风险等级
2. 漏洞原理
3. 典型利用方式
4. 修复建议
格式简洁，适合比赛报告。
"""
        return self.chat(prompt)

    def generate_forensics_report(self, scan_data, evidence):
        """生成取证报告"""
        prompt = f"""你是取证分析师，请根据以下数据生成一份完整的网络安全取证报告：
扫描目标：{scan_data.get('target')}
开放端口：{scan_data.get('ports')}
漏洞列表：{evidence}
要求：结构清晰、专业、可直接用于CTF或应急响应。
"""
        return self.chat(prompt)
