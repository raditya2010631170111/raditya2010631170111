# from odoo import models
from odoo import api, fields, models
import xlsxwriter

class ReportingXlsx(models.AbstractModel):
    _name = 'report.jidoka_msu_recruitment.report_reporting'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('Report Reporting %s' % obj.name)
        
        text_top_style = workbook.add_format({'font_size': 12, 'bold': True , 'valign': 'vcenter', 'text_wrap': True})
        text_header_style = workbook.add_format({'font_size': 12, 'bold': True , 'border':True, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        text_style = workbook.add_format({'font_size': 12, 'valign': 'vcenter', 'border':True, 'text_wrap': True, 'align': 'center'})
        number_style = workbook.add_format({'num_format': '#,##0.00', 'font_size': 12, 'border':True, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True})
        text_header_style_orange = workbook.add_format({'font_size': 12, 'bold': True , 'border':True, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'bg_color': 'orange'})
        text_header_style_blue = workbook.add_format({'font_size': 12, 'bold': True , 'border':True, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'bg_color': 'blue'})
        text_header_style_green = workbook.add_format({'font_size': 12, 'bold': True , 'border':True, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'bg_color': 'green'})
        text_header_style_yellow = workbook.add_format({'font_size': 12, 'bold': True , 'border':True, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'bg_color': 'yellow'})
        text_header_style_silver = workbook.add_format({'font_size': 12, 'bold': True , 'border':True, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center', 'bg_color': 'silver'})
        style_bold_money = workbook.add_format({'left': 1, 'top': 1,'right':1,'bottom':1,'bold': True,'num_format':'#,##0.00', 'align':'right'})
        currency_style = workbook.add_format({'num_format': '#,##0.00','left': 1, 'top': 1,'right':1,'bottom':1})
        style_bold = workbook.add_format({'left': 1, 'top': 1,'right':1,'bottom':1,'bold': True,'align':'center'})

        sheet.merge_range(0, 0, 0, 5, "REPORTING", text_top_style)
        row = 2
        sheet.set_column(1, 9, 20)
        header = ['No','Creation Date','Application Name','Mobile','Applied Job','Tags','Appreciation','Recruiter','Stage']
        sheet.write_row(2, 0, header, text_header_style)

        no_lst = []
        tgl_lst = []
        kode_unit = []
        tipe_unit = []
        owner = []
        ritase = []
        volume = []
        lokasi = []
        remark = []

        no = 1
        if obj.create_date:
            for prod in self.env['hr.applicant'].search([('create_date','=',obj.create_date.id)]):
                no_lst.append(no)
                tgl_lst.append(create_date('%d-%B-%Y') if prod.create_date else '')
                kode_unit.append(prod.partner_name or '-')
                tipe_unit.append(prod.partner_mobile or '-')
                owner.append(prod.job_id or '-')
                ritase.append(prod.categ_ids)
                volume.append(prod.priority or 0)
                lokasi.append(prod.user_id or 0)
                remark.append(prod.stage_id or '-')
                
                no += 1

        else:
            for prod in self.env['hr.applicant'].search([]):
                no_lst.append(no)
                tgl_lst.append(prod.create_date.strftime('%d-%B-%Y') if prod.create_date else '')
                kode_unit.append(prod.partner_name or '-')
                tipe_unit.append(prod.partner_mobile or '-')
                owner.append(prod.job_id or '-')
                ritase.append(prod.categ_ids)
                volume.append(prod.priority or 0)
                lokasi.append(prod.user_id or 0)
                remark.append(prod.stage_id or '-')
        
#openerp        
        for x in obj.session_line:
            no_list.append(no)
            session.append(x.name or '')
            partner.append(x.partner_id.name if x.partner_id and x.partner_id.name else '')
            start_date.append(x.start_date.strftime('%d-%m-%Y') if x.start_date else '')
            end_date.append(x.end_date.strftime('%d-%m-%Y') if x.end_date else '')
            duration.append(x.duration or '')
            seats.append(x.seats or '')
            attendees.append(x.attendees_count)
            taken_seats.append(x.taken_seats)
            status.append(x.state.capitalize())

                no += 1

        row += 1
        sheet.write_column(row, 0, no_lst, text_header_style)
        sheet.write_column(row, 1, tgl_lst, text_header_style)
        sheet.write_column(row, 2, kode_unit, text_style)
        sheet.write_column(row, 3, tipe_unit, text_style)
        sheet.write_column(row, 4, owner, text_style)
        sheet.write_column(row, 5, ritase, text_style)
        sheet.write_column(row, 6, volume, text_style)
        sheet.write_column(row, 7, lokasi, text_style)
        sheet.write_column(row, 8, remark, text_style)