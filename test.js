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
//  port.write('(ACMe:abc)');           //Enable Continuous & Multiple ADC Channel (A0-A2)
    port.write('(ACMe:abce)');          //Enable Continuous & Multiple ADC Channel (A0-A2,A5)
    port.write('(TT0t:496u)');          //Set Continuous timing, 500uSec period
    port.write('(TT0r)');               //Start Data Streaming, repeat every 5 seconds

//    port.write('(PM2e)');               //Enable PWM2
//    port.write('(PM1e)');               //Enable PWM1

//    port.write('(PM2f:047k)');          //Set PWM2 to 47kHz
//    port.write('(PM1f:047k)');          //Set PWM1 to 47kHz

//    port.write('(PM2r:0512)');          //Set PWM2 to 50% cycle
//    port.write('(PM1r:0512)');          //Set PWM1 to 50% cycle

}
//-----------------------------------------------------
//   Terminate
//-----------------------------------------------------
//function term() {
//   port.write('(PM1d)');               //Disable PWM1
//   port.write('(PM2d)');               //Disable PWM2
//}

init();

//-----------------------------------------------------
//   Main & Loop Function
//-----------------------------------------------------
var rx_count = 0;
var rx_data = '';
var log_count = 0;

setInterval(main_loop, 1000);       //1sec
function main_loop() {
    console.log('rx:' + rx_count + ',' + rx_data);
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
//    term();
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
    var ch_d = parseInt(rx_data.substr(25, 4), 16) * 0.001;

    //log data
    var dje = rx_count.toString().padStart(4, '0');
    var chxa = ch_a.toFixed(3);
    var chxb = ch_b.toFixed(3);
    var chxc = ch_c.toFixed(3);
    var chxd = ch_d.toFixed(3);
    var log_data = 'rx:' + dje + ', a:' + chxa + ', b:' + chxb + ', c:' + chxc + ', d:' + chxd;
    log_count++;

    // if(log_count >= 10000){
    //     log_count = 0;
    //     today = new Date();
    //     logger = fs.createWriteStream('./' + today + '.txt', {
    //         flags: 'a+' // appending (old data will be preserved). The file is created if it does not exist.
    //     })
    // }

    logger.write(log_data + '\r\n')
    //logger.end() // close string
    //console.log(log_data);

    rx_count++;
}
