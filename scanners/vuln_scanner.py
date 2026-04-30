class VulnerabilityScanner:
    def __init__(self):
        # 内置常见漏洞检测规则
        self.vuln_rules = {
            "Apache Path Traversal (CVE-2021-41773)": {
                "ports": [80, 443, 8080], 
                "pattern": "apache",
                "severity": "CRITICAL"
            },
            "SSH Weak Configuration": {
                "ports": [22], 
                "pattern": "ssh",
                "severity": "HIGH"
            },
            "MySQL Default Configuration": {
                "ports": [3306], 
                "pattern": "mysql",
                "severity": "MEDIUM"
            },
            "PostgreSQL Default Configuration": {
                "ports": [5432], 
                "pattern": "postgresql",
                "severity": "MEDIUM"
            },
            "Redis Unauthorized Access": {
                "ports": [6379], 
                "pattern": "redis",
                "severity": "CRITICAL"
            },
            "MongoDB Unauthorized Access": {
                "ports": [27017], 
                "pattern": "mongodb",
                "severity": "CRITICAL"
            },
            "HTTP Proxy Misconfiguration": {
                "ports": [8080, 8443], 
                "pattern": "http",
                "severity": "HIGH"
            }
        }
    
    def detect_vulnerabilities(self, scan_data):
        """根据端口扫描结果检测潜在漏洞"""
        vulnerabilities = []
        
        if "services" not in scan_data:
            return vulnerabilities
        
        for service in scan_data["services"]:
            port = service["port"]
            service_name = service["service"]
            version = service["version"]
            
            # 匹配漏洞规则
            for vuln_name, rule in self.vuln_rules.items():
                if port in rule["ports"] and rule["pattern"].lower() in service_name.lower():
                    vulnerabilities.append({
                        "name": vuln_name,
                        "port": port,
                        "service": service_name,
                        "version": version,
                        "severity": rule["severity"],
                        "verified": False
                    })
        
        return vulnerabilities
