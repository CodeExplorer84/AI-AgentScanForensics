import os
import argparse
from agents import ScanAgent, ReportAgent
from config import Settings

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='AgentScanForensics - AI驱动的漏洞扫描与取证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py -t 192.168.1.1
  python main.py -t 192.168.1.1 -p 22,80,443
  python main.py -t 192.168.1.1 --ai openai
  python main.py -t example.com --ports 80,443,8080 --ai qwen --report my_report.txt
        """
    )
    
    parser.add_argument('-t', '--target', required=True, 
                       help='目标IP地址或域名')
    parser.add_argument('-p', '--ports', 
                       help='扫描端口（逗号分隔），默认使用config.yaml配置')
    parser.add_argument('--ai', default='doubao',
                       choices=['openai', 'qwen', 'zhipu', 'doubao', 'ollama'],
                       help='AI引擎类型（默认: doubao）')
    parser.add_argument('--report', default='forensics_report.txt',
                       help='报告输出文件路径')
    parser.add_argument('--config', default='config.yaml',
                       help='配置文件路径')
    
    return parser.parse_args()

def get_api_keys():
    """从环境变量获取所有AI API密钥"""
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "qwen_api_key": os.getenv("DASHSCOPE_API_KEY", ""),
        "zhipu_api_key": os.getenv("ZHIPU_API_KEY", ""),
        "doubao_api_key": os.getenv("DOUBAO_API_KEY", ""),
        "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/api"),
        "ollama_model": os.getenv("OLLAMA_MODEL", "llama3")
    }

def main():
    args = parse_args()
    
    # 加载配置
    settings = Settings(args.config)
    
    # 获取API密钥
    api_keys = get_api_keys()
    
    # 确定扫描端口
    ports = args.ports or settings.settings.get("scan", {}).get("default_ports", "22,80,443,8080")
    
    print(f"""
========================================
  AgentScanForensics - AI漏洞扫描取证工具
========================================
[*] 扫描目标: {args.target}
[*] 扫描端口: {ports}
[*] AI引擎: {args.ai}
[*] 报告文件: {args.report}
========================================
""")
    
    # 初始化扫描Agent
    agent = ScanAgent(
        ai_type=args.ai,
        **api_keys
    )
    
    # 执行扫描（端口扫描 -> 漏洞检测 -> AI核实）
    scan_data = agent.scan_target(args.target, ports)
    
    # 输出扫描结果
    if scan_data.get("host_status") == "down":
        print(f"\n[!] 扫描失败：目标主机不可达")
        return
    
    print(f"\n[+] 端口扫描完成，发现 {len(scan_data['ports'])} 个开放端口")
    print(f"[+] 检测到 {len(scan_data.get('vulnerabilities', []))} 个潜在漏洞")
    
    # AI漏洞分析
    if scan_data.get("vulnerabilities"):
        print("\n[*] AI漏洞分析报告:")
        for vuln in scan_data["vulnerabilities"]:
            print(f"\n{'='*60}")
            print(f"漏洞: {vuln['name']}")
            print(f"端口: {vuln['port']}")
            print(f"服务: {vuln['service']} {vuln['version']}")
            print(f"严重级别: {vuln['severity']}")
            print(f"核实结果:\n{vuln.get('verification', '待核实')}")
    
    # 生成取证报告
    print(f"\n[*] 正在生成取证报告: {args.report}")
    reporter = ReportAgent(
        ai_type=args.ai,
        **api_keys
    )
    report = reporter.generate_report(scan_data)
    reporter.save_report(report, args.report)
    
    print("\n[+] 全部完成！")

if __name__ == "__main__":
    main()
