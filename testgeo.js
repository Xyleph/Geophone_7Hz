//npm install serialport
const SerialPort = require('serialport')
const Readline = require('@serialport/parser-readline')
const jsonfile = require("jsonfile")
const moment     = require('moment');

var portName = '/dev/ttyACM0';  //Ori
//var portName = '/dev/ttyUSB0';
const port = new SerialPort(portName) 
const parser = port.pipe(new Readline({ delimiter: '>' }))
parser.on('data', readSerialData) // emits data after every '>'

var fs = require('fs');
var today = new Date();
console.log(today);

var Vref = new Boolean(0)

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
    if (Vref.valueOf()) {
        console.log("Vref On");
        port.write('(AVPe)');
    }
    else{
        console.log("Vref Off");
        port.write('(AVPd)');               //iCP12B Model Only: Enable Vref+ @ RA3/AN3 pin (max ADC input: 4.096V)
    }
    port.write('(PPAw:aaaaxaxx)');      //Set PortA as analog port
    port.write('(ACMe:abc)');           //Enable Continuous & Multiple ADC Channel (A0-A2)
    //port.write('(PCMe)');               //Enable Digital reading
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
var log_data = '';

setInterval(main_loop, 1000);       //1sec
function main_loop() {
    console.log(rx_count)
    rx_count = 0;
}

setInterval(loop_5sec, 5000);        //5sec 
function loop_5sec() {
    port.write('(TT0r)');            //to allow icp12 continue data streaming
}

setInterval(stop_stream, 15000);
function stop_stream() {
    port.write('(TT0d)');
    console.log('Done')
}

//-----------------------------------------------------
//   Serial Function
//-----------------------------------------------------

var data_a = {}
var data_b = {}
var data_c = {}
var data_d = {}
var data_e = {}
var data_f = {}
var data_g = {}
var payload = {}

function readSerialData(data) {
    rx_data = data + '>';
    rx_data = rx_data.replace('#','');      //remove ack '#'
    //console.log('rx:' + rx_count + ',' + rx_data);
    //Convert hex data into voltage form
    if (Vref.valueOf()) {
        var ch_a    = parseInt(rx_data.substr(rx_data.indexOf("a") + 1, 4), 16) * 0.001;   //without Vref On: * 5 / 4096
        var ch_b    = parseInt(rx_data.substr(rx_data.indexOf("b") + 1, 4), 16) * 0.001;
        var ch_c    = parseInt(rx_data.substr(rx_data.indexOf("c") + 1, 4), 16) * 0.001;
        
    }
    else {
        var ch_a    = parseInt(rx_data.substr(rx_data.indexOf("a") + 1, 4), 16) * (5/4096);
        var ch_b    = parseInt(rx_data.substr(rx_data.indexOf("b") + 1, 4), 16) * (5/4096);
        var ch_c    = parseInt(rx_data.substr(rx_data.indexOf("c") + 1, 4), 16) * (5/4096);
    }
    
    var ch_sat  = parseInt(rx_data.substr(rx_data.indexOf("B") + 4, 1), 16).toString(2)
    var ch_mode = parseInt(rx_data.substr(rx_data.indexOf("C") + 4, 1), 16).toString(2)
    
    data_a[log_count.toString()] = ch_a         //data read on channel A
    data_b[log_count.toString()] = ch_b         //data read on channel B
    data_c[log_count.toString()] = ch_c         //data read on channel C
    data_d[log_count.toString()] = ch_sat[1]    //Saturation signal of channel A
    data_e[log_count.toString()] = ch_sat[2]    //Saturation signal of channel B
    data_f[log_count.toString()] = ch_sat[3]    //Saturation signal of channel C
    data_g[log_count.toString()] = ch_mode[3]   //High/Low sensitivity mode indicator
    
    log_count++;
    if(log_count >= 29900){
        log_count = 0;
        payload = {
            a : data_a,
            b : data_b,
            c : data_c,
            d : data_d,
            e : data_e,
            f : data_f,
            g : data_g
        };
        
        var json = JSON.stringify(payload);
	fs.writeFile(`./payload/${moment().format()}.json`, json, function readFileCallback(err, data){
		if (err){
			console.log(err);
		} else { }});
        
    }
    
    rx_count++;
}
