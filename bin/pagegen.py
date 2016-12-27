import os, sys, pages, subprocess, re, optionsgen, config

class HGException(Exception):
  pass
  
def jslist(name, debug):
  ui = pages.UIs[name]
  if debug:
    x = [pages.JS_BASE, ui.get("extra", []), pages.DEBUG, ["debug/ui/frontends/%s" % y for y in ui["uifiles"]]]
    hgid = ""
  else:
    #x = [pages.JS_BASE, ui.get("buildextra", ui.get("extra", [])), pages.BUILD_BASE, name]
    x = [name]
    hgid = "-" + gethgid()  
  
  return list("js/%s%s.js" % (y, hgid) for y in pages.flatten(x))

def csslist(name, debug, gen=False):
  ui = pages.UIs[name]
  nocss = ui.get("nocss")
  if not debug:
    return ["css/%s-%s.css" % (name, gethgid())]
  css = pages.flatten([ui.get("extracss", []), "colours", "dialogs"])
  if not nocss:
    css = list(css) + [name]
  return list("css/%s%s.css" % ("debug/" if gen else "", x) for x in css)

def _gethgid():
  try:
    p = subprocess.Popen(["hg", "id"], stdout=subprocess.PIPE)
  except Exception, e:
    if hasattr(e, "errno") and e.errno == 2:
      raise HGException, "unable to execute"
    raise HGException, "unknown exception running hg: %s" % repr(e)
    
  data = p.communicate()[0]
  if p.wait() != 0:
    raise HGException, "unable to get id"
  return re.match("^([0-9a-f]+).*", data).group(1)

HGID = None
def gethgid():
  global HGID
  if HGID is None:
    try:
      HGID =  _gethgid()
    except HGException, e:
      print >>sys.stderr, "warning: hg: %s (using a random id)." % e
      HGID = os.urandom(10).encode("hex")
  return HGID
    
def producehtml(name, debug):
  ui = pages.UIs[name]
  js = jslist(name, debug)
  css = csslist(name, debug, gen=True)
  csshtml = "\n".join("  <link rel=\"stylesheet\" href=\"%s%s\" type=\"text/css\"/>" % (config.STATIC_BASE_URL, x) for x in css)
  jshtml = "\n".join("  <script type=\"text/javascript\" src=\"%s%s\"></script>" % (config.STATIC_BASE_URL, x) for x in js)

  if hasattr(config, "ANALYTICS_HTML"):
    jshtml+="\n" + config.ANALYTICS_HTML

  div = ui.get("div", "")
  customjs = ui.get("customjs", "")

  return """%s
<!DOCTYPE html>
<html lang="es">
<head>
  <title>%s (qwebirc)</title>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
  <link rel="shortcut icon" type="image/png" href="favicon.png"/>
%s%s
%s
  <link rel="stylesheet" type="text/css" href="assets/css/site.css" />
  <link rel="stylesheet" type="text/css" href="assets/css/prettify.css" />
  <link rel="stylesheet" type="text/css" href="assets/css/font-awesome.css" />
  <script type="text/javascript">
    var ui = new qwebirc.ui.Interface("ircui", qwebirc.ui.%s, %s);
  </script>
</head>
<body>
  <div id="ircui">
    <noscript>
      <div id="noscript">Javascript is required.</div>
    </noscript>%s
  </div>
<div id="webcam">
<img src="%s" id="imagen" class="img-responsive imageClip" onerror="this.src='error.jpg';" />
<audio src="%s" id="audio" autoplay hidden="hidden"  ></audio>
<div><b>%s</b>
<a href="%s" target="_blank" class="btn btn-primary btn-lg">%s</a>
<a href="%s" target="_blank" class="btn btn-success btn-md">%s</a>
<a href="%s" target="_blank" class="btn btn-warning btn-md">%s</a>
<a href="%s" target="_blank" class="btn btn-danger btn-md">%s</a>
<p><span class="glyphicon glyphicon-bitcoin">%s</span>  %s</p>
<a href="http://gln7dm4pgfzax5hc.onion/"><img src="" id="flag" onerror="this.src='images/avatar.png';" /></a>
<a href="https://github.com/porn-libre/my-libre-cam" target="_blank" class="btn btn-danger btn-xs source" ><span class="glyphicon glyphicon-camera"></span> Broadcast Now (alpha 0.1)</a>
</div>
</div>
<script>
function refresh () {setTimeout(function (){$("imagen").src=url_imagen+"?"+Math.random(); refresh(); $("audio").src=$("audio").src + "?" + Math.random(); }, 20000);}
refresh();
var url_imagen=$("imagen").src;
$("flag").src="http://gln7dm4pgfzax5hc.onion/" + window.location.href;
</script>
</body>
</html>
""" % (ui["doctype"], config.APP_TITLE, csshtml, customjs, jshtml, ui["class"], optionsgen.get_options(), div, config.WEBCAM, config.AUDIO, config.TIP, config.TIP0, config.TIP0_MSG, config.TIP1, config.TIP1_MSG, config.TIP2, config.TIP2_MSG, config.TIP3, config.TIP3_MSG, config.BITCOIN_MSG, config.BITCOIN)

def main(outputdir=".", produce_debug=True):
  p = os.path.join(outputdir, "static")
  for x in pages.UIs:
    if produce_debug:
      f = open(os.path.join(p, "%sdebug.html" % x), "wb")
      try:
        f.write(producehtml(x, debug=True))
      finally:
        f.close()
      
    f = open(os.path.join(p, "%s.html" % x), "wb")
    try:
      f.write(producehtml(x, debug=False))
    finally:
      f.close()

if __name__ == "__main__":
  main()
  
