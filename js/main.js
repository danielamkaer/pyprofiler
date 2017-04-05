import Vue from 'vue'
import {Socket,Protocol} from './comm'

let app = new Vue({
    el: '#app',
    data: {
        ib: {}
    }
});

app.ib = {devices: []};

const socket = new Socket('ws://127.0.0.1:8080/ws');

const log = socket.registerProtocol('log');
const report = socket.registerProtocol('report');
const ib = socket.registerProtocol('ib');

ib.on('message', (update) => {
    console.log(update);
    switch (update.update) {
        case 'UPDATE_APPEND':
            var pieces = update.path.split('.');
            var o = app.ib;
            pieces.forEach(p => {
                o = o[p];
            });
            o.push(update.item);
            break;
        case 'UPDATE_SET':
            if (update.path == '') {
                app.ib = update.item;
            }
            break;

    }
});

//report.on('message', (report) => {
//    var dev = app.devices.find(d=>d.name == report.host);
//    if (dev) {
//        if (!(report.port in dev.ports)) {
//            dev.ports.push(report.port);
//        }
//    } else {
//        app.devices.push({
//            name: report.host,
//            ports: [report.port]
//        });
//    }
//});
