import socket
import ssl
import httpx
import asyncio

TIMEOUT = 5

def read_domains(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]
        
def resolve(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None
        
def check_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return True, cert
    except Exception as e:
        return False, f"Error: {e}"
        
        
async def check_https(domain):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, verify=True) as client:
            response = await client.get(f"https://{domain}/")
            return response.status_code
    except Exception as e:
        return f"Error: {e}"
        
        
async def main():
    domains = read_domains("dns_cleanup.txt")
    print("domain;ip;certificate_is_valid;status_https")
    
    for domain in domains:
         #print(f"Domain: {domain}")
         ip = resolve(domain)
         if not ip:
             print(f"{domain},N/A,N/A,N/A")   
             continue
             
         cert_valid, cert_info = check_certificate(domain)
         cert_status = "OK" if cert_valid else "NON_OK"
         
             
         status = await check_https(domain)
         print(f"{domain},{ip},{cert_status},{status}")
         
         
if __name__ == "__main__":
    asyncio.run(main())
             
             
             
