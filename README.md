![AgentScanForensics](banner.png)

# AgentScanForensics

AI-powered vulnerability scanning & forensic automation tool for CTF and incident response. Supports **5 major AI engines** (OpenAI, Qwen, Zhipu, Doubao, Ollama) with real port scanning and AI-verified vulnerability detection.

## ✨ Features

- **Multi-AI Support**: OpenAI GPT-4, Alibaba Qwen, Zhipu GLM, ByteDance Doubao, Local Ollama
- **Real Port Scanning**: Integrated python-nmap for actual port scanning (not simulated)
- **Vulnerability Detection**: Rule-based vulnerability identification for common services
- **AI Verification**: AI-powered vulnerability verification to reduce false positives
- **Automated Reporting**: Professional forensic report generation
- **Command-Line Interface**: Flexible configuration via command-line arguments
- **Configurable**: YAML-based configuration file support

## 📦 Installation

### Prerequisites

- Python 3.7+
- Nmap installed (required for port scanning)

### 1. Install Nmap

**Windows:**
Download from https://nmap.org/download.html and install

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install nmap
```

**macOS:**
```bash
brew install nmap
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 AI Configuration

### 1. OpenAI GPT

1. Get API key from https://platform.openai.com/api-keys
2. Set environment variable:

**Linux/macOS:**
```bash
export OPENAI_API_KEY="sk-your-openai-api-key"
```

**Windows:**
```cmd
set OPENAI_API_KEY=sk-your-openai-api-key
```

### 2. 通义千问 (Alibaba Qwen)

1. Get API key from https://dashscope.console.aliyun.com/
2. Set environment variable:

**Linux/macOS:**
```bash
export DASHSCOPE_API_KEY="sk-your-dashscope-api-key"
```

**Windows:**
```cmd
set DASHSCOPE_API_KEY=sk-your-dashscope-api-key
```

### 3. 智谱AI (Zhipu GLM)

1. Get API key from https://open.bigmodel.cn/
2. Set environment variable:

**Linux/macOS:**
```bash
export ZHIPU_API_KEY="your-zhipu-api-key"
```

**Windows:**
```cmd
set ZHIPU_API_KEY=your-zhipu-api-key
```

### 4. 豆包 (ByteDance Doubao)

1. Get API key from https://console.volcengine.com/
2. Set environment variable:

**Linux/macOS:**
```bash
export DOUBAO_API_KEY="your-doubao-api-key"
```

**Windows:**
```cmd
set DOUBAO_API_KEY=your-doubao-api-key
```

### 5. Ollama (Local)

1. Install Ollama from https://ollama.com/
2. Pull a model:
```bash
ollama pull llama3
```
3. (Optional) Set custom model:
```bash
export OLLAMA_MODEL=llama3
```

## 🚀 Usage

### Basic Usage

```bash
# Quick scan with default settings (uses doubao AI)
python main.py -t 192.168.1.1

# Specify target and ports
python main.py -t 192.168.1.1 -p 22,80,443,8080

# Use OpenAI GPT-4
python main.py -t 192.168.1.1 --ai openai

# Use Qwen with custom report file
python main.py -t example.com --ports 80,443,8080 --ai qwen --report report.txt
```

### Command-Line Options

```
-t, --target      Target IP address or domain (required)
-p, --ports       Ports to scan (comma-separated)
--ai              AI engine: openai/qwen/zhipu/doubao/ollama (default: doubao)
--report          Output report file path (default: forensics_report.txt)
--config          Configuration file path (default: config.yaml)
```

### Examples

```bash
# Scan common web ports with OpenAI
python main.py -t 192.168.1.100 -p 80,443,8080,8443 --ai openai

# Scan database ports with Qwen
python main.py -t 10.0.0.1 -p 3306,5432,6379,27017 --ai qwen

# Full scan with Zhipu AI
python main.py -t target.com --ai zhipu --report full_scan_report.txt

# Use local Ollama
python main.py -t 127.0.0.1 --ai ollama
```

## 📁 Project Structure

```
AgentScanForensics/
├── ai/                      # AI interface module
│   ├── __init__.py
│   └── ai_client.py         # Multi-AI client implementation
├── agents/                  # Agent modules
│   ├── __init__.py
│   ├── scan_agent.py        # Scanning agent
│   ├── report_agent.py      # Report generation agent
│   └── correlation_agent.py # Evidence correlation agent
├── scanners/                # Scanning engines
│   ├── __init__.py
│   ├── port_scanner.py      # Port scanning engine (nmap)
│   ├── vuln_scanner.py      # Vulnerability detection engine
│   └── verifier.py          # AI vulnerability verification
├── config/                  # Configuration management
│   ├── __init__.py
│   └── settings.py          # YAML config loader
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── data_loader.py       # Data loading utilities
├── main.py                  # Main entry point
├── requirements.txt         # Python dependencies
├── config.yaml.example      # Example configuration file
├── README.md                # This file
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
└── banner.png              # Project banner
```

## ⚙️ Configuration

### config.yaml

The tool automatically creates a `config.yaml` file on first run. You can customize it:

```yaml
ai:
  engine: doubao  # Default AI engine
  openai_model: gpt-4
  qwen_model: qwen-turbo
  zhipu_model: glm-4
  ollama_model: llama3

scan:
  default_ports: "22,80,443,8080,3306,5432,8443,6379,27017"
  scan_timeout: 60
```

## 🔍 How It Works

### Scanning Workflow

1. **Port Scanning**: Uses python-nmap to scan specified ports
2. **Service Detection**: Identifies running services and versions
3. **Vulnerability Detection**: Matches services against known vulnerability rules
4. **AI Verification**: Each vulnerability is verified by AI to reduce false positives
5. **Report Generation**: Comprehensive forensic report with AI analysis

### Vulnerability Rules

Built-in detection for:
- Apache Path Traversal (CVE-2021-41773)
- SSH Weak Configuration
- MySQL Default Configuration
- PostgreSQL Default Configuration
- Redis Unauthorized Access
- MongoDB Unauthorized Access
- HTTP Proxy Misconfiguration

## 📄 Output

### Console Output
- Real-time scanning progress
- Port and service information
- Vulnerability verification results

### Report File
- Complete forensic report (default: `forensics_report.txt`)
- Target information
- Port scan results
- Service details
- Vulnerability list with AI verification
- Professional AI-generated analysis

## 🔒 Security Notes

- **No Hardcoded Keys**: All API keys are read from environment variables
- **Git-Safe**: `.gitignore` prevents committing sensitive files
- **Local Processing**: Ollama option for fully local AI processing
- **Authorization**: Only scan systems you have permission to test

## 🛠️ Extending

### Add Custom Vulnerability Rules

Edit `scanners/vuln_scanner.py`:

```python
self.vuln_rules = {
    "Your Custom Vulnerability": {
        "ports": [80, 443],
        "pattern": "service-name",
        "severity": "HIGH"
    }
}
```

### Add New AI Provider

Edit `ai/ai_client.py` and add a new method:

```python
def _your_ai_chat(self, prompt):
    # Implement your AI interface
    pass
```

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool is designed for authorized security testing and educational purposes only. Always obtain proper authorization before scanning any systems. The authors are not responsible for misuse of this tool.
