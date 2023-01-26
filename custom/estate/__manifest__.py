{
    'name': 'Real Estate',
    'depends': ['base',
                'web'
    ],
    'category': 'Real Estate/Brokerage',

    'data': ['views/estate_property_views.xml',
             'views/estate_property_type_views.xml',
             'views/estate_property_tag_views.xml',
             'views/estate_property_offer_views.xml',
             'views/res_users_view.xml',
             'views/estate_menus.xml',
             'security/security.xml',
             'security/ir.model.access.csv'
    ],

    'application': 'True'
}