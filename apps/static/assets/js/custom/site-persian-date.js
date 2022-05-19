
var timeDisplay = document.getElementById("time");
var updatedtime;

//[+]: get reference time from server and update datetime each time refresh pages.
fetch(document.location.origin + '/gettime/', {
    headers:{
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
    }
})
.then(response => {
    return response.json() //Convert response to JSON
})
.then(data => {
    updatedtime = new persianDate(data['system_time']);
    return updatedtime
})


function refreshTime() {
    updatedtime = updatedtime.add('seconds', 1);
    formattedString = updatedtime.format("dddd, DD MMMM YYYY, h:mm:ss a");
    timeDisplay.innerHTML = formattedString;
} 
setInterval(refreshTime, 1000);


