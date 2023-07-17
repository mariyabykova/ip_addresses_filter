import csv
import re
from typing import Dict, List, Tuple, Union

import requests


IS_LIST: bool = False
PATH: str = 'data.csv'
EXPORT_PATH: str = 'output_data.csv'
FILE_1: str = 'input.txt'
FILE_2: str = 'input_csv.txt'


def read_csv(path: str) -> List[str]:
    """Получение ip-адресов из csv-файла."""
    with open(path, 'r', encoding='utf-8') as csv_file:
        file_reader = csv.DictReader(csv_file, delimiter=',')
        ip_addresses = []
        for row in file_reader:
            ip_addresses.append(row['ip'])
        return ip_addresses


def export_to_csv(export_path: str, ip_addresses: List[Dict]) -> None:
    """Загрузка данных в csv-файл."""
    with open(export_path, 'w', encoding='utf-8') as csv_file:
        names = ['ip', 'provider']
        file_writer = csv.DictWriter(
            csv_file,
            delimiter=',',
            fieldnames=names
        )
        file_writer.writeheader()
        for address in ip_addresses:
            for ip, provider in address.items():
                file_writer.writerow({'ip': ip, 'provider': provider})


def get_provider(ip_address: str) -> str:
    """Определение провайдера по ip-адресу."""
    try:
        IP_API_URL = f'http://ip-api.com/json/{ip_address}'
        response = requests.get(IP_API_URL)
        provider = response.json().get('org')
        if provider:
            return provider
        return 'Неизвестный провайдер'
    except Exception as error:
        raise Exception(f'Сбой при обращении к сервису IP-API: {error}')


def get_octets_from_ip(ip_address: str) -> List[int]:
    """Преобразование ip-адреса (либо маски подсети) в список октетов."""
    octet_list = []
    for octet in ip_address.split('.'):
        octet_list.append(int(octet))
    return octet_list


def compare_ip_and_mask(ip_octet_list: List[int],
                        mask_octet_list: List[int]) -> List[int]:
    """Сравнение двоичных чисел в ip-адресе и маске подсети.
    (Операция AND).
    """
    ip_and_mask_compare_list = []
    for ip_address, subnet_mask in zip(ip_octet_list, mask_octet_list):
        ip_and_mask_compare_list.append(ip_address & subnet_mask)
    return ip_and_mask_compare_list


def validate_ip_adress(ip_address: str) -> bool:
    """Валидация ip-адреса."""
    octet_list = get_octets_from_ip(ip_address)
    if len(octet_list) != 4:
        return False
    flag = False
    for octet in octet_list:
        if len(str(octet)) > 1 and str(octet).startswith('0'):
            return False
        if str(octet).isdigit() and int(octet) >= 0 and int(octet) <= 127:
            flag = True
        else:
            return False
    return flag


def validate_mask(ip_mask):
    """Валидация маски подсети."""
    regex = ('^(((127\.){3}(127|126|124|120|112|96|64|0+))|((127\.){2}'
            '(127|126|124|120|112|96|64|0+)\.0)|((127\.)'
            '(127|126|124|120|112|96|64|0+)(\.0+){2})|'
            '((127|126|124|120|112|96|64|0+)(\.0+){3}))$')
    if re.match(regex, ip_mask):
        return True
    return False


def filter_ip_addresses(network_ip: str,
                        subnet_mask: str,
                        ip_addresses: List[str],
                        is_list: bool = IS_LIST) -> Union[List[Dict], str]:
    """Фильтрация ip-адресов. Добавление в итоговый список адресов,
    входящих в указанную сеть, а также их провайдеров.
    """
    if not validate_ip_adress(network_ip):
        raise ValueError
    if not validate_mask(subnet_mask):
        raise ValueError
    network_octet_list = get_octets_from_ip(network_ip)
    subnet_mask_octet_list = get_octets_from_ip(subnet_mask)
    network_and_subnet_compare_list = compare_ip_and_mask(
        network_octet_list, subnet_mask_octet_list
    )
    filtered_list = []
    for ip in ip_addresses:
        if validate_ip_adress(ip):
            octet_list = get_octets_from_ip(ip)
            ip_and_mask_compare_list = compare_ip_and_mask(
                octet_list, subnet_mask_octet_list
            )
            if ip_and_mask_compare_list == network_and_subnet_compare_list:
                provider = get_provider(ip)
                filtered_list.append({ip: provider})
    if is_list is True:
        return filtered_list
    export_to_csv(EXPORT_PATH, filtered_list)
    return f'Отфильтрованный список записан в файл {EXPORT_PATH}'


def read_list_data(is_list: bool) -> Tuple[str, str, List[str]]:
    """Чтение пользовательских данных из текстового файла.
    """
    if is_list is True:
        with open(FILE_1, 'r') as file:
            network_ip = file.readline()
            subnet_mask = file.readline()
            ip_addresses = file.readline().split()
    if is_list is False:
        with open(FILE_2, 'r') as file:
            network_ip = file.readline()
            subnet_mask = file.readline()
            path = file.readline()
        ip_addresses = read_csv(path)
    return network_ip, subnet_mask, ip_addresses


def main() -> None:
    """Основная функция. Вывод отфильтрованного списка ip-адресов."""
    network_ip, subnet_mask, ip_addresses = read_list_data(IS_LIST)
    print(filter_ip_addresses(network_ip, subnet_mask, ip_addresses, IS_LIST))


if __name__ == '__main__':
    main()
