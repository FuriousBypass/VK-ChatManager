import time
import datetime
import vk_api
import requests
import random
import re
from vk_api.longpoll import VkLongPoll, VkEventType


vk_session = vk_api.VkApi(token='ВАШ ТОКЕН')
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
pattern = r"(id[\w\.]+)"
id = r"([0-9]+)"
print("Админ бот включен")
cmds = '/сkick - кикнуть пользователя из конференции \n /adminka(доступ у создателя беседы) - выдать права администратора'
adm = []
developer = 480509201 #Тут должен быть ID Разработчика бота :)
blist = []

#основной цикл
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                #print(event.peer_id)
                response = event.text
                text = response.split()
                conv = vk.messages.getChat(chat_id=event.chat_id)
                admin_id = conv['admin_id']


                if text[0] == "/cban":
                    a_lvl = str(event.user.id)
                    if a_lvl in adm or a_lvl == str(admin_id):
                        fof = event.text
                        sum1 = fof.replace('/cban', '')
                        sum2 = sum1.replace(text[1], '')
                        match = re.search(pattern, text[1])
                        if match:
                            test = match.group()
                            user1 = vk.utils.resolveScreenName(screen_name=test)
                            user = str(user1['object_id'])
                            users = vk.users.get(user_ids=user)
                            first_name = users[0]['first_name']
                            last_name = users[0]['last_name']
                            if user == '480509201':
                                vk.messages.send(peer_id=event.peer_id, message= "БОТ » У создателя бота иммунитет на все наказания, даже на наказания от создателя беседы" + text[2], random_id=random.randint(1, 10000000))

                            else:
                                try:
                                    vk.messages.removeChatUser(chat_id=int(event.chat_id), user_id=str(user))
                                    vk.messages.send(peer_id=event.peer_id, message= "БОТ » Пользователь " + "[id" + str(user) + "|" + first_name + " " + last_name + "]" + " был исключен из беседы. \n Причина: " + sum2, random_id=random.randint(1, 10000000))
                                    blist.append(event.user_id)

                                except vk_api.exceptions.ApiError as vk_error:
                                    if vk_error.code == 15:
                                        continue
                                except:
                                    vk.messages.send(peer_id=event.peer_id, message= "БОТ » Нельзя забанить создателя беседы!", random_id=random.randint(1, 10000000))

                elif text[0] == "/ckick":
                    a_lvl = str(event.user_id)
                    if a_lvl in adm or a_lvl == str(admin_id):
                        fof = event.text
                        sum1 = fof.replace('/ckick', '')
                        sum2 = sum1.replace(text[1], '')
                        match = re.search(pattern, text[1])
                        if match:
                            test = match.group()
                            user1 = vk.utils.resolveScreenName(screen_name=test)
                            user = str(user1['object_id'])
                            users = vk.users.get(user_ids=user)
                            first_name = users[0]['first_name']
                            last_name = users[0]['last_name']
                            if user == str(developer):
                                vk.messages.send(peer_id=event.peer_id, message= "БОТ » У создателя бота иммунитет на все наказания, даже на наказания от создателя беседы" + text[2], random_id=random.randint(1, 10000000))

                            else:
                                try:
                                    vk.messages.removeChatUser(chat_id=int(event.chat_id), user_id=str(user))
                                    vk.messages.send(peer_id=event.peer_id, message= "БОТ » Пользователь " + "[id" + str(user) + "|" + first_name + " " + last_name + "]" + " был исключен из беседы. \n Причина: " + sum2, random_id=random.randint(1, 10000000))



                                except:
                                    vk.messages.send(peer_id=event.peer_id, message= "БОТ » Нельзя кикнуть создателя беседы!", random_id=random.randint(1, 10000000))


                elif text[0] == ".conv":
                    conv = vk.messages.getChat(chat_id=str(event.chat_id))
                    admin_id = conv['admin_id']
                    title = conv['title']
                    id = conv['id']
                    users_conv = len(conv['users'])
                    vk.messages.send(peer_id=event.peer_id, message= "БОТ » Информация о беседе: \n Название беседы: " + str(title) + "\n ID Беседы: " + str(id) + "\n Создатель беседы: " + str(admin_id) + "\n Количество пользователей: " + str(users_conv), random_id=random.randint(1, 10000000))

                elif text[0] == '/adminka':
                    a_lvl = str(event.user_id)
                    if event.user_id == developer or a_lvl == str(admin_id):
                        asas = text[1]
                        match = re.search(pattern, asas)
                        if match:
                                test = match.group()
                                user1 = vk.utils.resolveScreenName(screen_name=test)
                                user = str(user1['object_id'])
                                users = vk.users.get(user_ids=user)
                                first_name = users[0]['first_name']
                                last_name = users[0]['last_name']

                                try:
                                    if text[2] == "1":
                                        vk.messages.send(peer_id=event.peer_id, message= "БОТ » Пользователю " + "[id" + str(user) + "|" + first_name + " " + last_name + "]" + " были выданы права администратора.", random_id=random.randint(1, 10000000))
                                        print(user)
                                        adm.append(user)

                                    elif text[2] == "0":
                                        vk.messages.send(peer_id=event.peer_id, message= "БОТ » Пользователю " + "[id" + str(user) + "|" + first_name + " " + last_name + "]" + " были сняты права администратора.", random_id=random.randint(1, 10000000))
                                        print(user)
                                        adm.remove(user)

                                    else:
                                        vk.messages.send(peer_id=event.peer_id, message= "БОТ » Укажите 1 или 0.", random_id=random.randint(1, 10000000))

                                except KeyError:
                                    vk.messages.send(peer_id=event.peer_id, message= "БОТ » Укажите 1 или 0.", random_id=random.randint(1, 10000000))


                elif text[0] == "/cmds" :
                    user = str(event.user_id)
                    if user in adm or a_lvl in str(admin_id):
                        vk.messages.send(peer_id=event.peer_id, message= "БОТ » Команды администратора: \n\n" + cmds, random_id=random.randint(1, 10000000))

    except IndexError:
        if response == "/ckick":
            if a_lvl in adm or a_lvl == str(admin_id):
                vk.messages.send(peer_id=event.peer_id, message= "БОТ » /ckick [ID пользователя] [Причина]", random_id=random.randint(1, 10000000))

        if response == "/adminka":
            if event.user_id == developer or a_lvl == str(admin_id):
                vk.messages.send(peer_id=event.peer_id, message= "БОТ » /adminka [ID пользователя] [1 - выдать/0 - забрать]", random_id=random.randint(1, 10000000))
        continue

    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверам ВК \n")
        time.sleep(3)
        try:
            print("Переподключение прошло успешно!")
        except:
            print("Ошибка подключения")


    except AttributeError:
        continue

    except:
        continue