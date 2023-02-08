---
base_template: templates/web.html
title: Contacto
meta_description: "Contacta con nosotros: haremos llegar tu email a la persona más adecuada par ayudarte"
sitemap: 1
---

<section>
	<div class="container">
		<div class="row">
			<div class="col-12">
				<div class="section-title-header text-center">
					<h1 class="section-title wow fadeInUp" data-wow-delay="0.2s">{{ _('contact:title') }}</h1>
				</div>
			</div>
		</div>
		<div class="row justify-content-center">
			<div class="col-lg-8 col-md-12 col-xs-12">
				{% include "templates/includes/contact.html" %}
			</div>
		</div>
	</div>
</section>
