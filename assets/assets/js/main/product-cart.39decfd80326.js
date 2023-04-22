var Cookie = (name)=>{
    let cookieValue = null;
    if(document.cookie && document.cookie !== ''){
        const cookies = document.cookie.split(";");
        for(let i = 0; i < cookies.length; i++){
            const cookie = cookies[i].trim();
            // does this cookie string begin with the name we want?
            if (cookie.substring(0,name.length + 1)===(name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var token = Cookie('csrftoken');
var ajaxCall = (dict, url, method, onsuccess, onerror)=>{
   
    dict['csrfmiddlewaretoken'] = token 
        $.ajax({
            type:method,
            url:url,
            data:dict,
            success: (response)=>{
                onsuccess(response)
               },
            error:(error)=>{
                onerror(error)
               }
    
        })
    }
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
autoUpdateFields(total)
}
const checkout_cart = $('#carter');

autoUpdateFields=(total)=>{
    document.getElementById('cart-total').innerHTML=`$${total}`;
}

// fetches all items related to the user in the database
const fetchUserCart = ()=>{
    $.ajax({
        type:'GET',
        url:`/user-cart/`,
        success: function(response){
            var data = response.data.data;
            var total = response.data.total;
            console.log(data)
            setTimeout(()=>{
                autoUpdateFields(total)
                data.forEach((el) => {
                    // console.log(data);
                    checkout_cart.append(`<tbody class="cart-products cart-product-${el.id}">
                    <tr>
                        <td>
                            <a href="product-left-sidebar.html">
                                <img src="${el.img}" class=" blur-up lazyload"
                                    alt="${el.name}">
                            </a>
                        </td>
                        <td>
                            <a href="product-left-sidebar.html " class="desc">${el.name}</a>
                            <div class="mobile-cart-content row">
                                <div class="col">
                                    <div class="qty-box">
                                        <div class="input-group">
                                            <span>
                                                <button class="btn minus cart-decrease-item" id="cart-decrease-item" onclick="decreaseUserCart(${el.id},${el.quantity})">-</button>
                                                <span class="item-value" id="cart-quantity-${el.id}">
                                                    ${el.quantity}
                                                </span>
                                                <button class="btn plus cart-increase-item" id="cart-increase-item" onclick="increaseUserCart(${el.id},${el.quantity})" >+</button>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                                <div class="col">
                                    <h2>$${el.price}</h2>
                                </div>
                                <div class="col">
                                    <h2 class="td-color">
                                        <a href="javascript:void(0)">
                                            <i class="fas fa-times"></i>
                                        </a>
                                    </h2>
                                </div>
                            </div>
                        </td>
                        <td>
                            <h2>$${el.price}</h2>
                        </td>
                        <td>
                            <div class="qty-box">
                                <div class="input-group">
                                    <span>
                                        <button class="btn minus cart-decrease-item" onclick="decreaseUserCart(${el.id},${el.quantity})" id="cart-decrease-item">-</button>
                                        <span class="item-value" id="cart-quantity-${el.id}">
                                            ${el.quantity}
                                        </span>
                                        <button class="btn plus cart-increase-item" onclick="increaseUserCart(${el.id},${el.quantity})" id="cart-increase-item">+</button>
                                    </span>
                                </div>
                            </div>
                        </td>
                        <td>
                            <button class="btn remove-from-cart deleter fas fa-times" onclick="removeCart(${el.id})" title="delete" delete-data-id="${el.id}">
                            </button>
                        </td>

                        <td>
                            <h2 class="td-color">$${el.total}</h2>
                        </td>
                    </tr>
                </tbody>`);
                
                });
            },0)
            
        },            
        
        error: function(error){
            console.log(error);
        }
    })
}

//add or  increase the number of product in cart on a buttin click {product-cart.html}
const increaseUserCart = (id,quantity=0)=>{
        var cartt = $(`#cart-quantity-${id}`)
        var quantity = Number(cartt.html());
        console.log(id,quantity)
        var onsuccess = (response)=>{
                        
            if(response.bool !== false){
                var total = response.data.body
                console.log(response.data.info)
                clearCart(total)
                quantity+=1;
                console.log(quantity)
                cartt.html(quantity);             
            }
            console.log(response.data)
        }

        var onerror=(error)=>{console.log(error)}
        ajaxCall({'pk':id,'quantity':1},`/add-to-cart/`,'POST',onsuccess,onerror)  
                   
    
    }

// decrease the number of product in cart on a buttin click {product-cart.html}
const decreaseUserCart = (id)=>{
        var cartt = $(`#cart-quantity-${id}`)
        var quantity = Number(cartt.html());
        quantity-=1;
        console.log(id)
        if (quantity == 0){
           removeCart(id)
        }
        else{
            var success = (response)=>{
                if(response.bool !== false){
                    var total = response.data.body
                    cartt.html(quantity); 
                    clearCart(total)
                    console.log(response.data.info)
                }   
            }
            var error = (error)=>{console.log(error)}
            ajaxCall({'pk':id,'quantity':1},`/minus-cart/`,'POST',success,error)
               
        }
    }
// removes item(s) from the cart when the delete button is clicked
const removeCart = (id)=>{
        var success = (response)=>{
            var total = response.data.info
            console.log(response.data.info)
            clearCart(total)       
       }
       var onerror = (error)=>{
        console.log(error)
       }
       ajaxCall({'csrfmiddlewaretoken':token,'pk':id}, `/remove-cart/`,'POST',success,onerror)
      
}
// clear all items cart
const clear = $("#clear")
clear.click(()=>{
    $.ajax({
        type:'POST',
        url:`/clear-cart/`,
        data:{'csrfmiddlewaretoken':token},
        success: (response)=>{
            alert(response.deleted)
            clearCart();
        },
        error:(error)=>{console.log(error)}

    })
})

fetchUserCart();
