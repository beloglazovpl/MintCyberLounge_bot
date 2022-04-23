# TelegramBot для Мята Cyber lounge 
## @MintCyberLounge_bot
### Запуск проекта
Установить `requirements.txt` 
```python
pip install -r requirements.txt
```
Записи о ближайших мероприятиях обновляются еженедельно в файлах `config.py` и `main.py`

Необходимо актуализировать ссылки на Delivery Club, 2gis и альбом с фотографими в VK в файле `main.py`.

---
### **UPDATE**

Добавлена возможность отвечать на сообщения клиента от имени бота.

В файле `config.py` необходимо указать id чата куда будут пересылаться сообщения от клиентов (тому кто будет администрировать).

Для того чтобы узнать свой id чата с ботом, отправьте боту команду
```python
/getchatid
```

Пример получения администратором сообщения от клиента

```python
user Сергей
chat 681481860
status other
text Какой режим работы?
event None
```

Для ответа клиенту пишем боту сообщение в формате

```python
admin chat_id#Текст сообщения
```
Например


```python
admin 681481860#Добрый день! Мы работаем с 10 до 2.
```

Клиенту придет сообщение

```
Добрый день! Мы работаем с 10 до 2.
```