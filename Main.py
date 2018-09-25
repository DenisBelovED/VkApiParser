import requests
from ParamsClass import Params


def use_method(f):
    def wrapped(params):
        if params:
            return requests.get(r'https://api.vk.com/method/' + f(), params=params)
        else:
            return requests.get(r'https://api.vk.com/method/' + f())

    return wrapped


@use_method
def users_get():
    return r'users.get'


@use_method
def friends_get():
    return r'friends.get'


@use_method
def docs_get():
    return 'docs.get'


@use_method
def docs_search():
    return 'docs.search'


def get_command():
    print("Введите запрос")
    return input().split(' ')


def help_list():
    print('exit')
    print('get_user_info <arg>')
    print('friend_list <arg>')
    print('get_docs <arg>')
    print('search_doc <arg> <count>')


def get_user_info(fields):
    response = users_get(fields.get_package()).json()
    for field in response['response'][0].items():
        print(field[0], ':', field[1])


def friend_list(fields, access_token, version):
    response = users_get(fields.get_package()).json()
    fields.add_fields({'user_id': str(response['response'][0]['id'])})
    response = friends_get(fields.get_package()).json()
    print('количество друзей :', str(response['response']['count']))
    fields_id = Params(access_token, version)
    s = str(response['response']['items'])[1:-1].replace(' ', '')
    fields_id.add_fields({'user_ids': s})
    response_id = users_get(fields_id.get_package()).json()
    for people in response_id['response']:
        for f in people.items():
            print(f[0], ':', f[1])
        print()


def get_docs(fields):
    response = users_get(fields.get_package()).json()
    fields.add_fields({'owner_id': str(response['response'][0]['id']), 'count': '2000'})
    response = docs_get(fields.get_package()).json()
    print('найдено документов:', str(response['response']['count']))
    for doc in response['response']['items']:
        for f in doc.items():
            print(f[0], ':', f[1])
        print()


def search_doc(fields):
    response = docs_search(fields.get_package()).json()
    for doc in response['response']['items']:
        for f in doc.items():
            print(f[0], ':', f[1])
        print()


def work_loop(access_token, version='5.85'):
    while True:
        fields = Params(access_token, version)
        command = get_command()
        if len(command) == 1:
            if command[0] == 'exit':
                break
            if command[0] == 'help':
                help_list()
                continue
        if len(command) == 2:
            if command[0] == 'get_user_info':
                fields.add_fields({'user_ids': str(command[1])})
                get_user_info(fields)
                continue
            if command[0] == 'friend_list':
                fields.add_fields({'user_ids': str(command[1])})
                friend_list(fields, access_token, version)
                continue
            if command[0] == 'get_docs':
                fields.add_fields({'user_ids': str(command[1])})
                get_docs(fields)
                continue
        if len(command) == 3:
            if command[0] == 'search_doc':
                fields.add_fields({'q': str(command[1]), 'search_own': '0', 'count': str(command[2])})
                search_doc(fields)
                continue


def main():
    print(r'Вводите команды через пробел. Чтобы просмотреть список команд введите help')
    with open('accessToken', 'r') as file:
        access_token = file.readline()
    work_loop(access_token)


if __name__ == '__main__':
    main()
