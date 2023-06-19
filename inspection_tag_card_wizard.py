from odoo import models, fields, api
from datetime import timedelta

class InspectionTagCardWizard(models.TransientModel):
    _name = "inspection.tag.card.wizard"

    filter = [
        ('', ''),
        ('pembahanan', 'Pembahanan'),
        ('proses_pengiriman', 'Proses Pengiriman'),
        ('pre_finishing', 'Pre Finishing'),
        ('top_coat', 'Top Coat'),
        ('packing', 'Packing'),
        ('bras_component', 'Bras Component'),
        ('kawai_top_coat', 'Kawai Top Coat'),
    ]
    type_qc = fields.Selection(filter, required=True, string='Type QC')
    start_date = fields.Datetime(string = 'Start Date')
    end_date = fields.Datetime(string = 'End Date')

    def action_print_inspection_tag_card_report(self):
        return self.env.ref('qa_qc.report_inspection_tag_card_xls_action').report_action(self)