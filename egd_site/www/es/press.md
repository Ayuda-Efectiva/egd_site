---
base_template: templates/web.html
title: Prensa
meta_description: Completa este formulario y te pondremos en contacto con el mejor contacto de prensa para tu país o tu área de interés
sitemap: 1
---

<section>
	<div class="container">
		<div class="row">
			<div class="col-12">
				<div class="section-title-header text-center">
					<h1 class="section-title wow fadeInUp" data-wow-delay="0.2s">{{ _('press:title') }}</h1>
					<p class="wow fadeInDown" data-wow-delay="0.2s">{{ _('press:intro') }}</p>
				</div>
			</div>
		</div>
		<div class="row justify-content-center">
			<div class="col-lg-8 col-md-12 col-xs-12">
				{% set press_form = 1 %}
				{% include "templates/includes/contact.html" %}
			</div>
		</div>
	</div>
</section>
