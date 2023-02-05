---
title: "News"
layout: textlay
excerpt: "Soda Lab at Indiana University Bloomington"
sitemap: false
permalink: /allnews.html
---

# News

{% for article in site.data.news %}
<p>{{ article.date }} <br>
<em>{{ article.headline }}</em></p>
{% endfor %}
