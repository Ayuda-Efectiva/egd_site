# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '2.0.0'



def is_app_for_actual_site() -> bool:
	"""
	When overriding Frappe or other apps methods, it allow us
	to set that specific override to the actual `site app`.
	Used when multi tenancy (multisites) is on.

	:rtype: bool
	"""
	from .hooks import site_app_domains as sites
	return frappe.local.site in sites


def site_env() -> str:
	"""
	Get actual site environment based on domain. 
	Defined into `hooks.py` as `site_app_domains`

	:return: prod|preprod|local
	:rtype: str
	"""
	from .hooks import site_app_domains as sites
	return sites[frappe.local.site] if frappe.local.site in sites else "local"


# <FRAPPE OVERRIDES

# def egd_render_page_by_language(path):
# 	if is_app_for_actual_site():
# 		from frappe.website.render import render_page

# 		translated_languages = frappe.get_hooks("translated_languages_for_website")
# 		user_lang = frappe.translate.get_language(translated_languages)
# 		if not user_lang in translated_languages:
# 			user_lang = "en"

# 		frappe.lang = user_lang
# 		frappe.local.lang = user_lang

# 		if translated_languages and translated_languages.index(user_lang) == 0:
# 			try:
# 				if path and path in ("login", "desk", "app", "access", "message", "unsubscribe", "translations"):
# 					lang_path = path
# 				elif path and path != "index":
# 					lang_path = '{0}/{1}'.format(user_lang, path)
# 				else:
# 					lang_path = user_lang # index

# 				return render_page(lang_path)
# 			except frappe.DoesNotExistError:
# 				return render_page(path)
# 		else:
# 			return render_page(path)
# 	else:
# 		return frappe_render_page_by_language(path)
# from frappe.website.render import render_page_by_language as frappe_render_page_by_language
# frappe.website.render.render_page_by_language = egd_render_page_by_language


def egd_load_lang(lang, apps=None):
	"""Checks `en` too"""
	if is_app_for_actual_site():
		import os
		from frappe.translate import get_translation_dict_from_file
		out = frappe.cache().hget("lang_full_dict", lang, shared=True)
		if not out:
			out = {}
			for app in (apps or frappe.get_all_apps(True)):
				path = os.path.join(frappe.get_pymodule_path(app), "translations", lang + ".csv")
				out.update(get_translation_dict_from_file(path, lang, app) or {})
			frappe.cache().hset("lang_full_dict", lang, out, shared=True)
		return out or {}
	else:
		return frappe_load_lang(lang, apps)

from frappe.translate import load_lang as frappe_load_lang
frappe.translate.load_lang = egd_load_lang


# def egd_resolve_redirect(path):
# 	if is_app_for_actual_site():
# 		requested = frappe.local.request.path
# 		restricted_to = []

# 		# Show access password for any host not related to production or local (staging., prod., ...)
# 		# Allow access to site checker Pulno/0.7 (http://www.pulno.com/bot.html)
# 		# Allow access to Letsencrypt check
# 		if site_env() == "preprod" and not path.startswith(".well-known/"):
# 			user_agent = frappe.local.request.headers.get("User-Agent")
# 			def is_allowed(user_agent):
# 				return ("pulno.com/bot.html" in user_agent
# 					or "letsencrypt.org" in user_agent)
# 			if not user_agent or not is_allowed(user_agent):
# 				restricted_to = ["/access"]

# 		if (restricted_to and requested not in restricted_to
# 			and not requested.startswith("/api/") and not requested.endswith((".js", ".css"))):
# 			if (not "preview_access" in frappe.local.request.cookies 
# 				or frappe.local.request.cookies["preview_access"] != frappe.local.conf.RESTRICTED_COOKIE_VALUE):
# 				frappe.local.flags.redirect_location = "/access"
# 				raise frappe.Redirect
# 	frappe_resolve_redirect(path)

# from frappe.website.redirect import resolve_redirect as frappe_resolve_redirect
# frappe.website.redirect.resolve_redirect = egd_resolve_redirect
# # First import full module `render` to avoid issue when file loading from `bench`
# import frappe.website.render
# frappe.website.render.resolve_redirect = egd_resolve_redirect


def egd_add_metatags(context):
	"""Override `Web Page` Doctype template if CMS page."""
	if is_app_for_actual_site():
		# Allow CMS webpages
		if context.doctype == "Web Page":
			context.template = "templates/web.html"

		# Override metatags
		if not "metatags" in context:
			context.metatags = frappe._dict({})

		context.metatags["lang"] = frappe.local.lang
		context.metatags["url"] = context.url
		context.metatags["og:url"] = context.url

		# If blog image or no default use the "summary_large_image" value
		if "image" in context.metatags and context.metatags["image"]:
			context.metatags["twitter:card"] = "summary_large_image"
		else:
			context.metatags["image"] = frappe.utils.get_url() + "/assets/egd_site/images/logo-square.png"
			context.metatags["twitter:card"] = "summary"

		if not "title" in context.metatags:
			context.metatags["title"] = ""
			if "meta_title" in context:
				context.metatags["title"] = context["meta_title"]
			elif context.title:
				context.metatags["title"] = context.title
			# Add title suffix except for home
			if context["path"] != "":
				from frappe import _
				context.metatags["title"] += " | " + _("hero:title")

		if not "description" in context.metatags and "meta_description" in context:
			context.metatags["description"] = context["meta_description"]
	frappe_add_metatags(context)
from frappe.website.context import add_metatags as frappe_add_metatags
frappe.website.context.add_metatags = egd_add_metatags


def egd_add_preload_headers(response):
	"""Allow externals links preloading"""
	frappe_add_preload_headers(response)
	if is_app_for_actual_site() and "Link" in response.headers:
		response.headers["Link"] = response.headers["Link"].replace("/http", "http")

from frappe.website.render import add_preload_headers as frappe_add_preload_headers
frappe.website.render.add_preload_headers = egd_add_preload_headers

# FRAPPE OVERRIDES>
