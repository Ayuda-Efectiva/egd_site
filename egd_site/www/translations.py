from __future__ import unicode_literals
import frappe


no_cache = 1
sitemap = 0


def get_context(context):

	import os
	import io
	# from frappe.translate import get_messages_for_app
	from frappe.translate import deduplicate_messages
	from frappe.translate import get_all_messages_from_js_files
	from frappe.translate import get_messages_from_file
	from frappe.translate import get_translation_dict_from_file
	from csv import writer

	def get_server_messages(app):
		"""Extracts all translatable strings (tagged with `_(`) from Python modules
			inside an app"""
		messages = []
		file_extensions = (".py", ".html", ".js", ".vue", ".md")
		for basepath, folders, files in os.walk(frappe.get_pymodule_path(app)):
			for dontwalk in (".git", "public", "locale", "__pycache__", "translations"):
				if dontwalk in folders: folders.remove(dontwalk)
			for f in files:
				f = frappe.as_unicode(f)
				if f.endswith(file_extensions):
					messages.extend(get_messages_from_file(os.path.join(basepath, f)))
		return messages

	app = "egd_site"
	messages = []
	# # full app messages
	# messages.extend(get_messages_for_app(app))
	# app_include_files
	messages.extend(get_all_messages_from_js_files(app))
	# server_messages
	messages.extend(get_server_messages(app))
	messages = deduplicate_messages(messages)

	ctx_lang = frappe._dict({
		"translated": frappe._dict(),
		"segments_as_txt": frappe._dict(),
	})

	def process_lang(lang):
		path = os.path.join(frappe.get_pymodule_path(app), "translations", lang + ".csv")
		data = get_translation_dict_from_file(path, lang, app)
		ctx_lang["translated"][lang] = data

		mem_file = io.StringIO()
		w = writer(mem_file, lineterminator="\n")
		for p, m, _, _ in messages:
			translated = m
			if (m in ctx_lang["translated"][lang] and ctx_lang["translated"][lang][m] not in [m, ""]):
				translated = ctx_lang["translated"][lang][m]
			# Set english as default language and use it for empty translation segments in other langs
			elif lang != "en" and m in ctx_lang["translated"]["en"]:
				translated = ctx_lang["translated"]["en"][m]
			w.writerow([p if p else '', m, translated])

		raw = mem_file.getvalue()
		ctx_lang["segments_as_txt"][lang] = raw.replace("<", "&lt;").replace(">", "&gt;")

	languages = frappe.get_hooks("translated_languages_for_website")
	if "en" in languages:
		process_lang("en")
		languages.remove("en")

	for lang in languages:
		process_lang(lang)

	context["languages_data"] = ctx_lang
