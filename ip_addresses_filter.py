import requests


def get_provider(ip_address):
    try:
        params = {'ip': ip_address}
        IP_API_URL = f'http://ip-api.com/json/{params}'
        response = requests.get(IP_API_URL, params=params)
        provider = response.json().get('org')
        if provider:
            return provider
        return 'Неизвестный провайдер'
    except Exception as error:
         raise Exception(f'Сбой при обращении к сервису IP-API: {error}')


def get_octets_from_ip(ip_address):
    """Преобразование ip-адреса (либо маски подсети) в список октетов."""
    octet_list = []
    for octet in ip_address.split('.'):
        octet_list.append(int(octet))
    return octet_list


def compare_ip_and_mask(ip_octet_list, mask_octet_list):
    """Сравнение двоичных чисел в ip-адресе и маске подсети.
    (Операция AND)."""
    ip_and_mask_compare_list = []
    for ip_address, subnet_mask in zip(ip_octet_list, mask_octet_list):
        ip_and_mask_compare_list.append(ip_address & subnet_mask)
    return ip_and_mask_compare_list


def filter_ip_addresses(network_ip, subnet_mask, ip_addresses):
    """Фильтрация ip-адресов. Добавление в итоговый список адресов,
    входящих в указанную сеть.
    """
    network_octet_list = get_octets_from_ip(network_ip)
    subnet_mask_octet_list = get_octets_from_ip(subnet_mask)
    network_and_subnet_compare_list = compare_ip_and_mask(
        network_octet_list, subnet_mask_octet_list
    )
    filtered_list = []
    for ip in ip_addresses:
        octet_list = get_octets_from_ip(ip)
        ip_and_mask_compare_list = compare_ip_and_mask(
            octet_list, subnet_mask_octet_list
        )
        if ip_and_mask_compare_list == network_and_subnet_compare_list:
            provider = get_provider(ip)
            filtered_list.append({ip: provider})
    return filtered_list


def main():
    with open('input.txt', 'r') as file:
        network_ip = file.readline()
        subnet_mask = file.readline()
        ip_addresses = file.readline().split()
    print(filter_ip_addresses(network_ip, subnet_mask, ip_addresses))


if __name__ == '__main__':
    main()
