from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": "Registrations & contacts",
			"items": [
				{
					"type": "doctype",
					"name": "Web Registration",
					"label": "Web registrations",
					"onboard": 0,
				},
				{
					"type": "doctype",
					"name": "Web Contact",
					"label": "Web contacts",
					"onboard": 0,
				},
				{
					"type": "doctype",
					"name": "Web Settings",
					"label": "Web Settings",
					"onboard": 0,
				},
			],
		},
		{
			"label": "Emails & Email groups",
			"items": [
				{
					"type": "doctype",
					"name": "Email Group",
					"label": "Email Groups",
					"onboard": 0,
				},
				{
					"type": "doctype",
					"name": "Email Group Member",
					"label": "Email Group Members",
					"onboard": 0,
				},
				{
					"type": "doctype",
					"name": "Email Queue",
					"label": "Email Queue (stop/play)",
					"onboard": 0,
				},
				{
					"type": "doctype",
					"name": "Newsletter",
					"description": "Create and manage newsletter"
				},
			],
		},
		{
			"label": "Exportar & importar",
			"items": [
				{
					"type": "doctype",
					"name": "Data Export",
					"label": "Export (select excel)",
					"onboard": 0,
				},
				{
					"type": "doctype",
					"name": "Data Import",
					"label": "Import",
					"onboard": 0,
				},
			],
		},
		{
			"label": "Setup & logs",
			"items": [
				{
					"type": "doctype",
					"name": "Error Log",
					"description": "Errors in Background Events",
				},
				{
					"type": "page",
					"label": "Background Jobs",
					"name": "background_jobs",
				},
				{
					"type": "doctype",
					"name": "Error Snapshot",
					"description": "A log of request errors",
				},
				{
					"type": "doctype",
					"name": "System Settings",
					"label": "System Settings",
					"description": "Language, Date and Time settings",
				},
				{
					"type": "doctype",
					"name": "Email Account",
					"description": "Add / Manage Email Accounts."
				},
			],
		},
	]
