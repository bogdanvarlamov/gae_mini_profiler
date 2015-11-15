Google App Engine Mini Profiler
===============================

gae\_mini\_profiler is a quick drop-in WSGI app that provides ubiquitous
profiling of your existing GAE projects. It exposes RPC statistics and
CPU profiling output for users of your choosing on your production site.
Only requests coming from users of your choosing will be profiled, and
others will not suffer any performance degradation, so you can use this
profiler to learn about production performance without stressing about
slowing users down. See screenshots and features below.

This project is heavily inspired by the Stack Exchange team's impressive
`mini-profiler <http://miniprofiler.com/>`__.

-  See it in action
-  Screenshots
-  Getting Started
-  Features
-  Dependencies
-  Bonus
-  FAQ

See it in action
----------------

Play around with a demo App Engine applications with gae\_mini\_profiler
enabled at
`http://mini-profiler.appspot.com <http://mini-profiler.appspot.com/>`__.

Screenshots
-----------

All profiled pages have total milliseconds in corner, which can be
expanded... ...to show more details... ...about remote procedure call
performance... ...or CPU profiler output. Choose between an instrumented
CPU profiler (above) or a sampling profiler (below). Ajax requests and
redirects are also profiled and added to the corner of your page. Any
Python logging module output is also available for easy access.

Getting Started
---------------

1. Download this repository's source and copy the ``gae_mini_profiler/``
   folder into your App Engine project's root directory.

2. Add the following two handler definitions to ``app.yaml``:

   ::

       handlers:
       - url: /gae_mini_profiler/static
         static_dir: gae_mini_profiler/static
       - url: /gae_mini_profiler/.*
         script: gae_mini_profiler.main.application

3. Modify the WSGI application you want to profile by wrapping it with
   the gae\_mini\_profiler WSGI application.

   ::

       import gae_mini_profiler.profiler
       ...
       application = webapp.WSGIApplication([...])
       application = gae_mini_profiler.profiler.ProfilerWSGIMiddleware(application)

4. Modify your template to include our javascript and stylesheets just
   before your ending body tag.

   There is a profiler\_includes() function in
   gae\_mini\_profiler.templatetags that spits out the right code for
   these scripts and stylesheets.

   Using any template engine of your choice, call this function at the
   end of your template:

   ::

               ...
               {% profiler_includes %}
           </body>
       </html>

   Note that these resources will not be loaded on requests when the
   profiler is disabled, so you don't need to worry about extra HTTP
   requests slowing down your users.

   Using Django? You can register a simple\_tag to expose this to your
   templates:

   ::

       register = template.create_template_register()
       @register.simple_tag
       def profiler_includes():
           return gae_mini_profiler.templatetags.profiler_includes()

   Using jinja2? You can expose this function to your templates easily:

   ::

       webapp2_extras.jinja2.default_config = {
           "globals": {
               "profiler_includes": gae_mini_profiler.templatetags.profiler_includes
           }
       }

   Using anything else to generate your HTML? Just find some way to spit
   the results of profiler\_includes() into your HTML. Doesn't have to
   be anything fancy.

5. You're all set! Now you just need to choose when you want to enable
   the profiler by overriding a simple function. By default it's enabled
   on the dev server and disabled in production. To enable it for App
   Engine admins in production, add the following to
   appengine\_config.py:

   ::

       def gae_mini_profiler_should_profile_production():
               from google.appengine.api import users
               return users.is_current_user_admin()

   In appengine\_config.py you can override both of the following...

   ::

       def gae_mini_profiler_should_profile_production(): pass
       def gae_mini_profiler_should_profile_development(): pass

   ...with any logic you want to choose when the profiler should be
   enabled.

Features
--------

-  Production profiling without impacting normal users
-  Easily profile all requests, including ajax calls
-  Summaries of RPC call types and their performance so you can quickly
   figure out whether datastore, memcache, or urlfetch is your
   bottleneck
-  Redirect chains are tracked -- quickly examine the profile of not
   just the currently rendered request, but any preceding request that
   issued a 302 redirect leading to the current page.
-  Share individual profile results with others by sending link
-  Duplicate RPC calls are flagged for easy spotting in case you're
   repeating memcache or datastore queries
-  Choose from either an instrumented or sampling CPU profiler to
   quickly figure out where your requests are spending time

Dependencies
------------

-  jQuery must be included somewhere on your page.
-  (Optional) If you want the fancy slider selector for the Logs output,
   jQuery UI must also be included with its Slider plugin.

Bonus
-----

gae\_mini\_profiler is currently in production use at `Khan
Academy <http://khanacademy.org>`__. If you make good use of it
elsewhere, please lemme know.

FAQ
---

1. What's the license? `MIT
   licensed <http://en.wikipedia.org/wiki/MIT_License>`__. There is also
   code from the Chromium project's DevTools whose license is at
   static/chrome/inspector/devtools.html.
2. I had my appstats\_RECORD\_FRACTION variable set to 0.1, which means
   only 10% of my queries were getting profiles generated. This meant
   that most of the time gae\_mini\_profiler was failing with a
   javascript error, because the appstats variable was null.

   If you are using appengine\_config.py to customize Appstats behavior
   you should add this to the top of your "appstats\_should\_record"
   method.

   .. raw:: html

      <pre>def appstats_should_record(env):
          from gae_mini_profiler.config import should_profile
          if should_profile(env):
              return True
      </pre>


