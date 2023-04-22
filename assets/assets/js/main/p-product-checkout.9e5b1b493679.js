var cook = (name)=>{
    let cookieValue = null;
    if(document.cookie && document.cookie !== ''){
        var cooki = document.cookie.split(";");
        for(let i = 0; i < cooki.length; i++){
            var cookie = cooki[i].trim();
            // does this cookie string begin with the name we want?
            if (cookie.substring(0,name.length + 1)===(name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const tok = cook('csrftoken');
var url = 'http://127.0.0.1:8000'
var payWithPayStack = (data)=>{
    var info = data.payment
    let currency = 'NGN';
    let plan = '';
    let key = data['paystack_public_key']
    let ref = info.ref
    let obj = {
        key:key,
        ref:ref,
        amount:info.amount,
        email : info.email,
        onclose: ()=>{console.log('closed')},
        callback: function(response){
            console.log('successfully paid in')
        }
    }
    if (Boolean(currency)){
        obj.currency = currency.toUpperCase()
      }
      if (Boolean(plan)){
        obj.plan = plan;
      }
    let handler = PaystackPop.setup(obj)
    handler.openIframe();
}
const cardFetchAPI = ()=>{
    // card details
    // const crypto = require(crypto)
    unique_ref = Date.now()
    console.log(unique_ref)
    var cardDetails = {acct_num: $("#acct_num").val(), bank_name: $("#bank_name").val(),acct_email: $("#acct_email").val(),amnt: $("#amnt").val(), unique_ref:unique_ref}
    console.log(cardDetails)
    const card_details = JSON.stringify(cardDetails)
    fetch(`${url}/apipoint/`,{
       method:'POST',
    //    credentials : "same-origin",
       headers:{
        //    "X-Requested-With" : "XMLHttpRequest",
           "X-CSRFToken" : tok,
           'Content-Type' : 'application/json'
       },
       body:card_details
           })
       .then(response=>response.json())
       .then(data=>{
        console.log(data)
        payWithPayStack(data);
    })
}
var ajaxa = (data)=>{
    $.ajax({
        type:'POST',
        url: `{url}/profile/create-address/`,
        data : {'csrfmiddlewaretoken':tok,'data':JSON.stringify(data)},
        success: (response)=>{
            console.log(response.data)
            cardFetchAPI()
        },
        error: ()=>{
            console.log('aya')
        }
    })
}
// toggle visibility for shipping address
$("#same_ship").click(()=>{
    var s = document.getElementById('same_ship');
    var x = document.getElementById('old-ship');
    if(s.checked == true){
        $("#ship_add").hide(1000);
        $("#pull-down2").toggle("d-none")
    }else if(x.checked == true){
        $("#ship_add").hide(1000);
    }
    else{$("#ship_add").show(1000);}
})
// alsos hides the shipping adddress
$("#cc-name").focus(()=>{ $("#ship_add").hide(1000);})
// processes the checkout form 
var checkout_form = $('#checkout_form');
checkout_form.submit((e)=>{
    e.preventDefault();
    var same_ship = document.getElementById('same_ship');
    var datas;
// checks if the user should use same billing address for shipping address
    var x = document.getElementById('old-bill');
    var y = document.getElementById('old-ship');
    if (x.checked==true && y.checked == true){
        cardFetchAPI()
    }

    else if (same_ship.checked == true){
    same_ship = true
    // billing address
    var BillingDetails = {fname: $("#fname").val(),lname: $("#lname").val(),email: $("#email").val(),address: $("#address").val(),address2: $("#address2").val(),country_select: $(".country-select").val(),zip: $("#zip").val(),phone: $("#phone").val(),state_select: $(".state-select").val() ,same_ship: same_ship}
    datas = [BillingDetails]
    ajaxa(datas);
    
    
    }else{ 
        same_ship=false
        var BillingDetails = {fname: $("#fname").val(),lname: $("#lname").val(),email: $("#email").val(),address: $("#address").val(),address2: $("#address2").val(),country_select: $(".country-select").val(),zip: $("#zip").val(),phone: $("#phone").val(),state_select: $(".state-select").val() ,same_ship: same_ship}
            // shipping address
    
        var ShippingDetails = {sfname: $("#sfname").val(),slname: $("#slname").val(),semail: $("#semail").val(),saddress: $("#saddress").val(),saddress2: $("#saddress2").val() ,scountry_select: $(".scountry-select").val(),szip: $("#szip").val(),sphone: $("#sphone").val(),sstate_select: $(".sstate-select").val()}
        datas = [BillingDetails,ShippingDetails]
        ajaxa(datas);
    
    }
    
})
// if the user uses default shipping
function useDefault(type,bool){
    // console.log(`default ${x} being used`)
    $.ajax({
        type : 'POST',
        url: '/process-checkout/',
        data:{'csrfmiddlewaretoken':tok, 'type': `${type}`,'bool':bool},
        success:(response)=>{
            console.log(response.data)
            // y.hide(1000)
        },
        error:(response)=>{
            console.log("error")
        }
    })
}
var bill = $('#old-bill');
var ship = $('#old-ship');
// toggles the billing address if user chooses default billing
bill.click(()=>{
    var bool;
    var x = document.getElementById('old-bill');
    if(x.checked == false){
        bool = false
        useDefault('B',bool);
        $('#bill_add').show(1000)
    }else{
        bool = true
        useDefault('B',bool); 
        $('#bill_add').hide(1000)
    }
   
})
// toggles the billing address if user chooses default shipping
ship.click(()=>{
    var bool;
    var x = document.getElementById('old-ship');
    if(x.checked == false){
        bool = false
        useDefault('S',bool)
    $('#ship_add').show(1000)
    }else{
        bool = true
        useDefault('S',bool);
        $('#ship_add').hide(1000) 
    }
   
})
// fetch the bank details
const fetchBankApi = ()=>{
    fetch(
        'https://api.paystack.co/bank',
        {
            method: 'GET'
        }
    ).then((response)=>response.json()).then(
        (data)=>{
        var dat = data['data']
        dat.forEach(bank =>{
            $('#bank_name').append(`
            <option>${bank['name']}</option>

            
            `)
        })
        }
    )
}
setTimeout(fetchBankApi,2000)

