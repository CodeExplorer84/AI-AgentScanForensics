from ai import AIClient
from scanners import PortScanner, VulnerabilityScanner, VulnerabilityVerifier

class ScanAgent:
    def __init__(self, ai_type="doubao", **kwargs):
        self.ai = AIClient(ai_type=ai_type, **kwargs)
        self.port_scanner = PortScanner()
        self.vuln_scanner = VulnerabilityScanner()
        self.verifier = VulnerabilityVerifier(self.ai)
    
    def scan_target(self, target, ports=None):
        """完整扫描流程：端口扫描 -> 漏洞检测 -> AI核实"""
        # 1. 端口扫描
        print(f"[*] 正在扫描端口: {target}")
        scan_data = self.port_scanner.scan_ports(target, ports)
        
        if scan_data.get("host_status") == "down":
            print(f"[!] 目标主机 {target} 不可达")
            return scan_data
        
        # 2. 漏洞检测
        print(f"[*] 正在检测潜在漏洞...")
        vulnerabilities = self.vuln_scanner.detect_vulnerabilities(scan_data)
        
        if not vulnerabilities:
            print(f"[+] 未检测到潜在漏洞")
            scan_data["vulnerabilities"] = []
            return scan_data
        
        # 3. AI核实漏洞
        print(f"[*] 正在使用AI核实漏洞...")
        verified_vulns = self.verifier.verify_all(vulnerabilities, scan_data)
        
        scan_data["vulnerabilities"] = verified_vulns
        
        return scan_data
    
    def ai_analyze_vuln(self, vuln):
        return self.ai.analyze_vulnerability(vuln)
