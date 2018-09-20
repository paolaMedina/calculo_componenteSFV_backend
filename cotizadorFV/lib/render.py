# -*- coding: utf-8 -*-
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from random import randint

##sin descargar el pdf
def render_to_pdf(template_src, context_dict={}):
 template = get_template(template_src)
 html  = template.render(context_dict)
 result = BytesIO()
 pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
 if not pdf.err:
   #return result.getvalue()
    return HttpResponse(result.getvalue(), content_type='application/pdf')
 return HttpResponse("Error Rendering PDF", status=400)
 
 
def render_to_file(path,params,file_name):
  template = get_template(path)
  html = template.render(params)
  result = BytesIO()
  pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
  file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "media/cotizaciones", file_name+".pdf")
  with open(file_path, 'wb') as pdf:
      pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
  return result.getvalue()