# -*- coding: utf-8 -*- 


{
    'name': 'Link Prepress management and MRP Applications',
    'author': 'Soft-integration',
    'application': True,
    'installable': True,
    'auto_install': False,
    'qweb': [],
    'description': False,
    'images': [],
    'version': '1.0.1.24',
    'category': 'Prepress/Manufacturing',
    'demo': [],
    'depends': ['mrp','prepress_management','mrp_maintenance'],
    'data': [
        'views/mrp_production_views.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_routing_views.xml',
        'views/mrp_workorder_views.xml'
    ],
    'license': 'LGPL-3',
}
