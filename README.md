# NetworksProject

Я решил реализовать в качестве проекта текстовый чат на сервере, к которому могут подключаться юзеры с разных адресов, используя написанный для них скрипт.

Проект написан на Python 3.6.3 с использованием стандартных библиотек. При запуске скрипта юзеру нужно указать IP адрес и порт сервера, после чего его поприветствует сервер и предложит выбрать ник. Этот ник будет отображаться при отправке сообщений, и по нему же можно будет обратиться к юзеру лично. Каждому юзеру соответствует ровно один ник. 

Для того, чтобы обратиться только к конретному юзеру, пользователю необходимо начать сообщение с символа @, за которым сразу следует ник нужного юзера. В ином случае сообщение пользователя отправляется в общий чат.

Я предусмотрел различные ошибки пользователей, например, выбор ника, который уже существует, выбор ника, который начинается со специального символа, посылка пустого обращения, обращение к юзеру, которого не существует. Во всех этих случаях юзеру выводится сообщение о соответствующей ошибке. Пример работы чата можно рассмотреть ниже:
![image](https://user-images.githubusercontent.com/75939271/149849842-5db88406-71e6-406d-89ed-9e7ce6ded7dd.png)
