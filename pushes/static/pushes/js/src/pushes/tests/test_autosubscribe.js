"usestrict";

var afterSubsCallback = sinon.fake();
var afterUnSubsCallback = sinon.fake();
var callbackIfSubs = sinon.fake();
var callbackIfUnSubs = sinon.fake();

const options = {
    autoSubsInvite: true,
    subsInviteTimeout: 5000,
    urls: {
        root: '',
        subscribe: 'pushes/subscribe',
        unsubscribe: 'pushes/unsubscribe',
        sw: 'sw.js',
    },
    vapidKey: 'BELZF_lFM5NpR27HJr47TGkc8Ix8t3v_Di_2Ii-_p3rrw1TMs-mnNYXZkBVkHw-5a8XWTBzT8sOo12ijL8GF5Jg',
    afterSubsCallback: afterSubsCallback,
    afterUnSubsCallback: afterUnSubsCallback,
    callbackIfSubs: callbackIfSubs,
    callbackIfUnSubs: callbackIfUnSubs,
};

describe("Init Pushes", function() {
    this.timeout(options.subsInviteTimeout+3000);
    it("Call callbackIfUnSubs and afterSubsCallback", (done) => {
        const pushApi = Pushes(options);
        setTimeout(() => {
            assert.equal(true, callbackIfUnSubs.called);
            assert.equal(true, afterSubsCallback.called);
            console.log('here');
            done();
        }, options.subsInviteTimeout+2000);
    });
});