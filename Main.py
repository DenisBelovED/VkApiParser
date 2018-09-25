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


def get_command():
    print("Введите запрос")
    return input().split(' ')


def help_list():
    print('exit')
    print('get_user_info <arg>')
    print('friend_list <int arg>')


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
        print('\n')


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


def main():
    print(r'Вводите команды через пробел. Чтобы просмотреть список команд введите help')
    with open('accessToken', 'r') as file:
        access_token = file.readline()
    work_loop(access_token)


if __name__ == '__main__':
    main()
