from __future__ import unicode_literals
import frappe
import datetime


no_cache = 1
# sitemap = 1
# no_breadcrumbs = 1


def get_context(context):
	context["access_granted"] = False
	if ("preview_access" in frappe.local.request.cookies
		and frappe.local.request.cookies["preview_access"] == frappe.local.conf.RESTRICTED_COOKIE_VALUE):
		context["access_granted"] = True


# /api/method/egd_site.acceso.check_code
@frappe.whitelist(allow_guest=True, xss_safe=True)
def check_code(code=""):
	frappe.response["result"] = False
	if not code:
		frappe.response["message"] = "A code is needed"
		return
	else:
		if code == frappe.local.conf.RESTRICTED_CODE:
			expires = datetime.datetime.now() + datetime.timedelta(days=1)
			frappe.local.cookie_manager.set_cookie(
				"preview_access", 
				frappe.local.conf.RESTRICTED_COOKIE_VALUE,
				expires
			)
			frappe.response["result"] = True
		else:
			frappe.local.cookie_manager.delete_cookie(["preview_access"])
			frappe.response["message"] = "Not valid code"
		return
