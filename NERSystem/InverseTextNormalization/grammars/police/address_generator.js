var streetNumber = ['25489', '87459', '35478', '15975', '95125', '78965']

var streetName = ['A street', 'B street', 'C street', 'D street', 'E street', 'F street',]

var cityName = ['Riyadh', 'Dammam', 'Jedda', 'Tabouk', 'Makka', 'Maddena', 'Haiel']

var stateName = ['Qassem State', 'North State', 'East State', 'South State', 'West State']

var zipCode = ['28889', '96459', '35748', '15005', '99625', '71465']

function getRandom(input) {
    return input[Math.floor((Math.random() * input.length))];
}

function createAdress() {
    return `${getRandom(streetNumber)}, ${getRandom(streetName)} 
${getRandom(cityName)}
${getRandom(stateName)} 
ZIP - ${getRandom(zipCode)}\n\n`;
}



for (var i = 0; i < 20; i++) {
    var address = createAdress();
    console.log(address);
}
