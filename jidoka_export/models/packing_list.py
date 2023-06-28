from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class PackingList(models.Model):
    _name = 'packing.list'
    _description = 'Packing List'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, tracking=True, index=True)
    product_line_ids = fields.One2many(comodel_name='packing.list.line', string='Product Detail', inverse_name='packing_id')
    
    @api.depends('picking_ids')
    def _compute_move_container_ids(self):
        for order in self:
            moves = self.env['stock.move']
            for picking in order.picking_ids:
                moves |= picking.move_lines.filtered(lambda move: move.state != 'cancel')
            order.move_container_ids = moves
            
    operation_container_line_ids = fields.One2many(comodel_name='operation.container.line', string='Product Detail', inverse_name='packing_id')
    no_sc_id = fields.Many2one('sale.order', 'SC No.')
    nosc_name = fields.Char('nosc_name', related='no_sc_id.name')
    to_partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    to_partner_country_id = fields.Many2one('res.country', string='To', required=True)
    to_city_deliver = fields.Char('Deliver City')
    to_country_of_deliver_id = fields.Many2one('res.country', string='Country of Delivery')

    delivery_address_id = fields.Many2one('res.partner', string='Delivery Address', required=True, readonly=True)
    invoice_address_id = fields.Many2one('res.partner',string='Invoice Address')
    
    shipper_id = fields.Many2one('res.company', string='Shipper', default=lambda self: self.env['res.company'].search([('name', '=', 'PT. CIPTA KREASI WOOD INDUSTRY')]),readonly=True)    
    vessel = fields.Char(string='Vessel')
    peb_no = fields.Char(string='PEB NO.')
    marchandise = fields.Char(string='Merchandise')
    schedule_date = fields.Date('Schedule Date', required=True)
    booking_date = fields.Date('Booking date',required=True)
    cargo_date = fields.Date('Cargo Date', required=True)
    container = fields.Char('Container')
    container_no = fields.Char(string='Container No.')
    source_document_ids = fields.Many2many('stock.picking', string='Source Documents', compute='_compute_source_document_ids')
    container_operation_ids = fields.One2many(comodel_name='container.operation', string='Container Operation',  inverse_name='packing_id')
    
    @api.depends('no_sc_id')
    def _compute_source_document_ids(self):
        for record in self:
            if record.delivery_address_id:
                record.source_document_ids = self.env['stock.picking'].search([
                    ('origin', '=', record.nosc_name),
                    ('state', '=', 'done'),
                    ('picking_type_code', '=', 'outgoing')])
            else:
                record.source_document_ids = False
    
    freight = fields.Char('Freight')
    seal_no = fields.Char('Seal No.')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('ready', 'Ready'),
        ('done', 'Done'),
    ], string='State',default='draft', tracking=True)
    picking_id = fields.Many2one('stock.picking', string='Transfers')
    no_st_id = fields.Many2one('stock.picking', string='no_st')

    total_net_wght = fields.Float('Total Net Weight', compute='_compute_total_net_weight')
    total_gross_wght = fields.Float('Total Gross Weight', compute='_compute_total_gross_wght')
    total_means = fields.Float('Total Measurement', compute='_compute_total_total_means')
    total_qty_pcs = fields.Float('Total Quantity', compute='_compute_total_total_qty')
    total_qty_set = fields.Float('Total Quantity', compute='_compute_total_total_qty')
    total_pack = fields.Float('Total Pack', compute='_compute_total_pack')
    volume_uom_name_line = fields.Char('Measurement')
    weight_uom_name_line = fields.Char('weight_uom_name')
    uom_name_line = fields.Char('Measurement')

    city_of_deliver_id = fields.Many2one("res.country.state","Deliver State")
    city_deliver = fields.Char('Deliver City')
    country_of_deliver_id = fields.Many2one('res.country', string='Country of Delivery')
    buyer_po = fields.Char('Buyer PO')
    invoice_count = fields.Integer(
            compute="_compute_invoice_count", string='Invoice Count', copy=False, default=0, store=True)
    invoice_ids = fields.One2many(
        string='Invoice',
        comodel_name='invoice',
        inverse_name='invoice_id',
    )
   
    shipping_ins_id = fields.Many2one(
        string='Shipping',
        comodel_name='shipping.ins',
    )
    
    many_container_operaton_line_ids = fields.Many2many('container.operation.line', string='container_operaton_line', 
        compute='_compute_many_container_operaton_line_ids' )
    
    @api.depends('container_operation_ids')
    def _compute_many_container_operaton_line_ids(self):
        for record in self:
            record.many_container_operaton_line_ids = self.container_operation_ids.container_operation_line_ids
    

    @api.depends('product_line_ids.pack', 'product_line_ids.product_uom_qty')
    def _compute_total_pack(self):
        for record in self:
            subtotal_pack = sum(line.pack * line.product_uom_qty for line in record.product_line_ids)
            record.total_pack = subtotal_pack

    def tes(self):
        import pdb;pdb.set_trace()
                    
    @api.depends('product_line_ids.uom_id.name', 'product_line_ids.product_uom_qty')
    def _compute_total_total_qty(self):
        for record in self:
            subtotal_qty_pcs = 0.0
            subtotal_qty_set = 0.0
            for p_line in record.product_line_ids:
                if p_line.uom_id.name == 'pcs':
                    subtotal_qty_pcs += p_line.product_uom_qty
                elif p_line.uom_id.name == 'set':
                    subtotal_qty_set += p_line.product_uom_qty
            record.total_qty_pcs = subtotal_qty_pcs
            record.total_qty_set = subtotal_qty_set
            
        
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


    @api.onchange('country_of_deliver_id')
    def _onchange_country_of_deliver_id(self):
        self.city_of_deliver_id = True

    def action_validate(self):
         if self.state == 'draft':
            self.write( { 
                         'state': 'waiting',
                         })

    # INI WORK UNTUK SOLUSI BERDASARKAN many_source_document_ids yang terpilih
    def action_approve(self):
        count_stock_picking = len(self.env['stock.picking'].search([('origin', '=', self.source_document_ids.name)]))
        count_done = len(self.env['stock.picking'].search([('origin', '=', self.source_document_ids.name), ('state', '=', 'done')]))
        if self.state == 'waiting':
            self.write({ 
                'state': 'ready',
            })
       
    def action_done(self):
        if self.state == 'ready':
            self.write({'state': 'done'})
            invoice_list = self.env['invoice'].create({
                'name': self.name,
                'no_sc_id': self.no_sc_id.id,
                'to_partner_id': self.to_partner_id.id,
                'to_city_deliver': self.to_city_deliver,
                'to_partner_country_id': self.to_partner_country_id.id,
                'delivery_address_id': self.delivery_address_id.id,
                'invoice_address_id': self.invoice_address_id.id,
                'country_of_deliver_id': self.country_of_deliver_id.id,
                'shipper_id': self.shipper_id.id,
                'vessel': self.vessel,
                'peb_no': self.peb_no,
                'marchandise': self.marchandise,
                'schedule_date': self.schedule_date,
                'booking_date': self.booking_date,
                'freight': self.freight,
                'cargo_date': self.cargo_date,
                'buyer_po' : self.buyer_po,
                'invoice_container_operation_ids': [(0, 0, {
                    'picking_ids': line.picking_ids,
                    'container_no': line.container_no,
                    'seal_no': line.seal_no,
                    'total_qty_pcs' : line.total_qty_pcs,
                    'total_qty_set' : line.total_qty_set,
                    'total_pack' : line.total_pack,
                    'total_net_wght' : line.total_net_wght,
                    'total_gross_wght' : line.total_gross_wght,
                    'total_means' : line.total_means,
                    'invoice_container_operation_line_ids':[(0,0,{
                        'container_no':in_line.container_no,
                        'order_line_id':in_line.order_line_id.id,
                        'move_id': in_line.move_id.id,
                        'container_no': in_line.container_no,
                        'seal_no': in_line.seal_no,
                        'order_line_id': in_line.order_line_id.id,
                        'product_id': in_line.product_id.id,
                        'quantity_done': in_line.quantity_done,
                        'product_uom': in_line.product_uom.id,
                        'product_container_qty': in_line.product_container_qty,
                        'pack': in_line.pack,
                        'net_weight': in_line.net_weight,
                        'gross_weight': in_line.gross_weight,
                        'means': in_line.means,
                        'unit_price': in_line.unit_price,
                        'amount': in_line.amount,
                        
                        
                    })for in_line in line.container_operation_line_ids],
                }) for line in self.container_operation_ids],
                'product_line_ids': [(0, 0, {
                    'container_no': line.container_no,
                    'seal_no': line.seal_no,
                    'account_id': line.account_id.id,
                    'product_id': line.product_id.id,
                    'sku': line.sku,
                    'product_uom_qty': line.product_uom_qty,
                    'unit_price': line.unit_price,
                    'amount': line.amount,
                }) for line in self.product_line_ids]
            })
            self.invoice_ids = [(4, invoice_list.id, 0)]
            
            return {
            'name': 'invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'invoice',
            'type': 'ir.actions.act_window',
            'res_id': invoice_list.id,
        }
            
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
            
    def _compute_invoice_count(self):
        for record in self:
            invoice_count = self.env['invoice'].search_count([('name', '=', record.name)])
            record.invoice_count = invoice_count
    
    def _invoice_action_view(self):
        views = [(self.env.ref('jidoka_export.invoice_view_tree').id, 'tree'),
        (self.env.ref('jidoka_export.invoice_view_form').id, 'form')]
        action = {
            'name': _("Invoice of %s" % (self.display_name)),
            'type': 'ir.actions.act_window',
            'res_model': 'invoice',
            'view_mode': 'tree,form',
            'views': views,
            'context': {'create': False},
        }
        return action

    def invoice_btn(self):
            action = self._invoice_action_view()
            action['domain'] = [('name','=',self.name)]
            self._compute_invoice_count()  # Memperbarui invoice_count sebelum mengembalikan action
            return action 
            
    @api.onchange('container_operation_ids')
    def _onchange_container_operation_ids(self): 
        if not self.container_operation_ids:
            self.product_line_ids = [(5, 0, 0)]  # Remove existing lines
            
        move_line_ids = [] 
                
        for rec in self.container_operation_ids.container_operation_line_ids:
            move_line = self.env['packing.list.line'].create({
                'container_operation_line_id': rec.id,
                'packing_id':rec.packing_id.id,
                'product_id':rec.product_id.id,
                'uom_id':rec.product_uom.id,
                'sku':rec.sku,
                'qty_done':rec.quantity_done,
                'product_uom_qty':rec.product_uom_qty,
                'pack':rec.pack,
                'net_weight':rec.net_weight,
                'gross_weight':rec.gross_weight,
                'means':rec.means,
                'seal_no': rec.seal_no,
                'container_no': rec.container_no,
                'move_id':rec.move_id.id,
                'product_container_qty': rec.product_container_qty,
            })
            move_line_ids.append(move_line.id)
            
        self.product_line_ids = [(5, 0, 0)]
        self.product_line_ids = move_line_ids 

class PackingListLine(models.Model):
    _name = 'packing.list.line'
    
    container_operation_line_id = fields.Many2one('container.operation.line', string='Container Operation Line')
    name = fields.Char(string='Description')
    product_tmpl_id = fields.Many2one('product.template', string='Product', related='product_id.product_tmpl_id')
    packing_id = fields.Many2one(comodel_name='packing.list', string='Packing List')
    product_id = fields.Many2one(comodel_name= 'product.product', string='Product')
    uom_id = fields.Many2one("uom.uom","Unit Of Measure", store=True, related='product_id.uom_id')
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot/Serial Number')
    location_id = fields.Many2one('stock.location', string='From')
    qty_done = fields.Float('Done')
    product_uom_qty = fields.Float('Quantity', store=True)
    pack = fields.Float('Pack (CTN)', store=True,compute='_compute_pack')
    net_weight = fields.Float('Net Weight (KGS)', store=True,compute='_compute_pack')
    gross_weight = fields.Float('Gross Weight (KGS)', store=True,compute='_compute_pack')
    means = fields.Float('Measurement(CBM)', store=True,compute='_compute_pack')
    reserved = fields.Float('Reserved')
    unit_price = fields.Float('Unit Price')
    amount = fields.Float('Amount')
    william_fob_price = fields.Float('Single Price')
    william_set_price = fields.Float('Set Price')
    move_line_id = fields.Many2one('stock.move.line', string='Stock Move Line')
    sku = fields.Char('SKU')
    mo_no = fields.Char('Mo No.')
    product_container_qty = fields.Float('Quantity in Cont.', store=True)
    seal_no = fields.Char('Seal No.')
    container_no = fields.Char(string='Container No.')
    account_id = fields.Many2one('account.account', store=True,string='Account', related='product_id.property_account_income_id')
    move_id = fields.Many2one('stock.move', string='Move')

    @api.depends('product_uom_qty')
    def _compute_pack(self):
        for record in self:
            record.pack = record.product_id.pack
            record.net_weight = record.product_id.net_weight
            record.gross_weight = record.product_id.gross_weight
            record.means = record.product_id.means
   
class OperationContainer(models.Model):
    _name = 'operation.container.line'
    _description = 'Operation Container Line'
    
    packing_id = fields.Many2one(comodel_name='packing.list', string='Packing List')
    no_sc_ids = fields.Many2many('stock.picking', 'no_sc_ids_rel', 'container_line_id', 'picking_id', string='SC No', compute='_compute_no_sc_ids', store=True)
    many_no_sc_ids = fields.Many2many('stock.picking', 'many_no_sc_ids_rel', 'container_line_id', 'picking_id', string='SC No', store=True)
    container_no = fields.Char('Container No.')
    seal_no = fields.Char('Seal No.')
    item_container_ids = fields.Many2many('product.product', string='Item', compute='_compute_item_container_ids')
    many_container_ids = fields.Many2many('product.product', string='Item')
 

    @api.depends('packing_id')
    def _compute_no_sc_ids(self):
        for record in self:
            if record.packing_id:
                no_sc_ids = self.env['stock.picking'].search([
                    ('origin', '=', record.packing_id.no_sc_id.name),
                    ('picking_type_id.code', '=', 'outgoing'),
                    ('state', '=', 'done')
                ])
                record.no_sc_ids = no_sc_ids
            else:
                record.no_sc_ids = False


    @api.depends('many_no_sc_ids')
    def _compute_item_container_ids(self):
        for container_line in self:
            items = container_line.many_no_sc_ids.mapped('move_lines.product_id')
            container_line.item_container_ids = items
            # Hapus item_container_ids yang sudah ada dalam many_container_ids
            container_line.item_container_ids -= container_line.many_container_ids

class ContainerOperation(models.Model):
    _name = 'container.operation'
    _description = 'Container Operation'
    
    packing_id = fields.Many2one(comodel_name='packing.list', string='Packing List')
    container_no = fields.Char('Container No.')
    seal_no = fields.Char('Seal No.')
    order_id = fields.Many2one('sale.order', string='order', 
        compute='_compute_order_id', store=True)
    
    container_operation_line_ids = fields.One2many(comodel_name='container.operation.line', inverse_name='container_operation_id', string='Operation Container Line', store=True)
    picking_ids = fields.Many2many('stock.picking', 'picking_ids_rel', 'container_line_id', 'picking_id', string='SC No', store=True)
    move_container_ids = fields.Many2many('stock.move','container_operation_move_rel', string='Move Container', compute='_compute_move_container_ids', store=True,)
    
    available_picking_ids = fields.Many2many('stock.picking', 'container_operation_available_picking_rel', 'container_operation_id', 'picking_id',  string='Available Picking', compute="_get_available_picking", store=True)
    
    total_net_wght = fields.Float('Total Net Weight', compute='_compute_total_net_weight')
    total_gross_wght = fields.Float('Total Gross Weight', compute='_compute_total_gross_wght')
    total_means = fields.Float('Total Measurement', compute='_compute_total_total_means')
    total_qty = fields.Float('Total Quantity', compute='_compute_total_total_qty')
    total_qty_pcs = fields.Float('Total Quantity Pcs', compute='_compute_total_total_qty')
    total_qty_set = fields.Float('Total Quantity Set', compute='_compute_total_total_qty')
    total_pack = fields.Float('Total Pack', compute='_compute_total_pack')
    volume_uom_name_line = fields.Char('Measurement')
    weight_uom_name_line = fields.Char('weight_uom_name')
    uom_name_line = fields.Char('Measurement')
    total_pack = fields.Float('Total Pack', compute='_compute_total_pack')
    
    datetime_now = fields.Datetime(
        string='date_now',
        default=fields.Datetime.now,
    )
    move_container_line_ids = fields.One2many(comodel_name='move.container.line', inverse_name='container_operation_id', string='Move Container Line', store=True)
    
    def tes(self):
        import pdb;pdb.set_trace()
    
    @api.depends('container_operation_line_ids.pack', 'container_operation_line_ids')
    def _compute_total_pack(self):
        for record in self:
            subtotal_pack = sum(line.pack for line in record.container_operation_line_ids)
            record.total_pack = subtotal_pack

    @api.depends('container_operation_line_ids.quantity_done')
    def _compute_total_total_qty(self):
        for rec in self:
            subtotal_qty_pcs = 0.0
            subtotal_qty_set = 0.0
            for c_line in rec.container_operation_line_ids:
                if c_line.product_uom.name == 'pcs':
                    subtotal_qty_pcs += c_line.quantity_done
                elif c_line.product_uom.name == 'set':
                    subtotal_qty_set += c_line.quantity_done
            rec.total_qty_pcs = subtotal_qty_pcs
            rec.total_qty_set = subtotal_qty_set

    
    @api.depends('container_operation_line_ids.means', 'container_operation_line_ids')
    def _compute_total_total_means(self):
        for record in self:
            subtotal_means = sum(line.means for line in record.container_operation_line_ids)
            record.total_means = subtotal_means

    
    @api.depends('container_operation_line_ids.gross_weight', 'container_operation_line_ids')
    def _compute_total_gross_wght(self):
        for record in self:
            total_weight_gross = sum(record.container_operation_line_ids.mapped(lambda line: line.gross_weight ))
            record.total_gross_wght = total_weight_gross

    
    @api.depends('container_operation_line_ids.net_weight', 'container_operation_line_ids')
    def _compute_total_net_weight(self):
        for record in self:
            total_weight = sum(record.container_operation_line_ids.mapped(lambda line: line.net_weight))
            record.total_net_wght = total_weight
        
    @api.depends('packing_id')
    def _compute_order_id(self):
        for rec in self:
            if rec.packing_id:
                rec.order_id = rec.packing_id.no_sc_id.id
            
    @api.depends('order_id', 'container_no', 'seal_no')
    def _get_available_picking(self):
        for rec in self:
            if rec.order_id:
                picking_ids = False
                if rec.container_no or rec.seal_no:
                    picking_ids = rec.env['stock.picking'].search([('origin', '=', rec.order_id.name), ('state', '=', 'done')])
                rec.available_picking_ids = picking_ids
                
    @api.depends('picking_ids')
    def _compute_move_container_ids(self):
        for order in self:
            moves = self.env['stock.move']
            for picking in order.picking_ids:
                moves |= picking.move_lines.filtered(lambda move: move.state != 'cancel')
            order.move_container_ids = moves
                
    @api.model
    def create(self, vals):
        container_operation = super(ContainerOperation, self).create(vals)
        # container_operation.generate_container_operation_lines()
        if not 'move_container_ids' in vals:
            self.generate_container_operation_lines()
        return container_operation

    def write(self, vals):
        res = super(ContainerOperation, self).write(vals)
        if 'move_container_ids' in vals:
            self.generate_container_operation_lines()
        return res

    @api.onchange('move_container_ids')
    def onchange_move_container_ids(self):
        self.generate_container_operation_lines()

    def generate_container_operation_lines(self):
        self.container_operation_line_ids = False
        container_operation_line_ids = []
        for move in self.move_container_ids:
            container_operation_line = self.env['container.operation.line'].new({
                'move_id': move.id,
                'container_operation_id': self.id,
                'product_uom_category_id': move.product_uom_category_id.id,
                'company_id': move.company_id.id,
            })
            container_operation_line_ids.append(container_operation_line.id)
        self.container_operation_line_ids = [(6, 0, container_operation_line_ids)]
          
class ContainerOperationLine(models.Model):
    _name = 'container.operation.line'
    _description = 'Container Operation Line'
    
    move_id = fields.Many2one('stock.move', string='Move')
    packing_id = fields.Many2one(comodel_name='packing.list', string='Packing List', related='container_operation_id.packing_id',store=True)
    container_operation_id = fields.Many2one('container.operation', string='Container Operation')
    product_id = fields.Many2one(comodel_name= 'product.product', string='Product',store=True, related='move_id.product_id')
    product_uom_qty = fields.Float('Quantity', store=True, related='move_id.product_uom_qty')
    quantity_done = fields.Float('Quantity', store=True, related='move_id.quantity_done')
    picking_id = fields.Many2one('stock.picking', string='picking', store=True, 
        compute='_compute_picking_id' )
    container_no = fields.Char('Container No.', related='container_operation_id.container_no',store=True)
    seal_no = fields.Char('Seal No.', related='container_operation_id.seal_no',store=True)
    product_container_qty = fields.Float('Quantity in Cont.', store=True)
    pack = fields.Float('Pack (CTN)', store=True, related='product_id.pack' )
    net_weight = fields.Float('Net Weight (KGS)', store=True , related='product_id.net_weight')
    gross_weight = fields.Float('Gross Weight (KGS)', store=True, related='product_id.gross_weight' )
    means = fields.Float('Measurement(CBM)', store=True , related='product_id.means')
    order_line_id = fields.Many2one('sale.order.line', string='Order Line', 
        compute='_compute_order_line_id' )
    sku = fields.Char('SKU', store=True)
    product_uom = fields.Many2one('uom.uom', string='UoM',store=True, related='move_id.product_uom')
    unit_price = fields.Float('Unit Price')
    amount = fields.Float('Amount')
    datetime_now = fields.Datetime('datetime_now', related='container_operation_id.datetime_now')
    quantity_before = fields.Float('Qty Before')
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company,
        index=True, required=True)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    @api.depends('product_id','container_operation_id')     
    def _compute_order_line_id(self):
        for record in self:
            product = self.env['sale.order.line'].search([
                ('product_id', '=', record.product_id.id),
                ('no_mo', '=', record.container_operation_id.order_id.name)
            ], limit=1)
            
            if product:
                record.order_line_id = product.id
                record.sku = product.sku
            else:
                record.order_line_id = False

    @api.depends('move_id')
    def _compute_picking_id(self):
        for record in self:
            record.picking_id = record.move_id.picking_id.id
    
class MoveContainerLine(models.Model):
    _name = 'move.container.line'
    _description = 'Move Container Line'
    
    move_id = fields.Many2one('stock.move', string='Move', store=True)
    container_operation_id = fields.Many2one('container.operation', string='Container Operation')
    reference = fields.Char('reference')
    product_container_qty = fields.Float('Quantity in Cont.', store=True)
    sku = fields.Char('SKU', store=True)
    quantity_before = fields.Float('quantity_before')
    unit_price = fields.Float('Unit Price')
    amount = fields.Float('Amount')
    product_id = fields.Many2one(comodel_name= 'product.product', string='Product',store=True,)
    product_uom_qty = fields.Float('Quantity', store=True, related='move_id.product_uom_qty')
    quantity_done = fields.Float('Quantity', store=True, related='move_id.quantity_done')
    product_uom = fields.Many2one('uom.uom', string='UoM',store=True, related='move_id.product_uom')
    packing_id = fields.Many2one(comodel_name='packing.list', string='Packing List', related='container_operation_id.packing_id',store=True)
    container_no = fields.Char('Container No.', related='container_operation_id.container_no',store=True)
    seal_no = fields.Char('Seal No.', related='container_operation_id.seal_no',store=True)
    datetime_now = fields.Datetime('datetime_now', related='container_operation_id.datetime_now')
    pack = fields.Float('Pack (CTN)', store=True, related='product_id.pack' )
    net_weight = fields.Float('Net Weight (KGS)', store=True , related='product_id.net_weight')
    gross_weight = fields.Float('Gross Weight (KGS)', store=True, related='product_id.gross_weight' )
    means = fields.Float('Measurement(CBM)', store=True , related='product_id.means')
    picking_id = fields.Many2one('stock.picking', string='picking', store=True, 
        compute='_compute_picking_id' )
    order_line_id = fields.Many2one('sale.order.line', string='Order Line', 
        compute='_compute_order_line_id' )
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company,
        index=True, required=True)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    @api.depends('product_id','container_operation_id')     
    def _compute_order_line_id(self):
        for record in self:
            product = self.env['sale.order.line'].search([
                ('product_id', '=', record.product_id.id),
                ('no_mo', '=', record.container_operation_id.order_id.name)
            ], limit=1)
            
            if product:
                record.order_line_id = product.id
                record.sku = product.sku
            else:
                record.order_line_id = False

    @api.depends('move_id')
    def _compute_picking_id(self):
        for record in self:
            record.picking_id = record.move_id.picking_id.id