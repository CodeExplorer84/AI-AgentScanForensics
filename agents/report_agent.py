from ai import AIClient

class ReportAgent:
    def __init__(self, ai_type="doubao", **kwargs):
        self.ai = AIClient(ai_type=ai_type, **kwargs)
    
    def generate_report(self, scan_data):
        """生成完整的取证报告"""
        vulns_summary = []
        for vuln in scan_data.get("vulnerabilities", []):
            vulns_summary.append(f"- {vuln['name']} (端口:{vuln['port']}, 严重级别:{vuln['severity']}, 核实:{vuln.get('verification', '待核实')})")
        
        ai_report = self.ai.generate_forensics_report(scan_data, vulns_summary)
        
        final = f"""
{'='*70}
  AgentScanForensics - 自动化漏洞扫描与取证报告
{'='*70}

【目标信息】
目标地址: {scan_data['target']}
主机状态: {scan_data.get('host_status', 'unknown')}

【端口扫描结果】
开放端口: {scan_data['ports']}

【服务详情】
{self.format_services(scan_data.get('services', []))}

【漏洞检测与核实】
发现漏洞: {len(scan_data.get('vulnerabilities', []))} 个
{chr(10).join(vulns_summary) if vulns_summary else '无'}

【AI智能分析报告】
{ai_report}

{'='*70}
报告生成时间: 由AgentScanForensics自动生成
{'='*70}
"""
        return final
    
    def format_services(self, services):
        """格式化服务信息"""
        if not services:
            return "  无"
        output = []
        for svc in services:
            output.append(f"  端口 {svc['port']}: {svc['service']} {svc['version']} ({svc['state']})")
        return '\n'.join(output)
    
    def save_report(self, content, path="forensics_report.txt"):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] 报告已保存到 {path}")
