"use strict";


function Pushes(options) {
    // default settings
    const opts = {
        autoSubsInvite: false,
        subsInviteTimeout: 5000,
        urls: {
            root: '/',
            subscribe: '/pushes/subscribe',
            unsubscribe: '/pushes/unsubscribe',
            sw: '/sw.js',
        },
        vapidKey: undefined,
        afterSubsCallback: undefined,
        afterUnSubsCallback: undefined,
        callbackIfSubs: undefined,
        callbackIfUnSubs: undefined,
    };

    let sw;
    let subscriptionData;

    // merge default and custom settings
    if (options) {
        mergeObjects(opts, options);
    };

    function mergeObjects(targetObj, sourceObj) {
        for (let key in sourceObj) {
            if (sourceObj.hasOwnProperty(key)) {
                targetObj[key] = sourceObj[key];
            };
        };
    };
    
    // Initialize
    if (!opts.vapidKey) {
        throw new Error('Public Vapid key is not defined!');
    }
    function init() {
        registerSw();
    };

    function urlB64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');
    
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        const outputData = outputArray.map((output, index) => rawData.charCodeAt(index));
    
        return outputData;
    };

    async function registerSw() {
        // Check browser supports push before to init
        // after gegister sw call initializeState() with registration data
        if ('serviceWorker' in navigator) {
            const reg = await navigator.serviceWorker.register(opts.urls.root+opts.urls.sw);
            sw = reg;
            initialiseState();
        } else {
            // Do smth when sw or push not supported
            showNotAllowed('Service Worker is not supported :(');
        };
    };

    function initialiseState() {
        if (!sw) {
            showNotAllowed('Service Worker is not supported :(');
            return
        }
        // No method to show notifications
        if (!sw.showNotification) {
            showNotAllowed('Showing notifications is not supported :(');
            return
        }
        // Notifications denied
        if (Notification.permission === 'denied') {
            showNotAllowed('You prevented us from showing notifications :(');
            return
        }
        if (!'PushManager' in window) {
            showNotAllowed('Push is not allowed in your browser :(');
            return
        }
        checkSubscribe();
    };

    async function checkSubscribe() {
        const subscription = await sw.pushManager.getSubscription(); // resolve promise which returned reg.pushManager.getSubscription
        if (subscription) {
            // If already subscribed then save data
            // Call callback
            subscriptionData = subscription;
            if (opts.callbackIfSubs) {
                opts.callbackIfSubs();
            }
            return
        };
        // If autosubscribe then call it
        // Call callbacks
        if (opts.autoSubsInvite) {
            setTimeout(() => {
                subscribe();
                if (opts.callbackIfUnSubs) {
                    opts.callbackIfUnSubs();
                };
            }, opts.subsInviteTimeout);
        } else {
            if (opts.callbackIfUnSubs) {
                opts.callbackIfUnSubs();
            };
        };
    };

    async function subscribe() {
        const params = {
            userVisibleOnly: true,
            // if key exists, create applicationServerKey property
            ...(opts.vapidKey && {applicationServerKey: urlB64ToUint8Array(opts.vapidKey)})
        };
        try {
            const sub = await sw.pushManager.subscribe(params);
            sendSubData(sub, 'subscribe');
            return sub
        } catch(error) {
            // If subscribe failed show message
            handleErrors(error);
        };
    };

    async function unsubscribe() {
        try {
            const res = subscriptionData.unsubscribe();
            if (res) {
                sendSubData(subscriptionData, 'unsubscribe')
            }
        } catch(error) {
            handleErrors(error);
        }  
    };

    async function sendSubData(subscription, action) {
        if (action === 'subscribe') {
            var actionUrl = opts.urls.subscribe;
            var method = 'POST';
        } else if (action === 'unsubscribe') {
            var actionUrl = opts.urls.unsubscribe;
            var method = 'DELETE';
        } else {
            handleErrors('Wrong action!');
            return
        }
        const browser = navigator.userAgent;
        const data = {
            subscription: subscription.toJSON(),
            browser: browser,
        };
        // If server raise error then afterSubsCallback wont be called
        const res = await fetch(opts.urls.root + actionUrl, {
            method: method,
            body: JSON.stringify(data),
            headers: {
                'content-type': 'application/json',
                'X-XSRF-TOKEN': Cookies.get('csrftoken'),
            },
            credentials: "include"
        });
        handleResponse(res, subscription, action);
    };

    function handleResponse(res, subscription, action) {
        if (res.status >= 400) {
            handleErrors(res.text())
            return
        };
        if (action === 'subscribe') {
            subscriptionData = subscription;
            if (opts.afterSubsCallback) {
                opts.afterSubsCallback();
            }
        } else if (action === 'unsubscribe') {
            subscriptionData = undefined;
            if (opts.afterUnSubsCallback) {
                opts.afterUnSubsCallback();
            }
        } else {
            handleErrors('Wrong action!');
            return
        }
    };

    function handleErrors(error) {
        // FIXME More actions with error
        console.log(error);
    };

    function showNotAllowed(message) {
        // FIXME More actions if sw is not supported
        console.log(message);
    };

    // Init
    init();
    
    // API
    return {
        subscribe: subscribe,
        unsubscribe: unsubscribe,
    };

}