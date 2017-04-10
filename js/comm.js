import EventEmitter from 'events'

class Socket {
    constructor(endpoint) {
        this.endpoint = endpoint;
        this.protocols = {};
        this._setupSocket();
    }

    _setupSocket() {
        this.ws = new WebSocket(this.endpoint);
        this.ws.onopen = evt => { console.log("WebSocket connected"); };
        this.ws.onclose = evt => { console.log("WebSocket disconnected"); };
        this.ws.onmessage = evt => this.onMessage(evt);
    }

    onMessage(evt) {
        const msg = JSON.parse(evt.data);
        if (!Array.isArray(msg) || msg.length != 2) {
            console.warn("Don't know what to do with non-array data.");
        }

        const proto = msg[0];
        const data = msg[1];

        if (proto in this.protocols) {
            this.protocols[proto].handleMessage(data);
        } else {
            console.warn("Don't know how to handle protocol: ", proto);
        }
    }

    sendMessage(proto, data) {
        this.ws.send(JSON.stringify([proto, data]));
    }

    isConnected() {
        return this.ws.readyState == this.ws.OPEN;
    }

    registerProtocol(name) {
        const proto = new Protocol(this, name);
        this.protocols[name] = proto;
        return proto;
    }

}
class Protocol extends EventEmitter {
    constructor(socket, name) {
        super();
        this.socket = socket;
        this.name = name;
    }

    handleMessage(data) {
        console.log("proto: ", this.name, " received data.");
        this.emit('message', data);
    }

    sendMessage(data) {
        this.socket.sendMessage(this.name, data);
    }

}
export {
    Socket,
    Protocol
}