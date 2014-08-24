# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import config
from gis import model
from gis.model import *
from datetime import datetime, time
from gis.lib.mailchimpsync import GisChimpLists
from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from tgext.crud import EasyCrudRestController
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from tgext.pluggable import app_model


class RootController(TGController):

    admin = AdminController(model, app_model.DBSession, config_type=TGAdminConfig)

    @expose('gis.templates.index')
    def index(self):
        import pprint
        pprint.pprint(TGAdminConfig.default_index_template)
        return dict(page='index')

    @expose()
    def posttest(self):
        return self.post(**{'HOTSPOT_ID': u'942455a9',
                                'LOGIN': u'2013-11-25 16:53:52',
                                'Name': u'daniele',
                                'SURNAME': u'favara',
                                'Email': u'daniele@zeroisp.com'})

    @expose()
    def post(self, *args, **kw):

        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.
        {'HOTSPOT_ID': u'942455a9', 'LOGIN': u'2013-11-25 16:53:52', 'Name': u'daniele', 'Email': u'dfavara@eurobalance.it'}

        gis.redirect = http://mywebsite.com

        """
        hotspot_alias = kw.get('HOTSPOT_ID', 'test01')
        date = kw.get('LOGIN')
        try:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except:
            date = datetime.now()
        name = kw.get('Name')
        email = kw.get('Email')
        surname = kw.get('Surname')
        if email:
            email = email.strip()
            if email:
                try:
                    hs = DBSession.query(model.Hotspot).filter(model.Hotspot.hotspot_alias==hotspot_alias).one()
                except:
                    hs = model.Hotspot()
                    hs.hotspot_alias = hotspot_alias

                hslog = model.Hotspotlog()
                hslog.email = email
                hslog.name= name
                hslog.surname = surname
                hslog.date=date
                hs.logs.append(hslog)
                DBSession.add(hs)
                DBSession.flush()
                gm = GisChimpLists(config)
                mcsource = config.get('gis.source','hotspot')
                mchimp = dict(SOURCE=mcsource,
                                HOTSPOT_ID=hs.hotspot_alias,
                                FNAME=name,
                                LNAME=surname)
                if gm.apikey:
                    """'GROUPINGS': [{u'groups': ['Westfield'],u'name': u'Hotspot'}]"""
                    """
                    mlist, mgroup, mgrouping = DBSession.query(
                            model.MCList, model.MCGroup, model.MCGrouping).filter(
                                and_(model.MCList.mc_list_id==hs.mc_list_id,
                                    model.MCGroup.mc_list_id==hs.mc_list_id,
                                    model.MCGroup.name==mcsource,
                                    model.MCGrouping.mc_group_id==MCGroup.mc_group_id,
                                    model.MCGrouping.name==hs.hotspot_alias2))
                    """
                    mclist = DBSession.query(model.MCList).filter(MCList.mc_list_id==hs.mc_list_id).one()

                    mchimp['GROUPINGS'] = [dict(groups=[hs.hotspot_alias2], name=mcsource)]
                    userinfo = gm.subscribe(email, lid=mclist.id, **mchimp)
                    import pprint
                    pprint.pprint(userinfo)
                else:
                    userinfo = dict(merges=mchimp)
                if userinfo:
                    try:
                        crmobj = DBSession.query(model.Crm).filter(model.Crm.email==email).one()
                    except:
                        crmobj = model.Crm(email=email)
                    crmobj.euid=userinfo.get('euid')
                    crmobj.leid=userinfo.get('leid')
                    for col in ['COMPANY','FNAME','LNAME','GENDER','SOURCE']:
                        if hasattr(crmobj, col.lower()):
                            setattr(crmobj, col.lower(), userinfo['merges'][col])
                    DBSession.add(crmobj)
                    DBSession.flush()


        redirect(config.get('gis.redirect', '/'))
