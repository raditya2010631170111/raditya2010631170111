from odoo import models, fields, api, _
import xlsxwriter

class ReportReporting(models.AbstractModel):
    _name = 'report.jidoka_msu_recruitment.report_reporting'

    @api.model
    def create_xlsx_report(self, applicant_ids, data):

        Applicant = self.env['hr.applicant']
        # Bom = self.env['mrp.bom']
        # Product = self.env['product.product']
        workbook = xlsxwriter.Workbook('/tmp/reporting_overview.xlsx')
        # workbook = xlsxwriter.Workbook('/tmp/bom_overview.xlsx')

        text_format_left = workbook.add_format()
        text_format_left.set_align('left')
        text_format_left.set_align('vcenter')
        text_format_left.set_border()
        text_format_left.set_font_size(12)
        text_format_left.set_font_name('Calibri')
        
        text_format_left_title = workbook.add_format()
        text_format_left_title.set_align('left')
        text_format_left_title.set_align('vcenter')
        text_format_left_title.set_font_size(12)
        text_format_left_title.set_font_name('Calibri')
        
        text_format_c = workbook.add_format()
        text_format_c.set_align('center')
        text_format_c.set_align('vcenter')
        text_format_c.set_border()
        text_format_c.set_font_size(12)
        text_format_c.set_font_name('Calibri')
        
        text_format_center = workbook.add_format()
        text_format_center.set_align('center')
        text_format_center.set_align('vcenter')
        text_format_center.set_border()
        text_format_center.set_font_size(12)
        text_format_center.set_font_name('Calibri')
        text_format_center.set_num_format('#,##0')

        text_format_left_bold = workbook.add_format()
        text_format_left_bold.set_align('left')
        text_format_left_bold.set_align('vcenter')
        text_format_left_bold.set_font_size(12)
        text_format_left_bold.set_font_name('Calibri')
        text_format_left_bold.set_bold()
        text_format_left_bold.set_num_format('#,##0')
        
        text_format_center_gray = workbook.add_format()
        text_format_center_gray.set_align('center')
        text_format_center_gray.set_align('vcenter')
        text_format_center_gray.set_font_size(12)
        text_format_center_gray.set_font_name('Calibri')
        text_format_center_gray.set_num_format('#,##0')
        text_format_center_gray.set_bg_color('#d9d9d9')
        
        text_format_center_blue = workbook.add_format()
        text_format_center_blue.set_align('center')
        text_format_center_blue.set_align('vcenter')
        text_format_center_blue.set_font_size(12)
        text_format_center_blue.set_border()
        text_format_center_blue.set_bold()
        text_format_center_blue.set_font_name('Calibri')
        text_format_center_blue.set_num_format('#,##0')
        text_format_center_blue.set_bg_color('#146C94') 
        text_format_center_blue.set_font_color('white')  

        text_format_left_blue = workbook.add_format()
        text_format_left_blue.set_align('left')
        text_format_left_blue.set_align('vcenter')
        text_format_left_blue.set_font_size(12)
        text_format_left_blue.set_top() 
        text_format_left_blue.set_font_name('Calibri')
        text_format_left_blue.set_bg_color('#19A7CE')  
        text_format_left_blue.set_font_color('white') 
        
        text_format_right_blue = workbook.add_format()
        text_format_right_blue.set_align('right')
        text_format_right_blue.set_align('vcenter')
        text_format_right_blue.set_font_size(12)
        text_format_right_blue.set_top() 
        text_format_right_blue.set_left() 
        text_format_right_blue.set_font_name('Calibri')
        text_format_right_blue.set_bg_color('#19A7CE')  
        text_format_right_blue.set_font_color('white') 

        text_format_left_sub = workbook.add_format()
        text_format_left_sub.set_align('left')
        text_format_left_sub.set_align('vcenter')
        text_format_left_sub.set_font_size(12)
        text_format_left_sub.set_font_name('Calibri')
        text_format_left_sub.set_bg_color('#AFD3E2')  
        text_format_left_sub.set_font_color('black') 

        text_format_right_sub = workbook.add_format()
        text_format_right_sub.set_align('right')
        text_format_right_sub.set_align('vcenter')
        text_format_right_sub.set_font_size(12)
        text_format_right_sub.set_left()
        text_format_right_sub.set_font_name('Calibri')
        text_format_right_sub.set_bg_color('#AFD3E2')  
        text_format_right_sub.set_font_color('black') 

        worksheet = workbook.add_worksheet()

        title_format = workbook.add_format()
        title_format.set_align('center')
        title_format.set_align('vcenter')
        title_format.set_bold(True)
        title_format.set_bg_color('#FEFF86')
        title_format.set_font_size(20)

        worksheet.merge_range('A1:E1', 'Reporting History Recruitment', title_format)

        row = 0
        attachment_ids = Applicant.browse(attachment_ids)
        for partner_name in attachment_ids:
        # bom_ids = Bom.browse(bom_ids)
        # for bom_id in bom_ids:
            row += 3
            
            # product_name = "PRODUCT     :" + bom_id.product_tmpl_id.display_name
            # product_reference = "REFERENCE  :" + bom_id.code
            # product_quantity = "QTY                :" + str(bom_id.product_qty) + ' ' + bom_id.product_uom_id.name
            # worksheet.write(row, 0, product_name, text_format_left_bold)
            # worksheet.set_column(row, 0, 50)
            # worksheet.write(row+1, 0, product_reference, text_format_left_title)
            # worksheet.set_column(row, 0, 50)
            # worksheet.write(row+2, 0, product_quantity, text_format_left_title)
            # worksheet.set_column(row, 0, 50)

            # row += 5
            row += 9
            # headers = ['Components', 'Sub Components', 'Qty', 'UoM', 'Qty Total']
            header = ['No','Creation Date','Application Name','Mobile','Applied Job','Tags','Appreciation','Recruiter','Stage']
            col = 0
            for header in headers:
                worksheet.write(row-1, col, header, text_format_center_blue)
                col += 1
            
            # for line in bom_id.bom_line_ids:
            #     main_component = line.product_id.display_name
            #     quantity = line.product_qty 
            #     main_uom = line.product_uom_id.name
            for line in partner_name.attachment_line_ids:
                tgl_lst = line.create_date
                kode_unit = line.partner_name
                tipe_unit = line.partner_mobile

                # owner.append(prod.job_id or '-')
                # ritase.append(prod.categ_ids)
                # volume.append(prod.priority or 0)
                # lokasi.append(prod.user_id or 0)
                # remark.append(prod.stage_id or '-')
                
                worksheet.write(row, 0, tgl_lst, text_format_left_blue)
                worksheet.set_column(row, 0, 40)
                worksheet.write(row, 1, "", text_format_left_blue)
                worksheet.set_column(row, 1, 45)
                worksheet.write(row, 2, kode_unit , text_format_right_blue)
                worksheet.set_column(row, 2, 10)
                worksheet.write(row, 3, tipe_unit, text_format_left_blue)
                worksheet.set_column(row, 3, 10)
                worksheet.write(row, 4, "", text_format_left_blue)
                worksheet.set_column(row, 4, 10)

                row += 1

                # if line.product_id.bom_ids:
                #     for sub_bom in line.product_id.bom_ids:
                #         for sub_line in sub_bom.bom_line_ids:
                #             sub_component = sub_line.product_id.display_name
                #             sub_quantity = sub_line.product_qty
                #             sub_uom = sub_line.product_uom_id.name
                #             sub_total_qty = quantity * sub_quantity

                #             worksheet.write(row, 0, "", text_format_left_sub)
                #             worksheet.write(row, 1, sub_component, text_format_left_sub)
                #             worksheet.write(row, 2, sub_quantity, text_format_right_sub)
                #             worksheet.write(row, 3, sub_uom, text_format_left_sub)
                #             worksheet.write(row, 4, sub_total_qty, text_format_left_sub)

                #             row += 1
        workbook.close()
        with open('/tmp/reporting_overview.xlsx', 'rb') as f:
            result = f.read()

        return (result, 'xlsx')