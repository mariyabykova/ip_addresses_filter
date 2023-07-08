# ip_addresses_filter

Программа для фильтрации IP-адресов, находящихся не в указанной подсети.

### Технологии
python 3.9

### Описание
Программа позволяет отсеить IP-адреса, находящиеся не в указанной подсети. Приложение принимает 3 пользовательских аргумента:
1. IP-адрес сети (IPv4)
2. Маска подсети
3. Список проверяемых IP-адресов:
    * Списком через разделитель (пробел)
    * Передачей пути до файла на диске

В случае, если на вход поступил список адресов, на выходе выводится список словарей. Ключ словаря – это IP-адрес, а значение – провайдер. Пример вывода: [{'95.220.83.0': 'Net By Net Holding LLC'}, {'192.168.0.4': 'Неизвестный провайдер'}]

Если данные поступают из csv-файла, на выходе данные загружаются в другой csv-файл. Пример вывода в файл:

ip,provider
95.220.83.0,Net By Net Holding LLC <br/>
192.168.0.4,Неизвестный провайдер

### Логика работы программы:

Некоторые функции проекта:

``` read_list_data(is_list) ``` – отвечает за ввод пользовательских данных. Аргумент is_list может принимать значения True или False. В случае, если is_list is True, программа читает данные из файла, в котором указаны IP-адрес сети, маска подсети и список IP-адресов. В противном случае данные читаются из файла, в котором должны быть IP-адрес сети, маска подсети и путь к файлу csv. Для удобства использования программы введена константа IS_LIST, которой может быть присвоено значение True иил False. Также определены константы для пути к текстовым файлам (FILE_1 - для работы со списком, FILE_2 - для работы с csv-файлом) и константы для путей к файлам csv (PATH – путь к файлу для импорта данных, EXPORT_PATH – путь к файлу для экспорта данных). При тестировании проекта необходимо присвоить константам нужные значения, чтобы чтение данных и работы программы выполнялись корректно.

``` filter_ip_addresses(network_ip, subnet_mask, ip_addresses, is_list) ``` – отвечает за фильтрацию адресов. Для каждого адреса, который находится в указанной подсети, определяется провайдер. Отфильтрованные адреса с провайдерами добавляются в результирующий список. В случае, если аргумент is_list принимает значение True, функция возвращает список словарей в указанном выше формате. Если is_list is False, данные записываются в csv-файл, а функция возвращает сообщение: 'Отфильтрованный список записан в файл {путь_к_файлу}'.

``` read_csv ``` – всмопогательная функция, отвечающая за чтение данных из csv-файла. Возвращает список IP-адресов.

``` export_to_csv ``` – вспомогательная функция, отвечающая за запись данных в csv-файл.

``` get_provider ``` – вспомогательная функция, отвечающая за получение данных о провайдере по IP-адресу. Используется открытое IP-API.

``` get_octets_from_ip ``` – вспомогательная функция, позволяющая разделить IP-адрес (либо маску подсети) на октеты, что необходимо для дальнейшей процедуры сравнения IP-адресов.

``` compare_ip_and_mask ``` – вспомогательная функция, осуществляющая сравнение двоичных чисел в IP-адресе и маске подсети с помощью операции AND.

### Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

``` git@github.com:mariyabykova/ip_addresses_filter.git ``` <br/>
``` cd  ip_addresses_filter ```

Создать виртуальное окружение:

* Если у вас Linux/macOS:
    ``` python3 -m venv venv ``` 

* Если у вас Windows:
    ``` python -3.9 -m venv venv ```

Активировать виртуальное окружение:

* Если у вас Linux/macOS:
    ``` source venv/bin/activate ``` 

* Если у вас Windows:
    ``` source venv/Scripts/activate ```

Обновить pip:

``` python3 -m pip install --upgrade pip ``` 

Установить зависимости из файла requirements:

``` pip install -r requirements.txt ``` 

Запустить проект:

``` python3 ip_addresses_filter.py ``` 


### Автор проекта

**Мария Быкова.** 
