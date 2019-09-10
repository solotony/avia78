Vue.use(vueDirectiveTooltip);
new Vue({
	el: ".top-menu",
	data: {
		windows:[false,false,false,false,false],
		menu: false,
		instruction: 1,
		from: [],
		to: [],
		link: [false,false],
		link_0: false,
		link_1: false,
		link_2: false,
		city: 1,
	},
	methods: {
		openWindow: function(e){
			var current_key = e.target.attributes['data-window'].value;
			var key_true = this.windows[current_key];

			this.windows = [false,false,false,false,false];
			if(key_true==false)
			{
				this.windows[current_key] = true;
			}


		},
		windowIsOpened: function(value){
			return this.windows[value];
		},
		openMenu: function(){
			if(this.menu)
			{
				this.menu = false;
			}
			else
			{
				this.menu = true;
			}
		},
		topOrderSearch: function()
		{
			if(document.getElementById('top-order-search').value!="") window.location = "/order/cargo/" + document.getElementById('top-order-search').value;
		},
		topFaqSearch: function()
		{
			if(this.TIMEOUT)
			{
				clearTimeout(this.TIMEOUT);
			}
			this.TIMEOUT = setTimeout(this.topFaqSearchProcess, 1000);
		},
		topFaqSearchProcess: function() {
			document.getElementById('top-faq-search-results').innerHTML = "";
			text = document.getElementById('top-faq-search').value;
			this.link_0 = false;
			this.link_1 = false;
			this.link_2 = false;
			var links = "";
			if(text.length>=5){
				axios.post('/api/search/', "{\"query\":\""+text+"\"}").then(function (response){
					if(response.data.result=='error'||!response.data.length)
					{
						links += "<p>Нет ответов</p>";
						this.link_0 = true;
						this.link_2 = true;
					}
					else {
						response.data.forEach(function (item, i, arr) {
							links += "<p><a href='/news/" + item.fields.slug + "'>" + item.fields.name + "</a></p>";
						});
						this.link_0 = true;
						this.link_1 = true;
						this.link_2 = true;
					}
					document.getElementById('top-faq-search-results').innerHTML = links;
				});
			}
            var timer = 0;
            return function (callback) {
                clearTimeout(timer);
                timer = setTimeout(callback, ms);
            };
        },
		searchForm: function() {
			document.getElementById('search-form').submit();
		},
		setCity: function(city)
		{
			this.city=city;
			this.windows[4]=false;
			document.cookie = 'city='+city+';path=/;';
		},
		getCookie: function(name) {
		  var matches = document.cookie.match(new RegExp(
			"(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
		  ));
		  return matches ? decodeURIComponent(matches[1]) : undefined;
		}
	},
	mounted: function() {
		var from_select = "<option value=''>Страна отправки</option>";
		var to_select = "<option value=''>Страна получения</option>";
		axios.get('/api/from/').then(function (response) {
      			response.data.forEach(function(item, i, arr) {
      					from_select += "<option value='"+item.pk+"'>"+item.fields.title+"</option>"
				});
      			if(document.getElementById("top-order-form-from")) {
					document.getElementById("top-order-form-from").innerHTML = from_select;
				}

		});
		axios.get('/api/to/').then(function (response) {
      			response.data.forEach(function(item, i, arr) {
      					to_select += "<option value='"+item.pk+"'>"+item.fields.title+"</option>"
				});
      			if(document.getElementById("top-order-form-to")) {
					document.getElementById("top-order-form-to").innerHTML = to_select;
				}
		});
		this.city = this.getCookie('city');
		console.log(document.cookie);
	},
})

new Vue({
	el: ".content_block",
	data: {
		instruction: 1,
		prices : new Map([]),
		form_trby : "AIR",
		slides: [
			{
			  title: 'Slide #1',
			  content: 'Slide content.'
			},
  		],
		where_my_order: 0,
		where_my_order2: 0,
	},
	methods: {
		frontOrderSearch: function() {
			if (document.getElementById('front-order-search').value != "") window.location = "/order/cargo/" + document.getElementById('front-order-search').value;
		},
		frontMiniCalc: function() {
			from = document.getElementById('front-mini-calc-from').value;
			to = document.getElementById('front-mini-calc-to').value;
			/*mass = new Map([
				["1-1",[1,500,3,400]],
				["1-2",[2,510,4,401]],
				["1-3",[3,300,5,600]],
				["1-4",[4,600,11,700]],
				["1-5",[4,600,3,700]],
				["1-6",[4,600,10,700]],
			]);
			*/
			mass = this.prices;
			//from = 1;
			if(from&&to&&mass.get(from+"-"+to))
			{
				values = mass.get(from+"-"+to);
				values[0] = values[0]?values[0]:1;
				values[2] = values[2]?values[2]:1;
				if(values[0]) {
					document.getElementById("air_block").innerHTML = "от <span id=\"front-mini-calc-price-1\"></span>, от <span id=\"front-mini-calc-days-1\"></span>";
					day_text = values[0] > 1 ? 'дней' : 'дня';
					document.getElementById('front-mini-calc-days-1').innerHTML = "<b>" + (values[0] ? values[0] : 0) + "</b> " + day_text;
					document.getElementById('front-mini-calc-price-1').innerHTML = "<b>" + (values[1] ? values[1] : 0) + "</b>" + " $/кг";
				}
				else
				{
					document.getElementById("air_block").innerHTML = "<br>";
				}
				if(values[3]) {
					document.getElementById("sea_block").innerHTML = "от <span id=\"front-mini-calc-price-2\"></span>, от <span id=\"front-mini-calc-days-2\"></span>";
					day_text = values[2] > 1 ? 'дней' : 'дня';
					document.getElementById('front-mini-calc-days-2').innerHTML = "<b>" + (values[2] ? values[2] : 0) + "</b> " + day_text;
					document.getElementById('front-mini-calc-price-2').innerHTML = "<b>" + (values[3] ? values[3] : 0) + "</b>" + " $/м<sup>3</sup>";
				}
				else
				{
					document.getElementById("sea_block").innerHTML = "<br><br class=\"mobile-dop-br\">";
				}
			}
			else
			{
				document.getElementById("air_block").innerHTML = "<br>";
				document.getElementById("sea_block").innerHTML = "<br>";

			}
		},
		frontTrby: function(trby){
			if(trby)
			{
				document.getElementById('front-trby-value').value = trby;
				document.getElementById('front-trby-form').submit();
			}
		},
		frontTrby2: function(trby){
			if(trby)
			{
				document.getElementById('form-trby').value = trby;
			}
		},
		changeCountry: function(){
			if(document.getElementById("id_countryFrom")&&document.getElementById("div_id_otherCountryFrom")) {
				if(document.getElementById("id_countryFrom").value==29)
				{
					document.getElementById("div_id_otherCountryFrom").classList.remove("d-none");
				}
				else
				{
					document.getElementById("div_id_otherCountryFrom").classList.add("d-none");
				}
			}

			if(document.getElementById("id_countryTo")&&document.getElementById("div_id_otherCountryTo")) {
				if(document.getElementById("id_countryTo").value==29)
				{
					document.getElementById("div_id_otherCountryTo").classList.remove("d-none");
				}
				else
				{
					document.getElementById("div_id_otherCountryTo").classList.add("d-none");
				}
			}
		}
	},
	mounted: function() {
		var from_select = "<option>Страна отправки</option>";
		var to_select = "<option>Страна доставки</option>";
		axios.get('/api/from/').then(function (response) {
      			response.data.forEach(function(item, i, arr) {
      					selected = "";
						if(item.pk==2)
						{
							//selected = " selected ";
						}
						from_select += "<option value='"+item.pk+"' "+selected+">"+item.fields.title+"</option>"
				});

      			if(document.getElementById("front-mini-calc-from")) {
					document.getElementById("front-mini-calc-from").innerHTML = from_select;
				}
		});
		axios.get('/api/to/').then(function (response) {
      			response.data.forEach(function(item, i, arr) {
      					selected = "";
						if(item.pk==3)
						{
							//selected = " selected ";
						}
						to_select += "<option value='"+item.pk+"' "+selected+">"+item.fields.title+"</option>"
				});

      			if(document.getElementById("front-mini-calc-to")) {
					document.getElementById("front-mini-calc-to").innerHTML = to_select;
				}
		});

		var mass = new Map([]);
		axios.get('/api/prices/').then(function(response){
			response.data.forEach(function(item, i, arr) {
				mass.set(item.fields.c_from+"-"+item.fields.c_to, [item.fields.days_a,item.fields.price_a_kg,item.fields.days_s,item.fields.price_s_kg]);
			});
		});
		this.prices = mass;
		this.frontMiniCalc;

		if(document.getElementById("id_countryFrom")&&document.getElementById("div_id_otherCountryFrom"))
		{
			document.getElementById("id_countryFrom").addEventListener("change", this.changeCountry, false);
			document.getElementById("div_id_otherCountryFrom").classList.add("d-none");
			if(document.getElementById("id_countryFrom").value==29)
			{
				document.getElementById("div_id_otherCountryFrom").classList.remove("d-none");
			}
		}

		if(document.getElementById("id_countryTo")&&document.getElementById("div_id_otherCountryTo"))
		{
			document.getElementById("id_countryTo").addEventListener("change", this.changeCountry, false);
			document.getElementById("div_id_otherCountryTo").classList.add("d-none");
			if(document.getElementById("id_countryTo").value==29)
			{
				document.getElementById("div_id_otherCountryTo").classList.remove("d-none");
			}
		}
	},
})