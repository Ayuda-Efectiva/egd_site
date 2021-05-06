from __future__ import unicode_literals
import frappe, json, subprocess
from frappe.utils import get_bench_path
from . import site_env


site_app = "egd_site"
path_bench = get_bench_path()
path_site_app = "{0}/apps/{1}/".format(path_bench, site_app)



# Called when pushing to: https://github.com/Ayuda-Efectiva/egd_site
# /api/method/egd_site.deploy.github_site
@frappe.whitelist(allow_guest=True)
def github_site():
	import hashlib
	import hmac

	if "payload" not in frappe.form_dict:
		return { "error": "Call without \"payload\" key" }

	payload = frappe.request.data
	payload_obj = dict()
	github_webhooks_secret = bytes(frappe.local.conf.GITHUB_WEBHOOKS_SECRET, 'latin-1')
	signature = hmac.new(github_webhooks_secret, payload, hashlib.sha1).hexdigest()
	header_signature = frappe.request.headers.get('X-Hub-Signature')
	if header_signature:
		signature_received = header_signature.split('=')[1]
		if hmac.compare_digest(signature, signature_received):
			action = frappe.request.headers.get('X-GitHub-Event')
			payload_obj = json.loads(frappe.form_dict.payload)
			if action == "ping": 
				return "Ping received!"
			elif action == "push":
				if "ref" in payload_obj:
					if payload_obj["ref"] == "refs/heads/develop" and site_env() == "preprod":
						return deploy_site()
					elif payload_obj["ref"] == "refs/heads/master" and site_env() == "prod":
						return deploy_site()
					else:
						return { "error": "Nothing to do: {0} & {1}".format(
							site_env(), payload_obj["ref"]
						) }
				elif frappe.local.conf.maintenance_mode:
					return { "error": "bench in maintenance mode. Try again later..." }
			else:
				return 'no action for "{0}"'.format(action)
		else:
			return { "error": "Mmmm, sorry..." }
	else:
		return { "error": "No header signature" }


def deploy_site():
	app_site_pull()
	return app_site_compile_assets()


def app_site_pull():
	subprocess.check_output(["git", "pull"], cwd=path_site_app)
	# Doubled because weird git pull not working first time
	subprocess.check_output(["git", "pull"], cwd=path_site_app)


def app_site_compile_assets():
	from subprocess import Popen
	cmd = "bench build --app {0} && \
sudo supervisorctl restart frappe-bench-web:frappe-bench-frappe-web && \
bench --site {1} clear-cache && \
bench --site {1} clear-website-cache".format(site_app, frappe.local.site)
	Popen(cmd, shell=True, cwd=path_bench, executable="/bin/bash")
	return { "msg": "{0} app for {1} site {2} assets compiling initialized ok: {3}".format(
		site_app, site_env(), frappe.local.site, cmd) }
