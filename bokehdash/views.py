from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .BokehApps import boxplot

from bokeh.embed import server_session
from bokeh.util import session_id

@login_required
def home(request):
    return render(
        request,
        'bokehdash/home.html',
    )

@login_required
def boxplot_view(request):
    print(boxplot)
    context = {"graphname": "Boxplot",
               "div": boxplot.div,
               "js": boxplot.js,
               "cdn_js": boxplot.cdn_js,
               "cdn_css": boxplot.cdn_css,
               }
    return render(request, 'bokehdash/boxplot.html', context)

@login_required()
def sliders_view(request):
    # Define bokeh endpoint url
    bokeh_server_url = "%sbokehproxy/sliders" % (request.build_absolute_uri(location='/'))

    # Generate bokeh session token so user can access plot, this is done for all logged in users per the @login_required decorator
    # ensuring only logged in users can view plots

    # Using newer bokeh server_session method vs.  deprecated bokeh.embed.autoload_server
    # Note: session_id.generate_session_id() relies on the presence of BOKEH_SECRET_KEY defined in settings.py via an OS variable
    server_script = server_session(None, session_id=session_id.generate_session_id(), url=bokeh_server_url)

    # Tip: More elaborate permission checks can be made using Django's user system, to generate (or not) bokeh session accesss tokens:
    # if user.is_authenticated() and user.has_perm("bokehdash.change_plot"):
    #     server_session(None, session_id=....)
    # else:
    #     HttpResponseRedirect("You can't see this plot")
    # Tip2: More elaborate permissions checks can also be made with other method decorators @user_passes_test, @permission_required
    # (besides @login_reqired)

    # Proceed with context and response
    context = {"graphname":"Sliders",
               "server_script": server_script,
               }
    return render(request, 'bokehdash/bokeh_server.html', context)


@login_required()
def histogram_view(request):
    bokeh_server_url = "%sbokehproxy/selection_histogram" % (request.build_absolute_uri(location='/'))
    server_script = server_session(None, session_id=session_id.generate_session_id(), url=bokeh_server_url)
    context = {"graphname": "Selection Histogram",
               "server_script": server_script,
               }
    return render(request, 'bokehdash/bokeh_server.html', context)


def view_404(request):
    # make a redirect to homepage
    return redirect('/') # or redirect('name-of-index-url')