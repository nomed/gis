import mailchimp


class GisChimp(object):
    def __init__(self, config, *args, **kw):
        self.apikey = config.get('gis.mailchimp.apikey')
        self.lid = config.get('gis.mailchimp.lid')

    def subscribe(self, email, *args, **kw):
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

"""
{u'data': [{u'clients': [],
            u'email': u'daniele@zeroisp.com',
            u'email_type': u'html',
            u'euid': u'5998cbb678',
            u'geo': [],
            u'id': u'5998cbb678',
            u'info_changed': u'2014-08-16 12:39:08',
            u'ip_opt': None,
            u'ip_signup': u'2.36.198.241',
            u'is_gmonkey': False,
            u'language': u'en',
            u'leid': 226874305,
            u'list_id': u'e04a00c507',
            u'list_name': u"Ca'puccino Newsletter",
            u'lists': [],
            u'member_rating': 2,
            u'merges': {u'ADDRESS': u'',
                        u'BIRTHDAY': u'',
                        u'COMPANY': u'',
                        u'CRMUSER_ID': u'1',
                        u'EMAIL': u'daniele@zeroisp.com',
                        u'FNAME': u'Daniele',
                        u'GENDER': u'',
                        u'HOTSPOT_ID': u'ca-testme',
                        u'LNAME': u'Favara',
                        u'SOURCE': u''},
            u'notes': [],
            u'static_segments': [],
            u'status': u'pending', # u'status': u'subscribed',
            u'timestamp': u'',
            u'timestamp_opt': None,
            u'timestamp_signup': u'2014-08-16 12:39:08',
            u'web_id': 226874305}],
 u'error_count': 0,
 u'errors': [],
 u'success_count': 1}
"""


"""
{u'add_count': 1,
 u'adds': [{u'email': u'daniele@zeroisp.com',
            u'euid': u'5998cbb678',
            u'leid': u'226874305'}],
 u'error_count': 0,
 u'errors': [],
 u'update_count': 0,
 u'updates': []}

"""



