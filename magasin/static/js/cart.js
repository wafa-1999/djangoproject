var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var produitId = this.dataset.produit
		var action = this.dataset.action
		console.log('produitId:', produitId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(produitId, action)
		}else{
			updateUserOrder(produitId, action)
		}
	})
}

function updateUserOrder(produitId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'produitId':produitId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(produitId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[produitId] == undefined){
		cart[produitId] = {'quantity':1}

		}else{
			cart[produitId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[produitId]['quantity'] -= 1

		if (cart[produitId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[produitId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}
