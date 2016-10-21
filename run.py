import requests
from bs4 import BeautifulSoup
import re

url = 'http://222.204.3.49:8082/'
chk_code_url = "http://222.204.3.49:8082/gif.aspx?"
response = None


def main():
    global response

    # Get _ViewState
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html5lib")
    view_state = soup.select("#__VIEWSTATE")[0].attrs['value']
    print("input username\n")
    user_name = input()
    print("input password")
    password = input()

    print("getting check code...")
    ckdata = requests.get(chk_code_url)

    ckcode = re.search('(?<=ChkCode=).*', ckdata.cookies['validateCookie']).group(0)

    print("check code is %s" % (ckcode))

    chk_cookie = ckdata.cookies['validateCookie']
    session = ckdata.cookies['ASP.NET_SessionId']

    cookies = {'validateCookie': chk_cookie,
               'ASP.NET_SessionId': session}

    post_data = {
        '__VIEWSTATE': view_state,
        'Txt_UserName': user_name,
        'Txt_PassWord': password,
        'Txt_Yzm': ckcode,
        'Btn_login': ''
    }

    response = requests.post(url, cookies=cookies, data=post_data)
    print(response.text)
    print("Finished")
    print("request this with cookie : ASP.NET_SessionId=%s" %(session))
    pass


if __name__ == '__main__':
    main()
