// dont forget to add a button delay
// using fetch api?
// fetch(url,{
//     method:'POST',
//     credentials : "same-origin",
//     headers:{
//         "X-Requested-With" : "XMLHttpRequest",
//         "X-CSRFToken" : csrftoken
//     },
//     data:{
            // 'pk':clickedId
            // },  
//     .then(response=>response.json())
//     .then(data=>{console.log(data)})

// })

// create a csrf token
// function gets the cart items of a user from a database and places it in the product cart page
const cart_table =$('#cart_table')

// get the buttons for adding and removing from cart 
const add = $("#add-item-to-cart");
const increment = $("#incredecre");
// console.log(increment)
const decrement = $("#decrement-value");

// increase the number of product to be added to the cart on a buttin click {product-detail.html}
increment.click(()=>{
    const quantity_to_add = document.getElementById("incredecre");
    var me = Number(quantity_to_add.value);
    console.log(me)
    me=0
    quantity_to_add.value=me.toString();
    quantity_to_add.innerHTML=me.toString();

})

// decrease the number of product to be added to the cart on a button click {product-detail.html}
decrement.click(()=>{
    const quantity_to_minus = $("#quantity_wanted").val()
    var le = Number(quantity_to_minus);
    le-=1
    if (le < 1){
        $("#quantity_wanted").val('0');
        $("#quantity_wanted").html('0');
    }else{
        $("#quantity_wanted").val(le);
        $("#quantity_wanted").html(le)
    }
})

// clears the item in the cart(css specific)
clearCart = (total)=>{
    $(`.cart-products`).each(function(){
        $(this).css({'display':'none'})
    
})  
$(`.cart-item`).each(function(){
    $(this).css({'display':'none'})

}) 
setTimeout(fetchCartDeskMob,3000);
fetchUserCart(); 
document.getElementById('cart-total').innerHTML=`$${total}`;

}

var form = document.getElementById("search-item")
li = []
$("#search-item").keyup(()=>{
    // console.log(form.value)
    const input_value = $("#search-item").val()
    console.log($("#search-item").val())
    if(input_value==''){console.log('nothing requested')}
    else{
        $.ajax({
            type:'GET',
            url: `/search/${input_value}`,
            success:(response)=>{
                const query = response.query
                console.log(query[1])
                var search_ul = $("#search-item-ul");
                console.log(document.getElementById("search-items-div"))
                $(".search-items-div").css(
                    {'display':'block'}
                )
                
                query.forEach((item)=>{ 
                    console.log(item.name)
                    var check = $(`#${item.id}`)
                    if(check = item.id){
                        console.log('is here already')
                    }
                    else{
                        search_ul.prepend(`<li class="item search-item-li">
                        <a href="blog-list-sidebar-left.html" class="search-item-a" id="${item.id}" title="">${item.name}</a>
                        </li><hr class="search-item-hr">`)
                    }
                    
                    
                  }
                )
               query.length = 0
            },
            error:()=>{}
        })
    }
   
})
$("#search-item").keydown(()=>{
    // console.log(form.value)
    const input_value = $("#search-item").val()
    console.log($("#search-item").val())
    console.log(document.getElementById("search-items-div"))
    // $(".search-items-div").css(
    //     {'display':'none'}
    // )
    
   
})


var fetchCartDeskMob = ()=>{
    $.ajax({
        type:'GET',
        url:`/nav-cart/`,
        success: function(response){
            // console.log("item fetched", response.data)
            var data = response.data;
            setTimeout(()=>{
                data.forEach((el) => {
                    cart_table.prepend(`<li class="cart-item">
                            <div class="media">
                                <img src= "${el.img}"
                                    class="img-fluid blur-up lazyload" alt="${el.name}">
                                <div class="media-body">
                                    <h6>${el.name}</h6>
                                    <div class="qty-with-price">
                                        <span>$${el.price}</span>
                                        
                                        <span>
                                        <button class="btn n-plus cart-increase-item" onclick="increaseUserCart(${el.id},${el.quantity})" id="cart-increase-item">+</button>
                                       
                                        <span class="n-item-value" id="cart-quantity-${el.id}">
                                            ${el.quantity}
                                        </span>
                                        <button class="btn n-minus cart-decrease-item" onclick="decreaseUserCart(${el.id},${el.quantity})" id="cart-decrease-item">-</button>
                                       
                                
                                        </span>
                                    </div>
                                </div>
                                <button type="button" class="btn-close d-block d-md-none"
                                    aria-label="Close">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div
                            </li> `) 
                        });
                    },0)  
                },        

        
        error: function(error){
            console.log("unable to get cart");
        }
    })
}
fetchCartDeskMob();










