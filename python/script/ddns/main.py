import socket
import logging
import time

# from lib.dynv6 import dynv6_update as update
from lib.dnspod import dnspod_update as update

logging.basicConfig(filename='log.txt', filemode='a', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def get_temp_ipv6():
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.connect(('2001::1', 80))  # 连接到一个IPv6地址 (未真正建立链接)
        return s.getsockname()[0]  # 获取临时IPv6地址


def task():
    last_ipv6 = None
    while True:
        try:
            current_ipv6 = get_temp_ipv6()
            if current_ipv6 != last_ipv6:
                resp = update(current_ipv6)
                last_ipv6 = current_ipv6

                logging.info(f'{current_ipv6} {resp}')

            else:
                logging.info('ipv6 address no changed with last hour')

            time.sleep(60 * 60)
        except Exception as e:
            logging.error(e)
            time.sleep(60)


task()
