var getCookie = (name)=>{
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
var csrftoken = getCookie('csrftoken');
var ajaxCall = (dict, url, method, onsuccess, onerror)=>{
// dict = a dictionary containing the required data to be sent to the server(csrf token is omitted)
// url = the url to be used
// type = the method to be used,. GET, POST
// onsuccess = function to run on a successful response
// onerror = function to run when error occurs
dict['csrfmiddlewaretoken'] = csrftoken 
    $.ajax({
        type:method,
        url:url,
        data:dict,
        success: (response)=>{
            onsuccess(response)
        },
        error:(error)=>{onerror(error)}

    })
}

// an ajax call theat loads new item on a button click
var load1 = $("#load-btn1");
const first = $('#first');
let visible = 4;
var getData = ()=>{
    $.ajax({
        type:'GET',
        url:`/hello-world/${visible}/`,
        success: function(response){
            var data = response.data.data;
            var total = response.data.total
            document.getElementById('cart-total').innerHTML=`$${total}`;

            setTimeout(()=>{
                data.forEach(el => {
                    // console.log(data);
                    first.prepend( `
                    <div class="col-xl-3 col-lg-4 col-6">
                    <div class="product-box">
                        <div class="img-wrapper">
                            <a href="/product-detail/${el.id}">
                                <img src= "${el.img}"
                                    class="w-100 bg-img blur-up lazyload" alt="">
                            </a>
                            <div class="circle-shape"></div>
                            <span class="background-text">Parizian</span>
                            <div class="label-block">
                                <span class="label label-theme">30% Off</span>
                            </div>
                            <div class="cart-wrap">
                                <ul>
                                    <li>
                                        <a href="" class="addtocart-btn" data-bs-toggle="modal" onclick="increaseUserCart(${el.id})"
                                            data-bs-target="#addtocart" addtocart-id=${el.id}>
                                            <i data-feather="shopping-bag" class="fas fa-shopping-bag"></i>
                                        </a>
                                    </li>
                                    <li>
                                        <a href="" data-bs-toggle="modal"
                                            data-bs-target="#quick-view">
                                            <i data-feather="eye" class="fas fa-eye"></i>
                                        </a>
                                    </li>
                                    <li>
                                        <a href="compare.html">
                                            <i data-feather="refresh-cw" class="fas fa-refresh-cw"></i>
                                        </a>
                                    </li>
                                    <li>
                                        <a href="wishlist.html" class="wishlist">
                                            <i data-feather="heart" class="fas fa-heart"></i>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="product-style-3 product-style-chair">
                            <div class="product-title d-block mb-0">
                                <p class="font-light mb-sm-2 mb-0">Fully Confirtable</p>
                                <a href="/product-detail/${el.id}" class="font-default">
                                    <h5>${el.name}</h5>
                                </a>
                            </div>
                            <div class="main-price">
                                <ul class="rating mb-1 mt-0">
                                    <li>
                                        <i class="fas fa-star theme-color"></i>
                                    </li>
                                    <li>
                                        <i class="fas fa-star theme-color"></i>
                                    </li>
                                    <li>
                                        <i class="fas fa-star"></i>
                                    </li>
                                    <li>
                                        <i class="fas fa-star"></i>
                                    </li>
                                    <li>
                                        <i class="fas fa-star"></i>
                                    </li>
                                </ul>
                                <h3 class="theme-color">$${el.price}</h3>
                            </div>
                        </div>
                    </div>
                </div>`);
                });
            },0)
            
        },        
        error: function(error){
            console.log(error);
        }
    })
}
    getData()
load1.click(()=>{
    visible +=4;
    getData();
})
