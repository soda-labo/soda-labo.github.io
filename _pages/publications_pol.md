---
title: "Soda Lab - Publications"
layout: gridlay
excerpt: "Soda Lab -- Publications."
sitemap: false
permalink: /publications/pol
---


# Publications

<!-- ## Group highlights -->

A list of selected papers in which research team members participated. <br/>
(For a full list see [below](#full-list) or go to Google Scholar ([Jisun An](https://scholar.google.com/citations?user=FYtw3zkAAAAJ&hl=en&oi=sra) and [Haewoon Kwak](https://scholar.google.com/citations?user=dcjrz5MAAAAJ&hl=en&oi=ao)).

<a href="/publications/css"><span class="label label-computational-social-science">computational social science</span></a>
<a href="/publications/cj"><span class="label label-computational-journalism">computational journalism</span></a>
<a href="/publications/"><span class="label label-political-science-selected">political science</span></a>
<a href="/publications/net"><span class="label label-network-science">network science</span></a>
<a href="/publications/game"><span class="label label-game-analytics">game analytics</span></a>
<a href="/publications/ai"><span class="label label-ai-ml-nlp">AI/ML/NLP</span></a>
<a href="/publications/hci"><span class="label label-hci">HCI</span></a><br/>
<a href="/publications/sm"><span class="label label-social-media">social media</span></a> 
<a href="/publications/harm"><span class="label label-online-harm">online harm</span></a> 
<a href="/publications/data"><span class="label label-dataset-tool">dataset/tool</span></a> 
<a href="/publications/bias"><span class="label label-bias-fairness">bias/fairness</span></a> 
<a href="/publications/user"><span class="label label-user-engagement">user engagement</span></a> 

{% assign number_printed = 0 %}
{% for publi in site.data.publist %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if publi.highlight == 1 and publi.tags contains 'political science'%}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
 <div class="well">
  <a href="{{ publi.link.url }}"><pubtit>{{ publi.title }}</pubtit></a>
  {% if publi.tags %}
  {% assign tags = publi.tags | split: ',' %}
  {%- for tag in tags -%}
  <span class="label label-{{tag | downcase | strip | replace: ' ', '-' | replace: '/', '-'}}">{{tag}}</span>
  {% endfor %}
  {% endif %}
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
  {%if publi.tags contains 'political science'%}
  <a href="{{ publi.link.url }}"><b>{{ publi.title }} </b></a><br />
  <em>{{ publi.authors }} </em><br />{{ publi.link.display }}<br/>
  {% if publi.news1 %}<b>{{ publi.news1 }}</b><br/>{% endif %}
  {% if publi.news2 %}{{ publi.news2 }}{% endif %}  
  {% endif %}
{% endfor %}
