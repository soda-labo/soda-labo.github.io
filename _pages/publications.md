---
title: "Soda Lab - Publications"
layout: gridlay
excerpt: "Soda Lab -- Publications."
sitemap: false
permalink: /publications/
---


# Publications

<!-- ## Group highlights -->

A list of selected papers in which research team members participated. <br/>
(For a full list see [below](#full-list) or go to Google Scholar ([Jisun An](https://scholar.google.com/citations?user=FYtw3zkAAAAJ&hl=en&oi=sra) and [Haewoon Kwak](https://scholar.google.com/citations?user=dcjrz5MAAAAJ&hl=en&oi=ao)).

{% assign number_printed = 0 %}
{% for publi in site.data.publist %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if publi.highlight == 1 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
 <div class="well">
  <a href="{{ publi.link.url }}"><pubtit>{{ publi.title }}</pubtit></a>
  <img src="{{ site.url }}{{ site.baseurl }}/images/pubpic/{{ publi.image }}" class="img-responsive" width="33%" style="float: left" />
  <p>{{ publi.description }}</p>
  <p><em>{{ publi.authors }}</em></p>
  <p><strong><a href="{{ publi.link.url }}">{{ publi.link.display }}</a></strong></p>
  <p class="text-danger"><strong> {{ publi.news1 }}</strong></p>
  <p> {{ publi.news2 }}</p>
 </div>
</div>

{% assign number_printed = number_printed | plus: 1 %}

{% if even_odd == 1 %}
</div>
{% endif %}

{% endif %}
{% endfor %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if even_odd == 1 %}
</div>
{% endif %}

<p> &nbsp; </p>


## Full List

{% for publi in site.data.publist %}

  <a href="{{ publi.link.url }}"><b>{{ publi.title }} </b></a><br />
  <em>{{ publi.authors }} </em><br />{{ publi.link.display }}<br/>
  {% if publi.news1 %}<b>{{ publi.news1 }}</b><br/>{% endif %}
  {% if publi.news2 %}{{ publi.news2 }}{% endif %}  
{% endfor %}
