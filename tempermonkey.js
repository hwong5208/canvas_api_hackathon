// ==UserScript==
// @name        UBC Canvas API Hackathon Test Post method
// @namespace   all
// @match       https://canvas.ubc.ca/courses/26149
// @require  http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js]
// @requre   https://cdnjs.cloudflare.com/ajax/libs/then-request/2.2.0/request.min.js
// @require  http://crypto.stanford.edu/sjcl/sjcl.js
// @grant    GM_getValue
// @grant    GM_setValue
// @include  http://YOUR_SERVER.COM/YOUR_PATH/*

// @grant    GM_addStyle
// ==/UserScript==


// Create a new section on left-side menu bar
var div = document.createElement('div');
div.innerHTML =
"<h4>Deadline Reminder Setup:</h4><p style = 'font-size =10pt'>Please enter your phone number:</P><input type='tel'id='phoneInput' name='phonenumber' style='height:20px;font-size:10pt;width:120px'/></n><button id='submit_button' >Submit</button><button id='demo_button'>Demo</button>";
var addPhone = document.getElementById("left-side").appendChild(div);
var passNum = $("#phoneInput").val();

// Create submit_button function
$(document).ready(function() {
    $("#submit_button").click(function() {
    var input = $("#phoneInput").val().toString();
    var msg = 'The number that you entered is ' + input +'. ' + 'We are going to send you a reminder 30 mins before the assignment deadlines.';
     alert(msg);

        $.ajax ( {
    type:       'POST',
    url:        'http://127.0.0.1:8000/post_json',
    dataType:   'JSON',
    data: JSON.stringify({ "phone_number": input}) ,
    success: function( data ){
        console.log("post success with number" )
    },
    error: function( errorThrown ){
        console.log( errorThrown );
    }


});
});
});


// Create demon_button function
$(document).ready(function() {
    $("#demo_button").click(function() {
     $.ajax ( {
    type:       'GET',
    url:        'http://127.0.0.1:8000/send_sms',
    dataType:   'JSON',
    success:    function (apiJson) {
        var resultObj = apiJson.items[0];
        alert (
              'User ' + resultObj.display_name
            + ' has accept rate of ' + resultObj.accept_rate + '%.'
        );
    }
} );
});
});
