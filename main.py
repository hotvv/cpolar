# nohup python3 /volume1/www/main.py > /volume1/www/nohup_log.log 2>&1 &  //在后台启动
# ps aux | grep host.py  查看进程 kill pid 结束进程
# filename='/volume1/www/url_log.log' 日志文件
# file_url = '/volumeUSB1/usbshare/ihyuhtml/1.txt' 得到url后保存在这个文件里

import requests,time
import logging

logging.basicConfig(filename='/volume1/www/url_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login(login_url, session, headers, json_data):
    """
    登录函数，返回登录token。
    """
    try:
        response = session.post(login_url, headers=headers, json=json_data, verify=True)
        response.raise_for_status()
        token = response.json()['data']['token']
        logging.info(f"登录成功")
        return token
    except Exception as error:
        logging.error(f"登录失败: {error}")
        return None

def get_tunnel_url(tunnel_url, session, headers):
    """
    获取隧道URL的函数。
    """
    try:
        response = session.get(tunnel_url, headers=headers, verify=True)
        response.raise_for_status()
        return response.json()['data']['items'][0]['publish_tunnels'][0]['public_url']
    except Exception as error:
        logging.error(f"获取隧道URL失败: {error}")
        return None

def write_to_file(file_url, content):
    """
    将内容写入文件。
    """
    try:
        with open(file_url, 'w') as f:
            f.write(content)
    except IOError as error:
        logging.error(f"写入文件错误: {error}")
        raise

def main_cycle(headers,tunnel_url,session,lod_pu_url, file_url):
    while True:
        # 每5分钟检查一次
        time.sleep(5 * 60)
        # for i in range(50):
        #     time.sleep(12)
        #     print('\r当前进度：{0}{1}%'.format('▉'*i,(i*2)), end='')
        # print('\n')
        
        pu_url = get_tunnel_url(tunnel_url, session, headers)
        if pu_url is None:
            #跳出循环并重新运行主函数
            logging.info('重新更新token')
            main()
            return
        if pu_url != lod_pu_url:
            # print(pu_url)
            logging.info('更新网址：'+ pu_url)
            write_to_file(file_url, pu_url)
            lod_pu_url = pu_url

def main():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'http://192.168.10.9:9200/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    json_data = {
        'email': '123@123.com', #用户
        'password': '123123123', #密码
    }
    login_url = 'http://192.168.10.9:9200/api/v1/user/login'
    tunnel_url = 'http://192.168.10.9:9200/api/v1/tunnels'
    session = requests.Session()
    file_url = '/volumeUSB1/usbshare/ihyuhtml/1.txt'
    login_token = login(login_url, session, headers, json_data)
    headers['Authorization'] = f'Bearer {login_token}'
    with open(file_url, 'r') as f:
            lod_pu_url = f.read()
    main_cycle(headers,tunnel_url,session,lod_pu_url, file_url)

if __name__ == '__main__':
    main()
