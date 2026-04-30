class VulnerabilityVerifier:
    def __init__(self, ai_client):
        self.ai = ai_client
    
    def verify_vulnerability(self, vuln_info, scan_data):
        """使用AI辅助核实漏洞"""
        prompt = f"""你是网络安全专家，请核实以下漏洞是否存在：

目标信息：
- IP: {scan_data['target']}
- 开放端口: {scan_data['ports']}
- 服务信息: {scan_data['services']}

待核实漏洞：
- 漏洞名称: {vuln_info['name']}
- 涉及端口: {vuln_info['port']}
- 服务: {vuln_info['service']} {vuln_info['version']}
- 初步严重级别: {vuln_info['severity']}

请分析：
1. 该漏洞是否可能存在于当前环境
2. 判断依据
3. 建议的验证方法
4. 误报可能性

输出格式：
- 核实结果：[高可能性/中可能性/低可能性/误报]
- 原因分析：[详细说明]
- 验证建议：[具体步骤]
"""
        return self.ai.chat(prompt)
    
    def verify_all(self, vulnerabilities, scan_data):
        """批量核实所有漏洞"""
        verified_results = []
        
        for vuln in vulnerabilities:
            print(f"[*] 正在核实漏洞: {vuln['name']}...")
            verification = self.verify_vulnerability(vuln, scan_data)
            
            verified_results.append({
                **vuln,
                "verification": verification,
                "verified": True
            })
        
        return verified_results
