
"""Useful common constants."""

BASE_URL = "https://www.empleate.gob.es/empleate/open/solrService/select?"

HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}

DEFAULT_FILENAME = 'offers'

# WARNING: This probably won't be used again
# URL_TEMPLATE = "https://www.empleate.gob.es/empleate/open/solrService/select?q.op=AND&rows={}&start={}&facet=true&facet.field=paisF&facet.field=provinciaF&facet.field=categoriaF&facet.field=subcategoriaF&facet.field=origen&facet.field=tipoContratoN&facet.field=noMeInteresa&facet.field=educacionF&facet.limit=7&facet.mincount=1&f.topics.facet.limit=50&json.nl=map&fq=speStateId:1 OR speStateId:4&fl=*, score&q=*&wt=json&json.wrf=jQuery110206334639521193013_1540412324942&_=1540412324943"

# URL_TEMPLATE_SPAIN = "https://empleate.gob.es/empleate/open/solrService/select?q.op=AND&rows={}&start={}&facet=true&facet.field=paisF&facet.field=provinciaF&facet.field=categoriaF&facet.field=subcategoriaF&facet.field=origen&facet.field=tipoContratoN&facet.field=noMeInteresa&facet.field=educacionF&facet.limit=7&facet.mincount=1&f.topics.facet.limit=50&json.nl=map&fq=paisF:\"ESPAÑA\"&fq=speStateId:1 OR speStateId:4&fl=*, score&q=*&wt=json&json.wrf=jQuery110206835888167913868_1540833068137&_=1540833068141"

# URL_TEMPLATE_SPAIN_TODAY = "https://empleate.gob.es/empleate/open/solrService/select?q.op=AND&rows={}&start={}&facet=true&facet.field=paisF&facet.field=provinciaF&facet.field=categoriaF&facet.field=subcategoriaF&facet.field=origen&facet.field=tipoContratoN&facet.field=noMeInteresa&facet.field=educacionF&facet.limit=7&facet.mincount=1&f.topics.facet.limit=50&json.nl=map&fq=paisF:\"ESPAÑA\"&fq=fechaCreacionPortal:[NOW/DAY TO NOW/DAY+1DAY]&fq=speStateId:1 OR speStateId:4&fl=*, score&q=*&wt=json&json.wrf=jQuery110206835888167913868_1540833068137&_=1540833068142"