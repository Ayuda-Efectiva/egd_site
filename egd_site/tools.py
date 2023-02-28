
from __future__ import unicode_literals
import frappe
from frappe import _
from . import site_env


def get_home_page(user:str=""):
	return "index"


def context_extend(context):
	context["site_env"] = site_env()

	lang = frappe.db.get_default("lang")
	langs_enabled_raw = frappe.get_all("Language",
		fields=["language_name", "name"],
		filters={"enabled": 1, "name": ["!=", lang]},
		order_by="modified",
		as_list=True)
	languages = [lang] + [lang[1] for lang in langs_enabled_raw]

	frappe.local.lang = frappe.local.lang or "en"
	context["lang"] = frappe.local.lang
	context["languages"] = languages
	# context["url_lang"] = "" if frappe.local.lang == languages[0] else "/{0}".format(frappe.local.lang)
	context["url_lang"] = "/{0}".format(frappe.local.lang)

	context.ae_path = getattr(frappe.local, "path", "") # u/474
	context.ae_url = frappe.utils.get_url(context.ae_path) # https:...:443/u/474

	path = frappe.local.request.path

	# Below context not needed for JS/CSS
	if not path.endswith((".js", ".css")):

		path_without_language = path
		if path == "/":
			path_without_language = ""
		elif len(path) >= 3 and path[1:3] in languages:
			path_without_language = path[3:]

		context["languages_meta"] = []
		for language in languages:
			# # Main language: "x-default"
			# if language == languages[0]:
			# 	meta_url = "{0}".format(path_without_language)
			# else:
			meta_url = "/{0}{1}".format(language, path_without_language)
			context["languages_meta"].append({
				"code": language,
				"hreflang": "x-default" if language == languages[0] else language,
				"url": frappe.utils.get_url(meta_url),
				"is_home": not path_without_language,
			})

		if not "context" in frappe.local.response:
			frappe.local.response.context = {}

	return context


class EgdPageRenderer:
	def __init__(self, path, status_code=None):
		languages_enabled = { v: k for k, v in frappe.translate.get_lang_dict(enabled_only=True).items()}
		# Default lang
		lang = frappe.db.get_default("lang")
		# Lang based on starting path: en/page
		for l in languages_enabled:
			if path and (l == path or path.startswith(l+"/")):
				lang = l
				break
		# Passed in url lang: [url]?_lang=es
		if frappe.form_dict._lang and frappe.form_dict._lang in languages_enabled:
			lang = frappe.form_dict._lang
		frappe.lang = frappe.local.lang = lang

	def can_render(self):
		return False

	def render(self):
		return None


@frappe.whitelist(allow_guest=True, xss_safe=True)
def subscribe(email):
	from frappe.utils.verified_command import get_signed_params

	url = "{0}?{1}".format(
		frappe.utils.get_url("/api/method/egd_site.tools.confirm_subscription"),
		get_signed_params({"email": email, "_lang": frappe.local.lang})
	)
	messages = (
		_("newsletter:email:body:verify_your_email"),
		url,
		_("newsletter:email:body:click_here_to_verify")
	)
	content = "<p>{0}</p><p><a href=\"{1}\">{2}</a></p>".format(*messages)
	frappe.sendmail(email, subject=_("newsletter:email:subject"),
		content=content, delayed=False)


@frappe.whitelist(allow_guest=True, xss_safe=True)
def confirm_subscription(email):
	from frappe.utils.verified_command import verify_request
	if not email or not verify_request():
		return

	# Default user message
	message = frappe._dict({
		"title": _("newsletter:dialog:title:newsletter_subscription"),
		"html": _('newsletter:dialog:body:error_adding_email_"{0}".').format(email),
		"primary_label": _("dialog:body:go_to_homepage"),
	})

	group_name = "EGD Newsletter"
	if not frappe.db.exists("Email Group", group_name):
		frappe.get_doc({
			"doctype": "Email Group",
			"title": group_name,
		}).insert(ignore_permissions=True)

	from frappe.sessions import get_geo_from_ip
	country_code = ""
	if frappe.local.request_ip:
		geo = get_geo_from_ip(frappe.local.request_ip)
		if geo and "country" in geo:
			country_code = geo["country"]["iso_code"]

	from frappe.utils import validate_email_address
	email = email.strip()
	email_valid = validate_email_address(email, False)
	if email_valid:
		if not frappe.db.get_value("Email Group Member",
			{"email_group": group_name, "email": email_valid}):
			frappe.get_doc({
				"doctype": "Email Group Member",
				"email_group": group_name,
				"email": email_valid,
				"country": country_code,
				"ip": frappe.local.request_ip,
			}).insert(ignore_permissions=True)
			frappe.get_doc("Email Group", group_name).update_total_subscribers()
			frappe.db.commit()
			message.html=_('newsletter:dialog:body:email_"{0}"_subscribed_ok').format(email)
		else:
			message.html =_('newsletter:dialog:body:email_"{0}"_subscribed_previously').format(email)

	frappe.respond_as_web_page(**message)


@frappe.whitelist(allow_guest=True, xss_safe=True)
def contact(email, full_name, country_code, subject, message, press = 0):
	subject = "{0} ({1}): {2}".format("EGD: PRESS CONTACT" if int(press) else "EGD: USER CONTACT",
	country_code, subject)
	email_to = None
	settings = frappe.get_single("Web Settings")
	for row in settings.contacts_x_country:
		if row.country_code == country_code:
			email_to = row.email

	if not email_to and settings.contact_default:
		email_to = settings.contact_default

	if site_env() == "local":
		email_to = settings.contact_default_local or None

	email = "{0} <{1}>".format(full_name, email)

	if email_to:
		from frappe.utils import now
		if frappe.db.sql("""SELECT COUNT(*) FROM `tabWeb Contact`
			WHERE TIMEDIFF(%s, modified) < '01:00:00'""", now())[0][0] > 500:
			return
		frappe.sendmail(recipients=email_to, sender=email, content=message,
			subject=subject, delayed=False)

	doc = frappe.get_doc({
		"doctype": "Web Contact",
		"email": "-",
		"full_name": "-",
		"country_code": country_code,
		"forwarded_to": email_to,
		"subject": subject,
		"message": message,
		"language": frappe.local.lang,
	})
	doc.insert(ignore_permissions=True)

	return "success"


@frappe.whitelist(allow_guest=True, xss_safe=True)
def registration(firstname, lastname, email, country_code, occupation, organization, title, donation, familiarity):
	doc = frappe.get_doc({
		"doctype": "Web Registration",
		"email": email,
		"firstname": firstname,
		"lastname": lastname,
		"country_code": country_code,
		"occupation": occupation,
		"organization": organization,
		"title": title,
		"donations": int(float(donation)) if donation else 0,
		"familiarity": familiarity,
		"language": frappe.local.lang,
	})
	doc.insert(ignore_permissions=True)

	# <REGISTRO EXCEPTO DÍA DEL EVENTO
	from frappe.utils.verified_command import get_signed_params
	url = "{0}?{1}".format(
		frappe.utils.get_url("/api/method/egd_site.tools.confirm_registration"),
		get_signed_params({"email": email, "_lang": frappe.local.lang})
	)
	messages = (
		_("registration:email:body:verify_your_email"),
		url,
		_("registration:email:body:click_here_to_verify")
	)
	content = "<p>{0}</p><p><a href=\"{1}\">{2}</a></p>".format(*messages)
	frappe.sendmail(email, subject=_("registration:email:subject"),
		content=content, delayed=False)
	# REGISTRO EXCEPTO DÍA DEL EVENTO>

	# <REGISTRO SOLO DÍA DEL EVENTO
	# if frappe.local.lang == "es":
	# 	subject = "Tu enlace para acceder al evento"
	# 	content = """
	# 	<p>Gracias por registrarte para asistir al evento del Día Internacional 
	# 	de la Ayuda Efectiva <strong>esta tarde a las 18:45</strong>.</p>
	# 	<p>Este es el enlace para acceder al evento:</p>
	# 	<p><a href="https://youtu.be/ih70QEf8Scs">https://youtu.be/ih70QEf8Scs</a></p>
	# 	<p>¡Esperamos que te guste el evento!</p>
	# 	"""
	# else:
	# 	subject = "Your link to join the event"
	# 	content = """
	# 	<p>Thank you for registering to attend the International Effective 
	# 	Giving Day event on <strong>today at 6:45 p.m. CET</strong> 
	# 	(<a href="https://time.is/0645pm_30_Nov_2020_in_CET?Effective_Giving_Day">see in your time zone</a>).</p>
	# 	<p>This is the link to join the event:</p>
	# 	<p><a href="https://youtu.be/ih70QEf8Scs">https://youtu.be/ih70QEf8Scs</a></p>
	# 	<p>We hope you will enjoy the event!</p>
	# 	"""
	# frappe.sendmail(email, subject=subject, content=content, delayed=False)
	# REGISTRO SOLO DÍA DEL EVENTO>

	return "success"


@frappe.whitelist(allow_guest=True, xss_safe=True)
def confirm_registration(email):
	from frappe.utils.verified_command import verify_request
	if not verify_request():
		return

	# Default user message
	message = frappe._dict({
		"title": _("registration:dialog:title:registration_subscription"),
		"html": _('registration:dialog:body:error_confirming_your_email.').format(email),
		"primary_label": _("dialog:body:go_to_homepage"),
	})

	fields = ["name", "email_confirmed"]
	registration = frappe.get_value("Web Registration", {"email": email}, fields, as_dict=True)
	if registration.name and not registration.email_confirmed:
		doc = frappe.get_doc("Web Registration", registration.name)
		doc.email_confirmed = 1
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		message.html =_('registration:dialog:body:email_"{0}"_confirmed_ok').format(email)
	elif registration.name and registration.email_confirmed:
		message.html =_('registration:dialog:body:email_"{0}"_confirmed_previously').format(email)

	frappe.respond_as_web_page(
		title=message.title,
		html=message.html,
		primary_label=message.primary_label,
		http_status_code=200
	)
	# frappe.redirect_to_message(
	# 	title=message.title,
	# 	html=message.html
	# )
