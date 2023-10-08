from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class Invoice(models.Model):
    _name = 'invoice'
    _description = 'Invoice'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
        tracking=True,
        index=True,
        widget="button",
        on_click="show_account_move_data",
 )
    invoice_count = fields.Integer(
            compute="_compute_invoice_count", string='Invoice Count', copy=False, default=0, store=True)
   
    def _compute_invoice_count(self): 
        for record in self:
            invoice_domain = [('payment_reference', '=', record.name)]
            invoice_count = self.env['account.move'].search_count(invoice_domain)
            record.invoice_count = invoice_count

    def show_invoices(self):
        invoice_domain = [('payment_reference', '=', self.name)]
        invoices = self.env['account.move'].search(invoice_domain)

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_out_invoice_tree').id,
            'domain': invoice_domain,
        }

        if len(invoices) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': invoices[0].id,
            })

        return action
        
    operation_container_line_ids = fields.One2many(comodel_name='invoice.container.line', string='Product Detail', 
                                       inverse_name='invoice_id')
    product_line_ids = fields.One2many(comodel_name='invoice.line', string='Product Detail', 
                                       inverse_name='invoice_id')
    to_partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    to_partner_country_id = fields.Many2one('res.country', string='To', required=True)
    to_city_deliver = fields.Char('Deliver City')
    to_country_of_deliver_id = fields.Many2one('res.country', string='Country of Delivery')
    
    delivery_address_id = fields.Many2one('res.partner', string='Delivery Address', required=True)
    invoice_address_id = fields.Many2one('res.partner',string='Invoice Address')
    part_of_load = fields.Char(string='Port of Loading')
    shipper_id = fields.Many2one('res.company', string='Shipper')
    vessel = fields.Char(string='Vessel')
    peb_no = fields.Char(string='PEB NO.')
    marchandise = fields.Char(string='Merchandise')
    schedule_date = fields.Date('Schedule Date', required=True)
    booking_date = fields.Date('Booking date',required=True)
    cargo_date = fields.Date('Cargo Date', required=True)
    container = fields.Char('Container')
    container_no = fields.Char(string='Container No.')
    source_document_id = fields.Many2one('sale.order','Source Document')

    no_sc_id = fields.Many2one('sale.order', 'SC No.')
    source_document_ids = fields.Many2many('stock.picking', string='Source Documents', compute='_compute_source_documents')
    many_source_document_ids = fields.Many2many('stock.picking', string='Source Documents')
    invoice_container_operation_ids = fields.One2many('invoice.container.operation', 'invoice_id', string='invoice.container.operation')

    @api.depends('delivery_address_id')
    def _compute_source_documents(self):
        for record in self:
            if record.delivery_address_id:
                no_sc_id = record.no_sc_id.id
                picking_type_code = 'outgoing'
                record.source_document_ids = self.env['stock.picking'].search([
                    ('origin', '=', self.no_sc_id.name),
                    ('picking_type_id.code', '=', picking_type_code),
                    ('state', '=', 'done')
                ])
            else:
                record.source_document_ids = False

    
    freight = fields.Char('Freight')
    seal_no = fields.Char('Seal No.')
    buyer_po = fields.Char('Buyer PO')
    pricelist_id = fields.Many2one('product.pricelist', string='Currency', related='source_document_id.pricelist_id')
    currency_id = fields.Many2one(related='pricelist_id.currency_id', depends=["pricelist_id"], store=True)
    show_update_pricelist = fields.Boolean(string='Has Pricelist Changed', help="Technical Field, True if the pricelist was changed;\n"  " this will then display a recomputation button")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='State',default='draft', tracking=True)

    city_of_deliver_id = fields.Many2one("res.country.state","Deliver State")
    city_deliver = fields.Char('Deliver City')
    country_of_deliver_id = fields.Many2one('res.country', string='Country of Delivery')
    
    uom_name_line = fields.Char('Measurement')
    total_qty = fields.Float('Total Quantity', compute="_compute_total_qty")
    total_unit_price = fields.Float('Total Unit Price', compute="_compute_total_unit_price")
    total_amount = fields.Float('Total Amount',compute="_compute_total_amount")

    @api.onchange('source_document_id')
    def onchange_source_document_id(self):
        self.pricelist_id = self.source_document_id.pricelist_id
    
    @api.depends('product_line_ids.product_uom_qty')
    def _compute_total_qty(self):
        for record in self:
            subtotal_product_uom_qty = sum(record.product_line_ids.mapped('product_uom_qty'))
            record.total_qty = subtotal_product_uom_qty

    @api.depends('product_line_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            subtotal_amount = sum(record.product_line_ids.mapped('amount'))
            record.total_amount = subtotal_amount

    @api.depends('product_line_ids.unit_price')
    def _compute_total_unit_price(self):
        for record in self:
            subtotal_unit_price = sum(record.product_line_ids.mapped('unit_price'))
            record.total_unit_price = subtotal_unit_price

    def _prepare_invoice_lines(self):
        line_detail_inv = []
        for line in self.product_line_ids:
            line_detail = {
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.product_uom_qty,
                'product_uom_id': line.uom_id.id,
                'price_unit': line.unit_price,
                'price_subtotal': line.amount,
                'account_id': line.account_id.id,
            }
            line_detail_inv.append(line_detail)
        return line_detail_inv
    
    def send_data(self):
        invoice_ex = self.env['account.move'].create({
            'move_type' : 'out_invoice',
            'payment_reference': self.name,
            'partner_id': self.to_partner_id.id,
            'partner_shipping_id': self.delivery_address_id.id,
            'peb_no': self.peb_no,
            'invoice_date': self.booking_date,
            'state': 'draft',
            'invoice_date_due': self.schedule_date,
            'origin_ids': [(6, 0, self.many_source_document_ids.ids)],
        })
        invoice_lines = []
        for line in self.product_line_ids:
            line_detail = self.env['account.move.line'].create({
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.product_uom_qty,
                'product_uom_id': line.uom_id.id,
                'price_unit': line.unit_price,
                'price_subtotal': line.amount,
                'account_id': line.account_id.id,
                'move_id': invoice_ex.id,
            })
            invoice_lines.append((0, 0, {
                'product_id': line_detail.product_id.id,
                'name': line_detail.name,
                'quantity': line_detail.quantity,
                'product_uom_id': line_detail.product_uom_id.id,
                'price_unit': line_detail.price_unit,
                'price_subtotal': line_detail.price_subtotal,
                'account_id': line_detail.account_id.id,
                'move_id': invoice_ex.id,
            }))
        invoice_ex.write({'invoice_line_ids': invoice_lines})
        return invoice_ex

    
    def action_validate(self):
        if self.state == 'draft':
            self.write( { 
                         'state': 'done',
                         })
        invoice_ex = self.env['account.move'].create({
            'move_type' : 'out_invoice',
            'payment_reference': self.name,
            'partner_id': self.to_partner_id.id,
            'partner_shipping_id': self.delivery_address_id.id,
            'peb_no': self.peb_no,
            'invoice_date': self.booking_date,
            'state': 'draft',
            'invoice_date_due': self.schedule_date,


        })
        invoice_lines = []
        for line in self.product_line_ids:
            line_detail = self.env['account.move.line'].create({
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.product_uom_qty,
                'product_uom_id': line.uom_id.id,
                'price_unit': line.unit_price,
                'price_subtotal': line.amount,
                'account_id': line.account_id.id,
                'move_id': invoice_ex.id,
            })
            invoice_lines.append((0, 0, {
                'product_id': line_detail.product_id.id,
                'name': line_detail.name,
                'quantity': line_detail.quantity,
                'product_uom_id': line_detail.product_uom_id.id,
                'price_unit': line_detail.price_unit,
                'price_subtotal': line_detail.price_subtotal,
                'account_id': line_detail.account_id.id,
                'move_id': invoice_ex.id,
            }))
        invoice_ex.write({'invoice_line_ids': invoice_lines})
        return invoice_ex
    
    def action_approve(self):
        if self.state == 'waiting':
            self.write( { 
                         'state': 'ready',
                         })
    
    def action_done(self):
        if self.state == 'ready':
            self.write( { 
                         'state': 'done',
                         })
            
    def action_sign(self):
         if self.state == 'waiting':
            self.write( { 
                         'state': 'ready',
                         })
            
    def action_print(self):
        if self.state == 'waiting':
            self.write( { 
                        'state': 'ready',
                        })
    
    def action_scrap(self):
        if self.state == 'waiting':
            self.write( { 
                        'state': 'ready',
                        })
            
    def action_unlock(self):
        if self.state == 'waiting':
            self.write( { 
                        'state': 'ready',
                        })
    
    def action_cancel(self):
        if self.state == 'waiting':
            self.write( { 
                        'state': 'ready',
                        })   

    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        if self.pricelist_id and self._origin.pricelist_id != self.pricelist_id:
            self.show_update_pricelist = True
        else:
            self.show_update_pricelist = False

    def _get_update_prices_lines(self):
        return self(lambda line: not line.display_type)

    def update_prices(self):
        self.ensure_one()
        for line in self._get_update_prices_lines():
            line.product_uom_change()
            line.discount = 0  # Force 0 as discount for the cases when _onchange_discount directly returns
            line._onchange_discount()
        self.show_update_pricelist = False
        self.message_post(body=_("Product prices have been recomputed according to pricelist <b>%s<b> ", self.pricelist_id.display_name))
    
    invoice_id = fields.Many2one(
        string='Invoice',
        comodel_name='packing.list',
    )
class InvoiceLine(models.Model):
    _name = 'invoice.line'
    
    name = fields.Char(string='Description')
    invoice_id = fields.Many2one(comodel_name='invoice', string='Invoice')
    product_id = fields.Many2one(comodel_name= 'product.product', string='Product', required=True,)
    uom_id = fields.Many2one("uom.uom","Unit Of Measure", store=True, related='product_id.uom_id')
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot/Serial Number')
    location_id = fields.Many2one('stock.location', string='From')
    qty_done = fields.Float('Done')
    product_uom_qty = fields.Float('Quantity')
    reserved = fields.Float('Reserved')
    unit_price = fields.Float('Unit Price', store=True)
    amount = fields.Float('Amount',store=True)
    sku = fields.Char('SKU')

    seal_no = fields.Char('Seal No.')
    container_no = fields.Char(string='Container No.')
    account_id = fields.Many2one('account.account', store=True,string='Account')

class InvoiceContainerLine(models.Model):
    _name = 'invoice.container.line'
    _description = 'Invoice Container Line'

    invoice_id = fields.Many2one(comodel_name='invoice', string='Invoice')
    no_sc_ids = fields.Many2many('stock.picking',string='SC No', store=True)
    many_no_sc_id = fields.Many2one('stock.picking', string='SC No', store=True)
    container_no = fields.Char('Container No.')
    seal_no = fields.Char('Seal No.')


class InvoiceContainerOperation(models.Model):
    _name = 'invoice.container.operation'
    _description = 'Container Operation'
    
    invoice_id = fields.Many2one(comodel_name='invoice', string='Packing List',store=True)
    container_no = fields.Char('Container No.')
    seal_no = fields.Char('Seal No.')
    order_id = fields.Many2one('sale.order', string='order', compute='_compute_order_id', store=True)
    invoice_container_operation_line_ids = fields.One2many(comodel_name='invoice.container.operation.line', inverse_name='invoice_container_operation_id', string='Operation Container Line', store=True)
    picking_ids = fields.Many2many('stock.picking', 'invoice_cont_picking_ids_rel', 'invoice_cont_op_id', 'picking_id', string='SC No', store=True)
    total_net_wght = fields.Float('Total Net Weight',)
    total_gross_wght = fields.Float('Total Gross Weight',)
    total_means = fields.Float('Total Measurement',)
    total_qty = fields.Float('Total Quantity', )
    total_qty_pcs = fields.Float('Total Quantity Pcs',)
    total_qty_set = fields.Float('Total Quantity Set',)
    total_pack = fields.Float('Total Pack',)
    volume_uom_name_line = fields.Char('Measurement')
    weight_uom_name_line = fields.Char('weight_uom_name')
    uom_name_line = fields.Char('Measurement')
    total_pack = fields.Float('Total Pack')
    
class InvoiceContainerOperationLine(models.Model):
    _name = 'invoice.container.operation.line'
    _description = 'Invoice Container Operation Line'
    
    move_id = fields.Many2one('stock.move', string='Move')
    invoice_container_operation_id = fields.Many2one('invoice.container.operation', string='Invoice Container Operation')
    picking_id = fields.Many2one('stock.picking', string='picking', store=True, )
    order_line_id = fields.Many2one('sale.order.line', string='Order Line', )
    product_container_qty = fields.Float('Quantity in Cont.', store=True)
    invoice_id = fields.Many2one(comodel_name='invoice', string='Invoice List', related='invoice_container_operation_id.invoice_id',store=True)
    product_id = fields.Many2one(comodel_name= 'product.product', string='Product',store=True, related='move_id.product_id')
    product_uom_qty = fields.Float('Quantity', store=True, related='move_id.product_uom_qty')
    quantity_done = fields.Float('Quantity', store=True, related='move_id.quantity_done')
    container_no = fields.Char('Container No.', related='invoice_container_operation_id.container_no',store=True)
    seal_no = fields.Char('Seal No.', related='invoice_container_operation_id.seal_no',store=True)
    pack = fields.Float('Pack (CTN)', store=True, related='product_id.pack' )
    net_weight = fields.Float('Net Weight (KGS)', store=True , related='product_id.net_weight')
    gross_weight = fields.Float('Gross Weight (KGS)', store=True, related='product_id.gross_weight' )
    means = fields.Float('Measurement(CBM)', store=True , related='product_id.means')
    sku = fields.Char('SKU', store=True)
    product_uom = fields.Many2one('uom.uom', string='UoM',store=True, related='move_id.product_uom')
    unit_price = fields.Float('Unit Price', store=True)
    amount = fields.Float('Amount')