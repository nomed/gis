import mailchimp
try:
    from tgext.pluggable import app_model
except:
    pass

from gis.model import MCList, MCGroup, MCGrouping

class GisChimpLists(object):
    def __init__(self, config, *args, **kw):
        self.apikey = config.get('gis.mailchimp.apikey')

    def list(self, *args, **kw):
        """
        http://apidocs.mailchimp.com/api/2.0/lists/list.php
        """
        m = mailchimp.Mailchimp(self.apikey)
        ret = m.lists.list()
        return ret

    def batch_subscribe(self, email,double_optin=True, *args, **kw):
        """
        kw => {'CRMUSER_ID': user_id, 'HOTSPOT_ID': 'ca-testme', 'FNAME': 'Daniele', 'LNAME': 'Favara',
                    'mc_language': 'en','send_welcome': True}
        """
        m = mailchimp.Mailchimp(self.apikey)
        kw['send_welcome'] = True
        ret = m.lists.batch_subscribe(
            id=self.lid,
            batch=[
                {
                    'email': {'email': email},
                    'email_type': 'html',
                    'merge_vars': kw,
                },
            ],
            update_existing=True,
            replace_interests=False,
            double_optin=double_optin,
        )
        if len(ret.get('adds')) > 0:
            euid = ret['adds'][0]['euid']
        if len(ret.get('updates')) > 0:
            euid = ret['updates'][0]['euid']
        ret = m.lists.member_info(
                    id=self.lid,
                    emails=[
                        {
                            'euid' : euid
                        }
                    ])

        if len(ret['data']) > 0:
            return ret['data'][0]
        else:
            return {}

    def subscribe(self, email, lid=None, double_optin=False, send_welcome=True, *args, **kw):
        """
        http://apidocs.mailchimp.com/api/2.0/lists/subscribe.php
        """
        m = mailchimp.Mailchimp(self.apikey)

        ret = m.lists.subscribe(
            id=lid,
            email={'email': email},
            email_type = 'html',
            merge_vars = kw,
            update_existing=True,
            replace_interests=False,
            double_optin=double_optin,
            send_welcome=send_welcome
        )
        euid=ret.get('euid')
        ret = m.lists.member_info(
                    id=lid,
                    emails=[
                        {
                            'euid' : euid
                        }
                    ])

        return ret['data'][0]

    def interest_groupings(self, lid=None, *args, **kw):
        """
        kw => {'CRMUSER_ID': user_id, 'HOTSPOT_ID': 'ca-testme', 'FNAME': 'Daniele', 'LNAME': 'Favara',
                    'mc_language': 'en','send_welcome': True}
        """
        m = mailchimp.Mailchimp(self.apikey)

        ret = m.lists.interest_groupings(
            id=lid,
        )

        return ret

class GisChimpSync(object):
    def __init__(self, config, *args, **kw):
        self.apikey = config.get('gis.mailchimp.apikey')
        self.g=GisChimpLists(config)
    def list(self, *args, **kw):
        ret = self.g.list()
        data = ret.get('data')
        for linfo in data:
            id = linfo['id']
            try:
                lobj = app_model.DBSession.query(MCList).filter(MCList.id==id).one()
            except:
                lobj = MCList(id=id)
            for key, val in linfo.iteritems():
                if hasattr(lobj, key):
                    print key, val
                    setattr(lobj, key, val)
            app_model.DBSession.add(lobj)
            ginfos = self.g.interest_groupings(lid=id)
            for ginfo in ginfos:
                gid = ginfo['id']
                gname = ginfo['name']
                try:
                    gobj = app_model.DBSession.query(MCGroup).filter(MCGroup.id==gid).one()
                except:
                    gobj = MCGroup(id=gid)

                gobj.name = gname
                lobj.mc_groups.append(gobj)
                app_model.DBSession.add(gobj)
                for ging in ginfo.get('groups'):
                    import pprint
                    pprint.pprint(ging)
                    gingid = ging['id']
                    gingname = ging['name']
                    try:
                        gingobj = app_model.DBSession.query(MCGrouping).filter(MCGrouping.id==gingid).one()
                    except:
                        gingobj = MCGrouping(id=gingid)
                    gingobj.name = gingname
                    gobj.mc_groupings.append(gingobj)
                    app_model.DBSession.add(gingobj)


if __name__ == "__main__":
    config={}

    config['gis.mailchimp.apikey']='284e52da1d2d07ae7d6dc9da97089947-us8'
    config['gis.mailchimp.lid']='e04a00c507'
    g=GisChimpList(config)
    kw = {'CRMUSER_ID': 1,
            'HOTSPOT_ID': 'ca-testme',
            'FNAME': 'Daniele',
            'LNAME': 'Favara',
            'mc_language': 'en',
            'GROUPINGS': [{u'groups': ['Westfield'],u'name': u'Hotspot'}]
            }
    import pprint
    #pprint.pprint(g.subscribe('daniele@zeroisp.com', double_optin=False, **kw))
    #pprint.pprint(g.interest_groupings())
    #pprint.pprint(g.list())




