# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from . import __version__ as app_version

app_name = "egd_site"
app_title = "EGD Site"
app_publisher = "Fundación Ayuda Efectiva"
app_description = "Effective Altruism Day Website"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "info@ayudaefectiva.org"
app_license = "MIT"


ASSETS_VERSION = "1.0.1.1"

# Site domains & environment
site_app_domains = {
	"egd.local": "local",
	"effectivegivingday.org": "prod",
	"egd.ayudaefectiva.org": "preprod",
}

translated_languages_for_website = ["en"] #, "de", "es"]
language_default = translated_languages_for_website[0]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/egd_site/css/egd_site.css"
# app_include_js = "/assets/egd_site/js/egd_site.js"

# include js, css files in header of web template
# web_include_css = "/assets/egd_site/css/egd_site.css"
# web_include_js = "/assets/egd_site/js/egd_site.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Guest": "index",
# }

# Website user home page (by function)
get_website_user_home_page = "egd_site.tools.get_home_page"

# Url 301 redirects

website_redirects = [
	{ "source": "/index", "target": "/" },
	{ "source": "/index.html", "target": "/" },
	# Avoid framework contact and about pages being accesible 
	{ "source": "/about", "target": "/" },
	{ "source": "/contact", "target": "/" },
	# # Languages: Remove main language segment. For example,
	# # if "en" is first one in "translated_languages_for_website"
	# # then route "/en/example" will be redirected 301 to "/example"
	# { "source": r"/{0}".format(language_default), "target": "/" },
	# { "source": r"/{0}/(.*)".format(language_default), "target": r"/\1" },
]

# Url rewrites
# IMPORTANT!!! EMPTY CACHE AFTER UPDATING RULES: bench --site all clear-cache
# https://werkzeug.palletsprojects.com/en/1.0.x/routing/#werkzeug.routing.Rule
website_route_rules = [
	{ "from_route": "/sitemap.xml.gz", "to_route": "sitemap.xml" }, # Avoid error with charset as gzip: LookupError: unknown encoding: gzip
]

update_website_context = [
	"egd_site.tools.context_extend",
]

website_context = {
	"ASSETS_VERSION": ASSETS_VERSION,
	"language_default": language_default,
}

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "egd_site.install.before_install"
# after_install = "egd_site.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "egd_site.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_website_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_website_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"egd_site.tasks.all"
# 	],
# 	"daily": [
# 		"egd_site.tasks.daily"
# 	],
# 	"hourly": [
# 		"egd_site.tasks.hourly"
# 	],
# 	"weekly": [
# 		"egd_site.tasks.weekly"
# 	]
# 	"monthly": [
# 		"egd_site.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "egd_site.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "egd_site.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "egd_site.task.get_dashboard_data"
# }

