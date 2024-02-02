const subTotals = document.querySelectorAll('.subTotals');
let total = 0
subTotals.forEach(element => {
  total +=parseFloat(element.getAttribute('data-subtotal'))
});
document.querySelector('.prodOnlyTotal').innerText = 'Product/s cost: Rs.'+total;
document.querySelector('.checkoutTotal').innerText = 'Total cost: Rs.'+total+' + Delivery Charge';

const deliveryCharge = document.querySelector('.deliveryCharge');
let charge = 0
let autualCost = 0
const radioFunction = (district) => {
    let one = ['Bhaktapur', 'Kathmandu', 'Lalitpur']
    let two = ['Morang', 'Sunsari', 'Dhanusa', 'Mahottari', 'Parsa', 'Rautahat', 'Saptari', 'Sarlahi', 'Siraha', 'Dhading', 'Dolakha', 'Kavrepalanchowk', 'Makanwanpur', 'Nuwakot', 'Ramechhap', 'Baglung', 'Gorkha', 'Kaski', 'Nawalpur']
    let three = ['Sindhuli', 'Sindhupalchowk']
    let four = ['Khotang']
    let five = ['Jhapa', 'Lamjung', 'Banke', 'Bardiya', 'Dang', 'Gulmi', 'Kapilvastu', 'Parasi', 'Palpa', 'Pyuthan', 'Achham', 'Baitadi', 'Bajhang', 'Bajura', 'Kailali', 'Kanchanpur']
    let six = ['Ilam', 'Udayapur', 'Bara']
    let seven = ['Bhojpur', 'Dhankuta', 'Okhaldhunga', 'Panchthar', 'Sankhuwasabha', 'Solukhumbu', 'Taplejung', 'Terhathum', 'Doti', 'Darchula', 'Dadeldhura', 'Surkhet', 'Salyan', 'Mugu', 'Kalikot', 'Jumla', 'Jajarkot', 'Humla', 'Dolpa', 'Dailekh', 'Rupandehi', 'Rukum', 'Rolpa', 'Tanahu', 'Syangja', 'Parbat', 'Myagdi', 'Mustang', 'Manang', 'Rasuwa']
    let eight = ['Rukum Paschim']
    if(one.includes(district)){
        deliveryCharge.innerText = 'Delivery Charge: Rs.69'
        charge = 69
    }else if(two.includes(district)){
        deliveryCharge.innerText = 'Delivery Charge: Rs.149'
        charge = 149
    }else if(three.includes(district)){
        deliveryCharge.innerText = 'Delivery Charge: Rs.159'
        charge = 159
    }else if(four.includes(district)){
        deliveryCharge.innerText = 'Delivery Charge: Rs.169'
        charge = 169
    }else if(five.includes(district)){
        deliveryCharge.innerText = 'Delivery Charge: Rs.179'
        charge = 179
    }else if(six.includes(district)){
        deliveryCharge.innerText = 'Delivery Charge: Rs.189'
        charge = 189
    }else if(seven.includes(district)){
        deliveryCharge.innerText = 'Delivery Charge: Rs.199'
        charge = 199
    }else if(eight.includes(district)){
        deliveryCharge.innerText = 'Delivery Charge: Rs.229'
        charge = 229
    }else{
    }
    autualCost = total + charge
    document.querySelector('.checkoutTotal').innerText = 'Total cost: Rs.'+autualCost;
    document.querySelector('#charge').value = charge;
    document.querySelector('#totalcost').value = autualCost;
}

const calpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const num = '1234567890';
const options = [calpha, calpha, calpha, calpha, calpha, num, num, calpha, num, num, num, calpha];
let opt, choose;
let pass = "";
for ( let i = 0; i < 12; i++ ) {
    opt = Math.floor(Math.random() * options.length);
    choose = Math.floor(Math.random() * (options[opt].length));
    pass = pass + options[opt][choose];
    options.splice(opt, 1);
}
document.querySelector('#unique-order-id').value = pass;