//npm install serialport
const SerialPort = require('serialport')
const Readline = require('@serialport/parser-readline')

var portName = '/dev/ttyACM0';  //Ori
//var portName = '/dev/ttyUSB0';
const port = new SerialPort(portName) 
const parser = port.pipe(new Readline({ delimiter: '>' }))
parser.on('data', readSerialData) // emits data after every '>'

var fs = require('fs');
var today = new Date();
console.log(today);
var logger = fs.createWriteStream('./' + today + '.txt', {
    flags: 'a+' // appending (old data will be preserved). The file is created if it does not exist.
})

// list serial ports:
//list_port();
function list_port() {
    SerialPort.list(function (err, ports) {
        ports.forEach(function(port) {
            console.log(port.comName);
        });
    });
}

//-----------------------------------------------------
//   Initialize
//-----------------------------------------------------
function init() {
    port.write('(AVPe)');               //iCP12B Model Only: Enable Vref+ @ RA3/AN3 pin (max ADC input: 4.096V)
    port.write('(PPAw:aaaaxaxx)');      //Set PortA as analog port
    port.write('(ACMe:abc)');           //Enable Continuous & Multiple ADC Channel (A0-A2)
    port.write('(TT0t:496u)');          //Set Continuous timing, 500uSec period
    port.write('(TT0r)');               //Start Data Streaming, repeat every 5 seconds
}
init();

//-----------------------------------------------------
//   Main & Loop Function
//-----------------------------------------------------
var rx_count = 0;
var rx_data = '';
var log_count = 0;

setInterval(main_loop, 1000);       //1sec
function main_loop() {
    //console.log('rx:' + rx_count + ',' + rx_data);
    rx_count = 0;
}

setInterval(loop_5sec, 5000);        //5sec 
function loop_5sec() {
    port.write('(TT0r)');            //to allow icp12 continue data streaming
}

setInterval(loop_30sec, 30000);      //30sec 
function loop_30sec() {
    port.write('(TT0d)');            //stop data streaming after 30sec
    console.log('Streaming Stop');
}

//-----------------------------------------------------
//   Serial Function
//-----------------------------------------------------
function readSerialData(data) {
    rx_data = data + '>';
    rx_data = rx_data.replace('#','');      //remove ack '#'
    //console.log('rx:' + rx_count + ',' + rx_data);
    //Convert hex data into voltage form
    var ch_a = parseInt(rx_data.substr(7, 4), 16) * 0.001;   //without Vref On: * 5 / 4096
    var ch_b = parseInt(rx_data.substr(13, 4), 16) * 0.001;
    var ch_c = parseInt(rx_data.substr(19, 4), 16) * 0.001;

    //log data
    var log_data = 'rx:' + rx_count.toString().padStart(4, '0') + ', a:' + ch_a.toFixed(3) + ', b:' + ch_b.toFixed(3) + ', c:' + ch_c.toFixed(3);
    log_count++;
    if(log_count >= 10000){
        log_count = 0;
        today = new Date();
        logger = fs.createWriteStream('./' + today + '.txt', {
            flags: 'a+' // appending (old data will be preserved). The file is created if it does not exist.
        })
    }
    logger.write(log_data + '\r\n')
    //logger.end() // close string
    console.log(log_data);

    rx_count++;
}
