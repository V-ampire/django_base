"use strict";


const PushApp = (function (){
    const selectors = {
        pushTogglerId: 'push-toggler',
        pushTogglerContainerId: 'push-toggler-container',
        pushFormId: 'push-form',
        pushFormFailId: 'push-form-fail'
    };
    const api = {
        root: document.querySelector('meta[name="ajax_api_domen"]').content,
        sendPush: '/pushes/push'
    };
    const options = {
        autoSubsInvite: false,
        urls: {
            root: document.querySelector('meta[name="ajax_api_domen"]').content,
            subscribe: '/pushes/subscribe',
            unsubscribe: '/pushes/unsubscribe',
            sw: '/sw.js',
        },
        vapidKey: document.querySelector('meta[name="vapid_key"]').content,
        callbackIfSubs: pushStateOn,
        callbackIfUnSubs: pushStateOff,
    };
    let pushApi;
    let pushState;
    const subStorageKey = 'subscriptionData';

    function saveSubData(subscription) {
        localStorage.setItem(subStorageKey, JSON.stringify(subscription));
    };

    function getSubData() {
        return JSON.parse(localStorage.getItem(subStorageKey));
    };

    function loadEventListeners() {
        // Listen Push toggler change
        $(document).change((e) => {
            if (e.target.id === selectors.pushTogglerId) {
                const action = (e.target.checked) ? 'on' : 'off';
                if (action  === 'on') {
                    try {
                        // get promise
                        const sub = pushApi.subscribe();
                        sub.then((subscription) => {
                            saveSubData(subscription.toJSON());
                        });
                    } catch(err) {
                        console.log(err);
                    };
                    pushStateOn();
                } else if (action === 'off') {
                    try {
                        pushApi.unsubscribe();
                        localStorage.removeItem(subStorageKey);
                    } catch(err) {
                        console.log(err);
                    }
                    pushStateOff();
                };
            }
        });
        // Listen submit push form
        document.getElementById(selectors.pushFormId).addEventListener('submit', (e) => {
            e.preventDefault();
            const message = {
                header: e.target.elements.header.value,
                body: e.target.elements.body.value,
            };
            sendPush(message);
        });
    };

    function pushStateOn() {
        const input = `<input type="checkbox" 
                              data-toggle="toggle" 
                              data-onstyle="dark" 
                              id="${selectors.pushTogglerId}" 
                              checked></input>`;
        document.getElementById(selectors.pushTogglerContainerId).innerHTML = input;
        $('#'+selectors.pushTogglerId).bootstrapToggle()  
        pushState = 'on';
        console.log(`Push is ${pushState}`);
    }

    function pushStateOff() {
        const input = `<input type="checkbox" 
        data-toggle="toggle" 
        data-onstyle="dark" 
        id="${selectors.pushTogglerId}"></input>`;
        document.getElementById(selectors.pushTogglerContainerId).innerHTML = input;
        $('#'+selectors.pushTogglerId).bootstrapToggle()  
        pushState = 'off';
        console.log(`Push is ${pushState}`);
    }

    async function sendPush(message) {
        const subscriptionData = getSubData();
        if (subscriptionData !== null) {
            const data = {
                subscription: subscriptionData,
                message: message,
            };
            const headers = {
                'content-type': 'application/json',
                'X-XSRF-TOKEN': Cookies.get('csrftoken'),
            };
            const res = await fetch(api.root + api.sendPush, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: headers,
                credentials: "include"
            });
            if (res.status >= 400) {
                handleErrors('Ошибка при отправке уведомления :(')
            };
        } else {
            handleErrors('Пуш уведомления кажется отключены :(');
        };
    };

    function handleErrors(err) {
        document.getElementById(selectors.pushFormFailId).textContent = err;
        setInterval(() => {
            document.getElementById(selectors.pushFormFailId).textContent = '';
        }, 5000);
    }

    function init() {
        pushApi = Pushes(options);
        loadEventListeners();
    };

    return {
        init: init,
    }
})();

PushApp.init();