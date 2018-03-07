var tripImages = [];

/**
 * Only call this function once you've validated the data from isTripGood
 */
function getTripData(){
    return {
        "name":getName(),
        "cost":getCostNumber(),
        "maxTravelers":getMaxTravelers(),
        "date":getDate(),
        "locations":JSON.stringify(getLocations()),
        "description":getDescription(),
        "images":getImages(),
    }; 
}

/**
 * Displays message to user - this can be updated to use a modal 
 */
function messageToUser(message){
    alert("From page: "+message);
}

/** 
 * loops through all pre-determined trip fields and determines if the fields are legit, else returns false
*/
function isTripGood(){
    return ([nameTest, costTest, travelerNumberTest, dateTest, locationTest, descriptionTest].find(function(func){
        var bool = !func();
        return bool;
    }) === undefined);
}



function dateTest(){
    var date = getDate();
    if (date.length > 0)
        return true;
    return false;
}
function getDate(){
    var raw_date = getNonZeroLengthInputElement("#date");
    if (raw_date.length > 0){
        var dateValue = moment(raw_date,"DD-MMMM-YYYY").format("YYYY-MM-DD");
        return dateValue;
    }
    return "2018/04/18";
}



function locationTest(){
    var c = 0;
    $('#location-list li').each(function(item){
        c++;
    });
    if(c>0)
        return true;
    alert('Your trip is too short! Add something!');
}
function getLocations(){
    var locations = [];
    $('#location-list li').each(function(index){
        var elText = $(this).find('span').text();
        var id = trip.find(function(stop){
            if(stop.address == elText)
                return stop.placeId;
            return false;
        });
        locations.push(id);
    });
    return locations;
}

function getImages(){
    var images = [];
    $('#image-list li').each(function(index){ //each hidden span will have a url to the image
        var elText = $(this).find('span').text();
        images.push(elText);
    });
    return JSON.stringify(images);
}

function validateImage(str){

    var fileExtension = str.replace(/.*\./, "");
    var acceptedExtensions = ['png','jpg','jpeg','bmp','gif','gifv'];
    var testExtension = function(el){
        return fileExtension === el;
    };
    return acceptedExtensions.some(testExtension);
}

function descriptionTest(){
    var desc = getDescription();
    if(desc.length>=0||desc.length<240)
        return true;
    return false;
}
function getDescription(){
    var desc = getNonZeroLengthInputElement("#description");
    return desc;
}



function nameTest(){
    var name = $('#name').val();
    if (name == null || name == 0){
        alert("Title can't be left empty!");
        return false;
    }
    return name.length>0;
}
function getName(){
    return $('#name').val();
}


function costTest(){
    var input = getNonZeroLengthInputElement('#cost');
    if(input.length ==0){
        messageToUser("Your trip needs to cost something! Enter: 0 if you want free");
        return false;
    } else if(input.length>0){
        //logic for all lengths greater than 0
        var num = getCostNumber();
        if(num>=0)
            return true;
        messageToUser("your number is negative or weird issue: "+num);
        return false;
    }
}
function getCostNumber(){
    var input = getNonZeroLengthInputElement('#cost');
    var moneyReg = RegExp("^\\$?(\\d*.?\\d{0,2})$"); //$1.1, 1.1, 1 all valid - $1.1$ is not valid
    return getFloatRegex(moneyReg,input);
}



function travelerNumberTest(){
    var inputStr = getNonZeroLengthInputElement('#maxTravelers');
    var numRegex = RegExp("^(\\d*)$");
    if(getFloatRegex(numRegex,inputStr) >0)
        return true;
    alert('Number of travelers has to be at least 1!');
}
function getMaxTravelers(){
    var inputStr = getNonZeroLengthInputElement('#maxTravelers');
    var numRegex = RegExp("^(\\d*)$");
    return getFloatRegex(numRegex,inputStr);
}


/**
 * takes in Regex object with form .*().* (has to have grouping around desired float) and if doesn't find anything returns -1
 * This function is mostly used for >=0 values
 * NOTE: This grabs the first instance of the regex and does NOT do a /g search
 * @param {*} reg //new RegExp("regexhere")
 * @param {*} input //any string
 */
function getFloatRegex(reg,input){
    if(input)
        if(reg.exec(input).length){
            result = parseFloat(reg.exec(input)[1]); //first group will have $ if present. [1] is only our int
            return result;
        }
    return -1;
}


/**
 * grabs an <input> elements value. If null or empty will return empty string: "" else returns the text
 * @param {*} element //Can be id, class, div, etc
 */
function getNonZeroLengthInputElement(element){
    var val = $(element).val();
    if(val){
        return val;
    }
    return "";
}

/**
 * Grabs an element where .text() can be called. If null or empty will return empty string :"" else returns text
 * @param {*} element //can be id, class, div, etc
 */
function getNonZeroLengthInnerTextElement(element){
    var text = $(element).text();
    if (text){
        return text;
    }
    return "";
}