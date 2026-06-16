from flask import Blueprint, make_response, url_for, request
from ..models.rss_item import RSSItem
from ..models.destination import Destination
from ..models.promotion import Promotion
from ..models.blog import BlogPost
from datetime import datetime, timezone

bp = Blueprint("rss", __name__)


@bp.route("/rss.xml")
def rss_feed():
    items = RSSItem.query.filter_by(is_active=True).order_by(RSSItem.published_at.desc()).limit(50).all()
    recent_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc()).limit(10).all()
    new_destinations = Destination.query.filter_by(is_active=True).order_by(Destination.created_at.desc()).limit(5).all()

    base_url = request.host_url.rstrip("/")
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    xml_items = []
    for item in items:
        pub = item.published_at.strftime("%a, %d %b %Y %H:%M:%S +0000") if item.published_at else now
        link = item.link or base_url
        xml_items.append(f"""    <item>
      <title><![CDATA[{item.title}]]></title>
      <link>{link}</link>
      <description><![CDATA[{item.description or ""}]]></description>
      <category>{item.category or "news"}</category>
      <pubDate>{pub}</pubDate>
      <guid isPermaLink="false">rtvoyage-rss-{item.id}</guid>
    </item>""")

    for post in recent_posts:
        pub = post.published_at.strftime("%a, %d %b %Y %H:%M:%S +0000") if post.published_at else now
        link = f"{base_url}/blog/{post.slug}"
        xml_items.append(f"""    <item>
      <title><![CDATA[{post.title_fr}]]></title>
      <link>{link}</link>
      <description><![CDATA[{post.excerpt_fr or ""}]]></description>
      <category>article</category>
      <pubDate>{pub}</pubDate>
      <guid isPermaLink="true">{link}</guid>
    </item>""")

    for dest in new_destinations:
        link = f"{base_url}/destinations/{dest.slug}"
        xml_items.append(f"""    <item>
      <title><![CDATA[Nouvelle destination : {dest.name_fr}]]></title>
      <link>{link}</link>
      <description><![CDATA[{dest.short_desc_fr or ""}]]></description>
      <category>destination</category>
      <pubDate>{now}</pubDate>
      <guid isPermaLink="true">{link}</guid>
    </item>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>RT Voyage - Actualités et Destinations</title>
    <link>{base_url}</link>
    <description>Découvrez les dernières nouvelles, destinations et promotions de RT Voyage</description>
    <language>fr-FR</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="{base_url}/rss.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>{base_url}/static/images/logo-rtvoyage.png</url>
      <title>RT Voyage</title>
      <link>{base_url}</link>
    </image>
{chr(10).join(xml_items)}
  </channel>
</rss>"""

    response = make_response(xml)
    response.headers["Content-Type"] = "application/rss+xml; charset=utf-8"
    return response
