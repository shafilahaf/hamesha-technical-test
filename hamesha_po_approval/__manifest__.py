# -*- coding: utf-8 -*-
{
    'name': "HAMESHA-PO APPROVAL",

    'summary': "Custom Purchase Order Approval Workflow for Hamesha",
    'author': "SHAFILAH",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'purchase', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'security/approval_groups.xml',
        'data/mail_template.xml',
        'wizard/approval_reject_wizard.xml',
        'views/purchase_order_inherit.xml',
        
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

