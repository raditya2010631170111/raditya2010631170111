from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError
from odoo import http
from odoo.http import request


class ShippingIns(models.Model):
    _name = 'shipping.ins'

    name = fields.Char('Name', default=lambda self: _('New'), copy=False, readonly=True)
    product_line_ids = fields.One2many(comodel_name='shipping.ins.line', string='Product Detail', 
                                       inverse_name='shipping_id')
    to_partner_id = fields.Many2one('res.partner', string='Customer', required=True, store=True)
    to_partner_country_id = fields.Many2one('res.country', string='To', required=True)
    to_city_deliver = fields.Char('Deliver City')
    to_country_of_deliver_id = fields.Many2one('res.country', string='Country of Delivery')

    delivery_address_id = fields.Many2one('res.partner', string='Delivery Address', required=True)
    responsible_id = fields.Many2one('res.partner', string='Responsible', required=True)
    invoice_address_id = fields.Many2one('res.partner',string='Invoice Address')
    shipper_id = fields.Many2one(
    'res.company',
    string='Shipper',
    default=lambda self: self.env['res.company'].search([('name', 'in', ['PT. CIPTA KREASI WOOD INDUSTRY', 'Cipta Kreasi Wood Industry'])], limit=1) or self.env['res.company'].search([], limit=1),
    readonly=True
)
    schedule_date = fields.Date('Schedule Date', required=True)
    booking_date = fields.Date('Booking date',required=True)
    cargo_date = fields.Date('Cargo Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='State',default='draft', tracking=True)
    no_sc_id = fields.Many2one('sale.order', 'SC No.')
    no_st_id = fields.Many2one('stock.picking', string='no_st', compute='_compute_no_st_id')
    marchandise = fields.Char(string= 'Merchandise')    
    vessel = fields.Char(string='Vessel')
    container = fields.Char(string='Container')
    container_no = fields.Char(string='Container NO.')
    total_net_wght = fields.Float('Total Net Weight', compute='_compute_total_net_weight')
    total_gross_wght = fields.Float('Total Gross Weight', compute='_compute_total_gross_wght')
    total_means = fields.Float('Total Measurement', compute='_compute_total_total_means')
    total_qty = fields.Float('Total Quantity', compute='_compute_total_total_qty')
    total_pack = fields.Float('Total Pack', compute='_compute_total_pack')
    volume_uom_name_line = fields.Char('Measurement', related='product_line_ids.volume_uom_name')
    weight_uom_name_line = fields.Char('weight_uom_name', related='product_line_ids.weight_uom_name')
    uom_name_line = fields.Char('Measurement', related='product_line_ids.product_id.uom_id.name')
    freight = fields.Char('Freight')
    indicating = fields.Char('Indicating')
    seal_no = fields.Char('Seal No.')
    peb_no = fields.Char(string='PEB NO.')
    buyer_po = fields.Char('Buyer PO')
    packing_list_count = fields.Integer(
            compute="_compute_packing_list_count", string='Packing List Count', copy=False, default=0, store=True)
    packing_list_ids = fields.One2many(
        string='Packing',
        comodel_name='packing.list',
        inverse_name='shipping_ins_id',
    )
    
    city_of_deliver_id = fields.Many2one("res.country.state","Deliver State")
    city_deliver = fields.Char('Deliver City')
    country_of_deliver_id = fields.Many2one('res.country', string='Country of Delivery')
    @api.onchange('country_of_deliver_id')
    def _onchange_country_of_deliver_id(self):
        self.city_of_deliver_id = False
                  
    
    @api.depends('product_line_ids.pack', 'product_line_ids.product_uom_qty')
    def _compute_total_pack(self):
        for record in self:
            subtotal_pack = sum(line.pack * line.product_uom_qty for line in record.product_line_ids)
            record.total_pack = subtotal_pack


    @api.depends('product_line_ids.product_uom_qty')
    def _compute_total_total_qty(self):
        for record in self:
            subtotal_qty = sum(record.product_line_ids.mapped('product_uom_qty'))
            record.total_qty = subtotal_qty

    
    @api.depends('product_line_ids.means', 'product_line_ids.product_uom_qty')
    def _compute_total_total_means(self):
        for record in self:
            subtotal_means = sum(line.means * line.product_uom_qty for line in record.product_line_ids)
            record.total_means = subtotal_means

    
    @api.depends('product_line_ids.gross_weight', 'product_line_ids.product_uom_qty')
    def _compute_total_gross_wght(self):
        for record in self:
            total_weight_gross = sum(record.product_line_ids.mapped(lambda line: line.gross_weight * line.product_uom_qty))
            record.total_gross_wght = total_weight_gross

    
    @api.depends('product_line_ids.net_weight', 'product_line_ids.product_uom_qty')
    def _compute_total_net_weight(self):
        for record in self:
            total_weight = sum(record.product_line_ids.mapped(lambda line: line.net_weight * line.product_uom_qty))
            record.total_net_wght = total_weight

    @api.depends('no_sc_id')
    def _compute_no_st_id(self):
        for record in self:
            if record.no_sc_id:
                stock_picking = self.env['stock.picking'].search([('origin', '=', record.no_sc_id.name)], limit=1)
                record.no_st_id = stock_picking.id 
            else:
                record.no_st_id = False


    @api.onchange('no_sc_id', 'no_st_id')
    def onchange_no_sc_id(self):
        if self.no_sc_id:
            self.invoice_address_id = self.no_sc_id.partner_invoice_id.id
            self.to_partner_id = self.no_sc_id.partner_id.id
            self.delivery_address_id = self.no_sc_id.partner_shipping_id.id
            self.city_deliver = self.no_sc_id.city_deliver
            self.country_of_deliver_id = self.no_sc_id.country_of_deliver
            self.buyer_po = self.no_sc_id.buyer_po
            self.product_line_ids = [(5, 0, 0)] # remove existing lines
            lines = []
            for rec in self.no_sc_id.order_line.filtered(lambda r: r.product_id.type != 'service'):
                vals = {
                    'product_id' : rec.product_id.id,
                    'product_uom_qty' : rec.product_uom_qty,
                    'reserved' : rec.product_uom_qty,
                    'name'  : rec.name,
                    'william_fob_price' : rec.william_fob_price,
                    'william_set_price' : rec.william_set_price,
                    'sku' : rec.sku,
                }
                lines.append((0,0,vals))
            self.product_line_ids = lines
            
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('shipping.ins') or _('New')
        result = super(ShippingIns, self).create(vals)
        return result

    def action_validate(self):
        if self.state == 'draft':
            self.write({'state': 'done'})
            packing_list = self.env['packing.list'].create({
                'name' : self.name, 
                'to_partner_id': self.to_partner_id.id,
                'delivery_address_id': self.delivery_address_id.id,
                'invoice_address_id': self.invoice_address_id.id,
                'city_deliver': self.city_deliver,
                'country_of_deliver_id': self.country_of_deliver_id.id,
                'shipper_id': self.shipper_id.id,
                'vessel': self.vessel,
                'peb_no': self.peb_no,
                'marchandise': self.marchandise,
                'schedule_date': self.schedule_date,
                'booking_date': self.booking_date,
                'cargo_date': self.cargo_date,
                'to_city_deliver': self.to_city_deliver,
                'to_partner_country_id': self.to_partner_country_id.id,
                'no_sc_id' : self.no_sc_id.id,
                'freight': self.freight,
                'state': 'draft',
                'buyer_po' : self.buyer_po,     
                'shipping_ins_id': self.id        
            })
        return {
            'name': 'Packing List',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'packing.list',
            'type': 'ir.actions.act_window',
            'res_id': packing_list.id,
        }
    
    @api.depends('packing_list_ids')
    def _compute_packing_list_count(self):
        for order in self:
            order.packing_list_count = len(order.packing_list_ids)
    
    def _packing_list_action_view(self):
        views = [(self.env.ref('jidoka_export.packing_list_view_tree').id, 'tree'),
                (self.env.ref('jidoka_export.packing_list_view_form').id, 'form')]
        action = {
            'name': _("Picking List of %s" % (self.display_name)),
            'type': 'ir.actions.act_window',
            'res_model': 'packing.list',
            'view_mode': 'tree,form',
            'views': views,
            'context': {'create': False},
            'domain': [('id', 'in', self.packing_list_ids.ids)],
        }
        return action

    def packing_list_btn(self):
        action = self._packing_list_action_view()
        action['domain'] = [('id','in',self.packing_list_ids.ids)]
        return action

class ShippingInsLine(models.Model):
    _name = 'shipping.ins.line'
    
    name = fields.Char(string='Description')
    product_tmpl_id = fields.Many2one('product.template', string='Product', related='product_id.product_tmpl_id')
    shipping_id = fields.Many2one(comodel_name='shipping.ins', string='Shipping Instruction')
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
    )
    uom_id = fields.Many2one("uom.uom","Unit Of Measure", store=True, related='product_id.uom_id')
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot/Serial Number', domain="[('product_id','=',product_id)]")
    location_id = fields.Many2one('stock.location', string='From', default=lambda self: self.env.ref('stock.stock_location_stock').id)
    qty_done = fields.Float('Done')
    reserved = fields.Float('Reserved')
    type = fields.Char('type')
    pack = fields.Float('Pack (CTN)', related='product_tmpl_id.pack', store=True)
    net_weight = fields.Float('Net Weight (KGS)', related='product_tmpl_id.net_weight',store=True)
    gross_weight = fields.Float('Gross Weight (KGS)', related='product_tmpl_id.gross_weight',store=True)
    means = fields.Float('Measurement (CBM)', related='product_tmpl_id.means',store=True)
    volume_uom_name = fields.Char('Measurement', related='product_tmpl_id.volume_uom_name')
    weight_uom_name = fields.Char('Measurement', related='product_tmpl_id.weight_uom_name')
    qty_done = fields.Float('Done')
    sku = fields.Char('SKU')

    william_fob_price = fields.Float('Single Price',store=True)
    william_set_price = fields.Float('Set Price',store=True)
    @api.depends('william_fob_price', 'william_set_price')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.william_fob_price + record.william_set_price

    product_uom_qty = fields.Float('Quantity')
    unit_price = fields.Float('Unit Price', compute='_compute_unit_price', store=True)
    amount = fields.Float('Amount', compute='_compute_amount', store=True)
    @api.depends('product_uom_qty', 'unit_price')
    def _compute_amount(self):
        for record in self:
            record.amount = record.product_uom_qty * record.unit_price