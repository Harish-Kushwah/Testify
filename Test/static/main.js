'{% load static %}'
var hr = parseInt('{{hr}}')
var min = parseInt('{{min}}')
var sec =parseInt('{{sec}}')
console.log(typeof(hr))

    var newTime  = new Date()
    newTime.setDate(newTime.getDate())
    newTime.setHours(newTime.getHours()+0)
    newTime.setMinutes(newTime.getMinutes() + 30)
    newTime.setSeconds(newTime.getSeconds() + 0)
    console.log(newTime)
    var countDownDate = new Date(newTime).getTime();
 var x = setInterval(function(){
    var now = new Date().getTime();
    var distance = countDownDate - now

    var days = Math.floor(distance/(1000*60*60*24))
    var hours = Math.floor((distance%(1000*60*60*24))/(1000*60*60));
    var minutes = Math.floor((distance%(1000*60*60))/(1000*60));
    var seconds = Math.floor((distance%(1000*60))/(1000));
    if(distance>0){
    document.getElementById('days').innerHTML =days 
    document.getElementById('hours').innerHTML =hours 
    document.getElementById('minutes').innerHTML =minutes 
    document.getElementById('seconds').innerHTML =seconds 
    }

 } , 1000)