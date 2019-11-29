# Push уведомления

## Комплект:

   * Django приложение для обработки и отправки уведомлений
   * Файл сервис воркера
   * JQuery плагин для фронтенда

## Использование

###1. Django:

```
#settings.py

CSRF_HEADER_NAME = 'HTTP_X_XSRF_TOKEN'

WEBPUSH_SETTINGS: {
    VAPID_PUBLIC_KEY: your-vapid-public-key,
    VAPID_PRIVATE_KEY: your-vapid-private-key,
    VAPID_ADMIN_EMAIL: your-admin-email,
}
```

VAPID_PUBLIC_KEY необходимо передать на фронтенд и указать в мета теге <meta name="vapid_key" content="your-key">, либо передать в настройках.

```
#project_name/urls.py

urlpatterns = [
    ...
    path('pushes/, include('pushes.urls'))
    path('sw.js', path-to-sw-view),
]

#pushes/urls.py (Урлы приложения)

urlpatterns = [
    ...
    path('subscribe', views.SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe', views.UnSubscribeView.as_view(), name='unsubscribe'),
]
```

###2. JS:

const PushApi = Pushes(options);

Настройки:
{
    // Автоматически показывать всплывающее окно с предложением подписаться
    autoSubsInvite: false,

    // Временная задержка (мс) перед показом окна с предложение подписки (только при включенном автоинвайте)
    subsInviteTimeout: 5000,
    
    // Своя схема адресов на бекенде, по умолчанию см. п.1:
    urls: {
        // адрес до корня api
        root: 'api.com',
        // подписка
        subscribe: '/pushes/subscribe',
        // отписка
        unsubscribe: '/pushes/unsubscribe'
        // Файл сервис воркера
        sw: 'sw.js',
    }

    // Публичный ключ
    vapidKey: 'your-key',

    // Колбек для выполнения после подписки (после действия subscribe)
    // Выполнится только если данные будут успешно отправлены на сервер
    afterSubsCallback: undefined,

    // Колбек для выполнения после отписки (после действия unsubscribe)
    // Выполнится только если данные будут успешно отправлены на сервер
    afterUnSubsCallback: undefined,

    // Колбек выполнится если уже подписан
    // Выполняется независимо от ответа сервера
    callbackIfSubs: undefined;

    // Колбек выполнится если уже подписки еще нет
    // Выполняется независимо от ответа сервера
    callbackIfUnSubs: undefined;
}

Для отправки запросов на сервер нужно подключить [куки](https://github.com/js-cookie/js-cookie куки)

### Зависимости