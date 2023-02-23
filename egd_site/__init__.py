# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import copy
import frappe

__version__ = '2.1.1'



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

from frappe.translate import get_translations_from_apps as frappe_load_lang
frappe.translate.get_translations_from_apps = egd_load_lang


def egd_resolve_redirect(path, query_string=None):
	if is_app_for_actual_site():
		requested = frappe.local.request.path
		restricted_to = []

		# Show access password for any host not related to production or local (staging., prod., ...)
		# Allow access to site checker Pulno/0.7 (http://www.pulno.com/bot.html)
		# Allow access to Letsencrypt check
		if site_env() == "preprod" and not path.startswith(".well-known/"):
			user_agent = frappe.local.request.headers.get("User-Agent")
			def is_allowed(user_agent):
				return ("pulno.com/bot.html" in user_agent
					or "letsencrypt.org" in user_agent)
			if not user_agent or not is_allowed(user_agent):
				restricted_to = ["/access"]

		if (restricted_to and requested not in restricted_to
			and not requested.startswith("/api/") and not requested.endswith((".js", ".css"))):
			if (not "preview_access" in frappe.local.request.cookies 
				or frappe.local.request.cookies["preview_access"] != frappe.local.conf.RESTRICTED_COOKIE_VALUE):
				frappe.local.flags.redirect_location = "/access"
				raise frappe.Redirect
	frappe_resolve_redirect(path)

from frappe.website.path_resolver import resolve_redirect as frappe_resolve_redirect
frappe.website.path_resolver.resolve_redirect = egd_resolve_redirect


def not_extend_context_and_metatags_for_actual_path() -> bool:
	# Examples of frappe.local.path: '/'='index', '/app'='app', '/folder/file.js?a=1'='folder/file.js',...
	if (getattr(frappe.local, "path", None)
		and (
			frappe.local.path.startswith("app/")
			or frappe.local.path.startswith("tools/")
			or frappe.local.path in ["printview", "app", "error", "favicon.ico"]
			or frappe.local.path.endswith((".js", ".css"))
		)):
		return True
	return False


from frappe.website.website_components.metatags import MetaTags
frappe_website_website_components_metatags_set_metatags_from_website_route_meta = copy.copy(
	MetaTags.set_metatags_from_website_route_meta)
def ae_MetaTags_set_metatags_from_website_route_meta(self):
	frappe_website_website_components_metatags_set_metatags_from_website_route_meta(self)
	if is_app_for_actual_site():
		if not_extend_context_and_metatags_for_actual_path():
			return

		# # Allow CMS webpages
		# if context.doctype == "Web Page":
		# 	context.template = "templates/web.html"

		# ¡¡PRECAUCIÓN!! Si estás logueado como usuario este idioma será el definido en tu cuenta
		self.tags.language = frappe.local.lang or frappe.db.get_default("lang")
		self.tags.url = frappe.local.request.base_url
		self.tags["og:url"] = self.tags.url

		# If blog image or no default use the "summary_large_image" value
		if self.tags.image:
			self.tags["twitter:card"] = "summary_large_image"
		else:
			self.tags.image = frappe.utils.get_url() + "/assets/egd_site/images/logo-square.png"
			self.tags["twitter:card"] = "summary"

		if not self.tags.title:
			self.tags.title = ""
			if self.context.meta_title:
				self.tags.title = self.context.meta_title
			elif self.context.title:
				self.tags.title = self.context.title
			# Add title suffix except for home
			if self.path != "":
				from frappe import _
				self.tags.title += " | " + _("hero:title")

		if not self.tags.description and self.context.meta_description:
			self.tags.description = self.context.meta_description
MetaTags.set_metatags_from_website_route_meta = ae_MetaTags_set_metatags_from_website_route_meta


# def egd_add_preload_headers(response):
# 	"""Allow externals links preloading"""
# 	frappe_add_preload_headers(response)
# 	if is_app_for_actual_site() and "Link" in response.headers:
# 		response.headers["Link"] = response.headers["Link"].replace("/http", "http")

# from frappe.website.render import add_preload_headers as frappe_add_preload_headers
# frappe.website.render.add_preload_headers = egd_add_preload_headers

# FRAPPE OVERRIDES>
