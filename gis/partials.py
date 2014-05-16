from tg import expose

@expose('gis.templates.little_partial')
def something(name):
    return dict(name=name)