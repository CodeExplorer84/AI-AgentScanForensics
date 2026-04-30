import nmap

class PortScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    def scan_ports(self, target, ports="22,80,443,8080,3306,5432,8443"):
        """扫描指定端口，返回开放端口和服务信息"""
        try:
            self.nm.scan(target, ports=ports, arguments='-sV')
            
            scan_results = {
                "target": target,
                "ports": [],
                "services": [],
                "host_status": self.nm[target].state() if target in self.nm.all_hosts() else "down"
            }
            
            if target in self.nm.all_hosts():
                for port in self.nm[target]['tcp']:
                    port_info = self.nm[target]['tcp'][port]
                    scan_results["ports"].append(port)
                    scan_results["services"].append({
                        "port": port,
                        "service": port_info.get('name', 'unknown'),
                        "version": port_info.get('version', 'unknown'),
                        "state": port_info.get('state', 'unknown')
                    })
            
            return scan_results
        except Exception as e:
            print(f"[!] 扫描失败: {str(e)}")
            return {
                "target": target,
                "ports": [],
                "services": [],
                "host_status": "error",
                "error": str(e)
            }
