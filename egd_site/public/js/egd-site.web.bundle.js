
// import '../template/js/waypoints.min'
alert('TODO: waypoints necesario!?')

import '../template/js/jquery.easing.min'
import { default as wow } from '../template/js/wow'
window.WOW = wow.WOW

import '../template/js/jquery.slicknav' 

let frappe = window.frappe

alert('TODO: países traducidos en contacto¿?¿? necesario!?')
// import isoCountriesLanguages from '@hotosm/iso-countries-languages'

frappe.ready(function() {

	// // COUNTRIES TRANSLATED
	// // If not available for actual user language return countries in English
	// let countries = isoCountriesLanguages.getCountries(
	// 	isoCountriesLanguages.getSupportedLangs().indexOf(window.context.lang) > -1 ? window.context.lang : 'en'
	// )
	// let countries_sorted = Object.keys(countries).sort((a, b) => countries[a].localeCompare(countries[b]))
	// $('select.select-countries').each((idx, el) => {
	// 	$.each(countries_sorted, (idx, iso) => {
	// 		$(el).append($('<option></option>').val(iso).html(countries[iso]))
	// 	})
	// })


	$('#preloader').fadeOut()


	// // Sticky Nav
	// $(window).on('scroll', function() {
	// 	if ($(window).scrollTop() > 200) {
	// 		$('.scrolling-navbar').addClass('top-nav-collapse')
	// 	} else {
	// 		$('.scrolling-navbar').removeClass('top-nav-collapse')
	// 	}
	// })


	/*====================================
	slick menu js
	======================================*/
	let logo_path=$('.mobile-menu').data('logo')
	$('#navbarCollapse').slicknav({
		appendTo:'.mobile-menu',
		removeClasses:false,
		label:'',
		closedSymbol:'<i class="lni-chevron-right"><i/>',
		openedSymbol:'<i class="lni-chevron-down"><i/>',
		brand:'<a href="index.html"><img src="'+logo_path+'" class="img-responsive" alt="logo"></a>'
	})


	/* WOW Scroll Spy
	========================================================*/
	let wow = new WOW({
		//disabled for mobile
		mobile: false
	})
	wow.init()


	/* Back Top Link active
	========================================================*/
	let offset = 200
	$(window).scroll(function() {
		if ($(this).scrollTop() > offset) {
			$('.back-to-top').fadeIn(400)
		} else {
			$('.back-to-top').fadeOut(400)
		}
	})

	$('.back-to-top').on('click',function(event) {
		event.preventDefault()
		$('html, body').animate({
			scrollTop: 0
		}, 600)
		return false
	})


	// BS FORM VALIDATIONS
	const FORMS = document.getElementsByClassName('bs-validation')
	// Loop over them and prevent submission
	Array.prototype.filter.call(FORMS, function(form) {
		form.addEventListener('submit', function(event) {
			if (form.checkValidity() === false) {
				event.preventDefault()
				event.stopPropagation()
				$(form).addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
					$(this).removeClass('shake animated')
				})
			}
			form.classList.add('was-validated')
		}, false)
	})

	// TODO: check why js translations are not working
	// const button_message_ok = frappe._('form:submit:sending')
	// const button_message_ko = frappe._('form:submit:error')
	// console.log('button_message_ok', button_message_ok)
	// console.log('button_message_ko', button_message_ko)

	// SUBSCRIBE
	const $newsletter = $('.form-subscribe')
	if ($newsletter.length) {
		const $form = $newsletter.find('form')
		const $submit = $newsletter.find('button')
		const $message_ok = $newsletter.find('.alert-success')
		const $f_email = $newsletter.find('[name="email"]')
		const $f_accepted = $newsletter.find('[name="accepted"]')
		$form.on('submit', function(e) {
			e.preventDefault()
			e.stopPropagation()
			if (e.target.checkValidity() && $f_accepted.val() && validate_email($f_email.val())) {
				$submit.html(window.context.translations.form_submit_sending).attr('disabled', true)
				frappe.call({
					type: 'POST',
					method: 'egd_site.tools.subscribe',
					args: { email: $f_email.val() },
					callback: r => {
						if (!r.exc) {
							$message_ok.show()
							$form.hide()
						} else {
							$submit.html(window.context.translations.form_submit_error).addClass('btn-danger').attr('disabled', false)
							$f_email.val('').attr('disabled', false)
						}
					},
				})
			}
		})
	}


	// CONTACT
	const $contact = $('.form-contact')
	if ($contact.length) {
		const $form = $contact.find('form')
		const $submit = $contact.find('button')
		const $message_ok = $contact.find('.alert-success')
		const $f_press = $contact.find('[name="press"]')
		const $f_email = $contact.find('[name="email"]')
		const $f_fullname = $contact.find('[name="fullname"]')
		const $f_country = $contact.find('[name="country"]')
		const $f_subject = $contact.find('[name="subject"]')
		const $f_message = $contact.find('[name="message"]')
		const $f_accepted = $contact.find('[name="accepted"]')
		$form.on('submit', function(e) {
			e.preventDefault()
			e.stopPropagation()
			if (e.target.checkValidity() && $f_accepted.val() && validate_email($f_email.val())) {
				$submit.html(window.context.translations.form_submit_sending).attr('disabled', true)
				frappe.call({
					type: 'POST',
					method: 'egd_site.tools.contact',
					args: {
						press: $f_press.val(),
						email: $f_email.val(),
						full_name: $f_fullname.val(),
						country_code: $f_country.val(),
						subject: $f_subject.val(),
						message: $f_message.val(),
					},
					callback: r => {
						if (!r.exe && r.message == 'success') {
							$message_ok.show()
							$form.hide()
							frappe.ui.scroll('h1', true, 30)
						} else {
							$submit.html(window.context.translations.form_submit_error).addClass('btn-danger').attr('disabled', false)
							$f_email.val('').attr('disabled', false)
						}
					},
				})
			}
		})
	}


	// REGISTER
	const $register = $('.form-registration')
	if ($register.length) {
		const $form = $register.find('form')
		const $submit = $register.find('button')
		const $message_ok = $register.find('.alert-success')
		const $f_firstname = $register.find('[name="firstname"]')
		const $f_lastname = $register.find('[name="lastname"]')
		const $f_email = $register.find('[name="email"]')
		const $f_country = $register.find('[name="country"]')
		const $f_occupation = $register.find('[name="occupation"]')
		const $f_organization = $register.find('[name="organization"]')
		const $f_title = $register.find('[name="title"]')
		const $f_donation = $register.find('[name="effective_charities_donations_in_usd"]')
		const $f_familiarity = $register.find('[name="familiarity"]')
		const $f_accepted = $register.find('[name="accepted"]')
		$form.on('submit', function(e) {
			e.preventDefault()
			e.stopPropagation()
			if (e.target.checkValidity() && $f_accepted.val() && validate_email($f_email.val())) {
				$submit.html(window.context.translations.form_submit_sending).attr('disabled', true)
				frappe.call({
					type: 'POST',
					method: 'egd_site.tools.registration',
					args: {
						firstname: $f_firstname.val(),
						lastname: $f_lastname.val(),
						email: $f_email.val(),
						country_code: $f_country.val(),
						occupation: $f_occupation.val(),
						organization: $f_organization.val(),
						title: $f_title.val(),
						donation: $f_donation.val(),
						familiarity: $f_familiarity.val() == null ? '' : $f_familiarity.val(),
					},
					callback: r => {
						if (!r.exe && r.message == 'success') {
							$message_ok.show()
							$form.hide()
							frappe.ui.scroll('h1', true, 30)
						} else {
							$submit.html(window.context.translations.form_submit_error).addClass('btn-danger').attr('disabled', false)
							$f_email.val('').attr('disabled', false)
						}
					},
				})
			}
		})
	}


	// COOKIES MESSAGE
	// ga('set', 'allowAdFeatures', false)
	// Edit the tag -> More Settings -> Fields to set -> Add a field -> set Field Name as ‘anonymizeIp’ and its Value ‘true’
	// https://termly.io/resources/articles/google-analytics-gdpr/
	const $cookie_message = $('#cookies-message')
	if ($cookie_message.length) {
		$cookie_message.find('button.refuse').on('click', cookiesUserRefused)
		$cookie_message.find('button.accept').on('click', cookiesUserAccept)
		const cookies = frappe.get_cookie(cookie_consent_name)
		if (['accepted', 'refused'].indexOf(cookies) < 0) {
			$cookie_message.removeClass('hide')
		} else {
		}
	}


	// LEGAL SEE MORE LINKS
	const $legal_read_more_items = $('.legal-read-more-container')
	if ($legal_read_more_items.length) {
		$legal_read_more_items.each(function(key, item) {
			let $item = $(item)
			let $item_text = $item.find('.legal-read-more-text')
			let $item_link = $item.find('.legal-read-more-open')
			$item_link.on('click', function(event) {
				event.preventDefault()
				$item_text.addClass('opened')
				$item_link.hide()
			})
		})
	}

})


// <FRAPPE OVERRIDES
// <Override call from /frappe/public/js/frappe/request.js
frappe.call_cloned = frappe.call.bind({})
frappe.call = function(opts) {
	// Add language to all ajax calls
	opts.args = $.extend({}, opts.args || {}, { '_lang': window.context.lang })
	return frappe.call_cloned(opts)
}
// Override call from /frappe/public/js/frappe/request.js>
// FRAPPE OVERRIDES>




// COOKIES
const cookie_consent_name = 'cookie_consent'
function cookieSet(name, value = '', days = '365') {
	let expires = ''
	if (days) {
		let date = new Date()
		date.setTime(date.getTime() + (days*24*60*60*1000))
		expires = `; expires=${date.toUTCString()}`
	}
	document.cookie = `${name}=${value}${expires}; path=/`
}
function cookiesUserAccept() {
	console.log('cookies accepted!!!')
	cookieSet(cookie_consent_name, 'accepted')
}
function cookiesUserRefused() {
	console.log('cookies refused!!!')
	cookieSet(cookie_consent_name, 'refused')
}
