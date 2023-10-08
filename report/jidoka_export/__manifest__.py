{
    'name': "jidoka_export",

    'summary': 
        ,

    'description': 
        ,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','product','jidoka_inventory','stock','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'report/shipping_ins.xml',
        'report/packing_list.xml',
        'report/invoice.xml',
        'views/packing_list.xml',
        'views/shipping_ins.xml',
        'views/invoice.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
