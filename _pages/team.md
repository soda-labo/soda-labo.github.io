---
title: "Soda Lab - Team"
layout: gridlay
excerpt: "Soda Lab: Team members"
sitemap: false
permalink: /team/
---

# Group Members

 **(2024/09/23) The Soda Lab is currently seeking PhD students for Fall 2025.** If you are interested, please check [here]({{ site.url }}{{ site.baseurl }}/vacancies) for more information!


Jump to [Faculty](#faculty), [Postdoctoral researchers](#postdoctoral-researchers), [PhD students](#phd-students), [visitors](#visitors), or [Alumni](#alumni), .
<!-- [administrative support](#administrative-support) -->

## Faculty
{% assign number_printed = 0 %}
{% for member in site.data.team_members %}

{% assign even_odd = number_printed | modulo: 2 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
  <img src="{{ site.url }}{{ site.baseurl }}/images/teampic/{{ member.photo }}" class="img-responsive" width="25%" style="float: left" />
  <h4>{{ member.name }}</h4>
  <i>{{ member.info }}<br>Email: <{{ member.email }}></i><br/>
  <a href="{{ member.website }}">[Website]</a> <a href="{{ member.google_scholar }}">[Google Scholar]</a><a href="{{ site.url }}{{ site.baseurl }}/downloads/{{member.cv}}">[CV]</a>
  <ul style="overflow: hidden">

  {% if member.number_educ == 1 %}
  <li> {{ member.education1 }} </li>
  {% endif %}

  {% if member.number_educ == 2 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  {% endif %}

  {% if member.number_educ == 3 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  <li> {{ member.education3 }} </li>
  {% endif %}

  {% if member.number_educ == 4 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  <li> {{ member.education3 }} </li>
  <li> {{ member.education4 }} </li>
  {% endif %}

  {% if member.number_educ == 5 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  <li> {{ member.education3 }} </li>
  <li> {{ member.education4 }} </li>
  <li> {{ member.education5 }} </li>
  {% endif %}

  </ul>
</div>

{% assign number_printed = number_printed | plus: 1 %}

{% if even_odd == 1 %}
</div>
{% endif %}

{% endfor %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if even_odd == 1 %}
</div>
{% endif %}

## Postdoctoral Researchers
{% assign number_printed = 0 %}
{% for member in site.data.postdocs %}

{% assign even_odd = number_printed | modulo: 2 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
  {% if member.photo %}<img src="{{ site.url }}{{ site.baseurl }}/images/teampic/{{ member.photo }}" class="img-responsive" width="25%" style="float: left" />{% endif %}
  <h4>{{ member.name }}</h4>
  <i>{{ member.info }}<br>{% if member.email %}email: <{{ member.email }}>{% endif %}</i><br/>
  <a href="{{ member.website }}">[Website]</a> <a href="{{ member.google_scholar }}">[Google Scholar]</a><br/>
  {% if member.research %}<p style="overflow: hidden">Research areas: {{ member.research }}</p>{% endif %}
  <ul style="overflow: hidden">

  {% if member.number_educ == 1 %}
  <li> {{ member.education1 }} </li>
  {% endif %}

  {% if member.number_educ == 2 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  {% endif %}

  {% if member.number_educ == 3 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  <li> {{ member.education3 }} </li>
  {% endif %}

  {% if member.number_educ == 4 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  <li> {{ member.education3 }} </li>
  <li> {{ member.education4 }} </li>
  {% endif %}

  </ul>
</div>

{% assign number_printed = number_printed | plus: 1 %}

{% if even_odd == 1 %}
</div>
{% endif %}

{% endfor %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if even_odd == 1 %}
</div>
{% endif %}



## PhD Students
{% assign number_printed = 0 %}
{% for member in site.data.students %}

{% assign even_odd = number_printed | modulo: 2 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
  {% if member.photo %}<img src="{{ site.url }}{{ site.baseurl }}/images/teampic/{{ member.photo }}" class="img-responsive" width="25%" style="float: left" />{% endif %}
  <h4>{{ member.name }}</h4>
  <i>{{ member.info }}
  <br>{% if member.email %}email: <{{ member.email }}>{% endif %}</i><br/>
  <a href="{{ member.website }}">[Website]</a>
  <ul style="overflow: hidden">

  {% if member.number_educ == 1 %}
  <li> {{ member.education1 }} </li>
  {% endif %}

  {% if member.number_educ == 2 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  {% endif %}

  {% if member.number_educ == 3 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  <li> {{ member.education3 }} </li>
  {% endif %}

  {% if member.number_educ == 4 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  <li> {{ member.education3 }} </li>
  <li> {{ member.education4 }} </li>
  {% endif %}

  </ul>
</div>

{% assign number_printed = number_printed | plus: 1 %}

{% if even_odd == 1 %}
</div>
{% endif %}

{% endfor %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if even_odd == 1 %}
</div>
{% endif %}

## Other Student Collaborators
<div class="row">
<div class="col-sm-8 clearfix">
{% for member in site.data.other_student_collaborators %}
{{ member.name }}
{% endfor %}
</div>
</div>

## Visitors
<div class="row">
<div class="col-sm-8 clearfix">
{% for member in site.data.visitors %}
{{ member.name }}
{% endfor %}
</div>
</div>

<div class="row">
</div>

## Alumni

{% assign number_printed = 0 %}
{% for member in site.data.alumni_members %}

{% assign even_odd = number_printed | modulo: 2 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
  <img src="{{ site.url }}{{ site.baseurl }}/images/teampic/{{ member.photo }}" class="img-responsive" width="25%" style="float: left" />
  <h4>{{ member.name }}</h4>
  <i>{{ member.duration }} <br> Role: {{ member.info }}</i>
  <ul style="overflow: hidden">

  </ul>
</div>

{% assign number_printed = number_printed | plus: 1 %}

{% if even_odd == 1 %}
</div>
{% endif %}

{% endfor %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if even_odd == 1 %}
</div>
{% endif %}


<div class="row">

<div class="col-sm-8 clearfix">
<h4>Postdoctoral Researchers</h4>
{% for member in site.data.alumni_postdoc %}
<a href="{{ member.website }}">{{ member.name }}</a>
{% endfor %}
</div>
</div>

<div class="row">

<div class="col-sm-8 clearfix">
<h4>Visitors</h4>
{% for member in site.data.alumni_visitors %}
{{ member.name }}
{% endfor %}
</div>
</div>

<div class="row">
<div class="col-sm-8 clearfix">
<h4>Graduate students (SMU)</h4>
{% for member in site.data.alumni_grad_smu %}
{{ member.name }}
{% endfor %}
</div>
</div>

<div class="row">
<div class="col-sm-8 clearfix">
<h4>Undergraduate Students (SMU)</h4>
{% for member in site.data.alumni_bsc_smu %}
{{ member.name }}
{% endfor %}
</div>
</div>



<!-- ## Administrative Support -->
<!-- <a href="mailto:Rijsewijk@Physics.LeidenUniv.nl">Ellie van Rijsewijk</a> is helping us (and other groups) with administration. -->
