from odoo import models
 
class InspectionTagCardXlsx(models.AbstractModel):
    _name = 'report.qa_qc.report_inspection_tag_card_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, report):
        for obj in report:
            report_name = 'Report Inspection Tag Card'
            start_date = obj.start_date
            end_date = obj.end_date
            sheet = workbook.add_worksheet(report_name[:31])
            text_top_style = workbook.add_format({'font_size': 12, 'color': 'white', 'bold': True, 'valign': 'vcenter', 'text_wrap': True, 'bg_color': 'black', 'align': 'center', 'italic': True})
            label_title = workbook.add_format({'bold': True,'align':'center','font_size': 11})
            label_table = workbook.add_format({'align': 'center','valign': 'vcenter','bold':True,'font_size': 11,'border':1,'align':'center','text_wrap': True,'bg_color': '#B0E0E6'})
            label_table2 = workbook.add_format({'align': 'center','valign': 'vcenter','font_size': 11,'border':1,'align':'center','text_wrap': True,'bg_color': '#B0E0E6'})
            label_table2 = workbook.add_format({'align': 'center','valign': 'vcenter','bold':True,'font_size': 11,'border':1,'align':'center','bg_color': '#B0E0E6','text_wrap': True})
            label_table3 = workbook.add_format({'align': 'center','valign': 'vcenter','bold':True,'font_size': 11,'border':1,'align':'center','bg_color': '#90EE90','text_wrap': True})
            data_format = workbook.add_format({'font_size': 11,'border':1,'bg_color': '#F0F8FF','align':'center'})
            filter = []
            inspection_obj = self.env['inspection.tag.card']
            
            if obj.type_qc == 'pembahanan':
                filter.append(('type_qc', '=', 'pembahanan'))
            elif obj.type_qc == 'proses_pengiriman':
                filter.append(('type_qc', '=', 'proses_pengiriman'))
            elif obj.type_qc == 'pre_finishing':
                filter.append(('type_qc', '=', 'pre_finishing'))
            elif obj.type_qc == 'top_coat':
                filter.append(('type_qc', '=', 'top_coat'))
            elif obj.type_qc == 'packing':
                filter.append(('type_qc', '=', 'packing'))
            elif obj.type_qc == 'bras_component':
                filter.append(('type_qc', '=', 'bras_component'))
            elif obj.type_qc == 'kawai_top_coat':
                filter.append(('type_qc', '=', 'kawai_top_coat'))
            elif obj.type_qc == '':
                filter.append(('type_qc', '=', ''))
            else :
                filter.append('|')
                filter.append(('type_qc', '=', 'pembahanan'))
                filter.append(('type_qc', '=', 'proses_pengiriman'))
                filter.append(('type_qc', '=', 'pre_finishing'))
                filter.append(('type_qc', '=', 'top_coat'))
                filter.append(('type_qc', '=', 'packing'))
                filter.append(('type_qc', '=', 'bras_component'))
                filter.append(('type_qc', '=', 'kawai_top_coat'))
                filter.append(('type_qc', '=', ''))
            filter.append(('date','>=',start_date))
            filter.append(('date','<=',end_date))
            inspection = inspection_obj.search(filter, order="date asc")
            
            sheet.set_row(0, 17)
            sheet.set_column('A:A', 15)
            sheet.set_column('B:B', 15)
            sheet.set_column('C:C', 15)
            sheet.set_column('D:D', 15)
            sheet.set_column('E:E', 15)
            sheet.set_column('F:F', 15)
            sheet.set_column('G:G', 15)
            sheet.set_column('H:H', 15)
            sheet.set_column('I:I', 15)
            sheet.set_column('J:J', 15)
            sheet.set_column('K:K', 15)
            sheet.set_column('L:L', 15)
            sheet.set_column('M:M', 15)
            sheet.set_column('N:N', 15)
            
            for ins in inspection: #avoid singleton
                sheet.merge_range(1, 0, 1, 1, "START DATE", label_title)
                sheet.write(2, 0, "YEAR", label_table2)
                sheet.write(2, 1, start_date.strftime("%Y") if ins.date else "", label_table2)
                sheet.write(3, 0, "MONTH", label_table2)
                sheet.write(3, 1, start_date.strftime("%m") if ins.date else "", label_table2)
                sheet.write(4, 0, "DAY", label_table2)
                sheet.write(4, 1, start_date.strftime("%d") if ins.date else "", label_table2)
                sheet.merge_range(1, 3, 1, 4, "END DATE", label_title)
                sheet.write(2, 3, "YEAR", label_table2)
                sheet.write(2, 4, end_date.strftime("%Y") if ins.date else "", label_table2)
                sheet.write(3, 3, "MONTH", label_table2)
                sheet.write(3, 4, end_date.strftime("%m") if ins.date else "", label_table2)
                sheet.write(4, 3, "DAY", label_table2)
                sheet.write(4, 4, end_date.strftime("%d") if ins.date else "", label_table2)
                
            if obj.type_qc == 'pembahanan':
                sheet.merge_range(0, 0, 0, 9, "SERVICE RATE PEMBAHANAN", text_top_style)
                sheet.merge_range(6, 0, 7, 0, "ITEM", label_table)
                sheet.merge_range(6, 1, 7, 1,"KOMPONEN", label_table)
                sheet.merge_range(6, 2, 7, 2,"UKURAN", label_table)
                sheet.merge_range(6, 3, 7, 3,"Jenis Kayu", label_table)
                sheet.merge_range(6, 4, 7, 4,"DEFECT MATERIAL", label_table)
                sheet.merge_range(6, 5, 7, 5,"SU", label_table)
                sheet.merge_range(6, 6, 7, 6,"%", label_table)
                sheet.merge_range(6, 7, 7, 7,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 8, 7, 8,"TOTAL KIRIM (TK)", label_table)
                sheet.merge_range(6, 9, 7, 9,"% HARIAN", label_table)
                
                row = 7
                for ins in inspection:
                    for move in ins.product_line_ids:
                        sheet.write(row, 0, ins.product_pembahanan_id.name, data_format)
                        sheet.write(row, 1, move.product_id.name, data_format)
                        sheet.write(row, 2, move.ukuran_pembahanan, data_format)
                        sheet.write(row, 3, move.jenis_kayu_pembahanan_id.name, data_format)
                        for line in ins.operation_line_ids:
                            sheet.write(row, 4, line.ket_masalah_id.name, data_format)
                        sheet.write(row, 5, move.no_su, data_format)
                        sheet.write(row, 6, None, data_format) 
                        sheet.write(row, 7, move.no_lp, data_format)
                        sheet.write(row, 8, move.tk_qty, data_format)
                        sheet.write(row, 9, None, data_format) 
                        row+=1
                    
                sum_no_su = sum(move.no_su for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_qty = sum(move.tk_qty for move in inspection.product_line_ids)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,sum_no_su, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,sum_no_lp, label_table)
                sheet.write(row, 8,sum_tk_qty, label_table)
                sheet.write(row, 9,None, label_table3)
                row+=1
                
            elif obj.type_qc == 'proses_pengiriman':
                sheet.merge_range(0, 0, 0, 13, "SERVICE RATE PRODUKSI RAKITAN & PENGIRIMAN", text_top_style)
                sheet.merge_range(6, 0, 7, 0, "ITEM", label_table)
                sheet.merge_range(6, 1, 7, 1,"PO", label_table)
                sheet.merge_range(6, 2, 7, 2,"PO QTY", label_table)
                sheet.merge_range(6, 3, 7, 3,"COLOR", label_table)
                sheet.merge_range(6, 4, 7, 4,"KOMPONEN", label_table)
                sheet.merge_range(6, 5, 7, 5,"DEFECT PROSES", label_table)
                sheet.merge_range(6, 6, 7, 6,"DEFECT MATERIAL", label_table)
                sheet.merge_range(6, 7, 7, 7,"SU PROSES", label_table)
                sheet.merge_range(6, 8, 7, 8,"% PROSES", label_table)
                sheet.merge_range(6, 9, 7, 9,"SU MATERIAL", label_table)
                sheet.merge_range(6, 10, 7, 10,"% MATERIAL", label_table)
                sheet.merge_range(6, 11, 7, 11,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 12, 7, 12,"TOTAL KIRIM", label_table)
                sheet.merge_range(6, 13, 7, 13,"% HARIAN", label_table)
                
                row = 7
                for ins in inspection:
                    for move in ins.product_line_ids:
                        sheet.write(row, 0, ins.product_template_id.name, data_format)
                        sheet.write(row, 1, ins.no_mo_id.name, data_format)
                        sheet.write(row, 2, move.product_uom_qty, data_format)
                        sheet.write(row, 3, ins.fabric_colour_id.name, data_format)
                        sheet.write(row, 4, move.product_id.name, data_format)
                        for line in ins.operation_line_ids:
                            sheet.write(row, 5, line.defect_proses_id.name, data_format)
                            sheet.write(row, 6, line.defect_material_id.name, data_format)
                        sheet.write(row, 7, move.no_su_proses, data_format)
                        sheet.write(row, 8, None, data_format) 
                        sheet.write(row, 9, move.no_su_material, data_format)
                        sheet.write(row, 10, None, data_format) 
                        sheet.write(row, 11, move.no_lp, data_format)
                        sheet.write(row, 12, move.tk_qty, data_format)
                        sheet.write(row, 13, None, data_format) 
                        row+=1
                    
                sum_no_su_proses = sum(move.no_su_proses for move in inspection.product_line_ids) 
                sum_no_su_material = sum(move.no_su_material for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_no_tk = sum(move.no_tk for move in inspection.product_line_ids)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,sum_no_su_proses, label_table)
                sheet.write(row, 8,None, label_table)
                sheet.write(row, 9,sum_no_su_material, label_table)
                sheet.write(row, 10,None, label_table)
                sheet.write(row, 11,sum_no_lp, label_table)
                sheet.write(row, 12,sum_no_tk, label_table)
                sheet.write(row, 13,None, label_table3)
                row+=1
                
            elif obj.type_qc == 'pre_finishing':
                sheet.merge_range(0, 0, 0, 16, "SERVICE RATE PRODUKSI RAKITAN & PENGIRIMAN", text_top_style)
                sheet.merge_range(6, 0, 7, 0, "ITEM", label_table)
                sheet.merge_range(6, 1, 7, 1,"PO", label_table)
                sheet.merge_range(6, 2, 7, 2,"PO QTY", label_table)
                sheet.merge_range(6, 3, 7, 3,"COLOR", label_table)
                sheet.merge_range(6, 4, 7, 4,"KOMPONEN", label_table)
                sheet.merge_range(6, 5, 7, 5,"DEFECT PRODUKSI", label_table)
                sheet.merge_range(6, 6, 7, 6,"DEFECT PRE FINISHING", label_table)
                sheet.merge_range(6, 7, 7, 7,"KBL", label_table)
                sheet.merge_range(6, 8, 7, 8,"SU PRODUKSI", label_table)
                sheet.merge_range(6, 9, 7, 9,"% PRODUKSI", label_table)
                sheet.merge_range(6, 10, 7, 10,"SU PRE FINISHING", label_table)
                sheet.merge_range(6, 11, 7, 11,"% PRE FINISHING", label_table)
                sheet.merge_range(6, 12, 7, 12,"SU KBL", label_table)
                sheet.merge_range(6, 13, 7, 13,"% KBL", label_table)
                sheet.merge_range(6, 14, 7, 14,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 15, 7, 15,"TOTAL KIRIM", label_table)
                sheet.merge_range(6, 16, 7, 16,"% HARIAN", label_table)
                
                row = 7
                for ins in inspection:
                    for move in ins.product_line_ids:
                        sheet.write(row, 0, ins.product_template_id.name, data_format)
                        sheet.write(row, 1, ins.no_mo_id.name, data_format)
                        sheet.write(row, 2, move.product_uom_qty, data_format)
                        sheet.write(row, 3, ins.fabric_colour_id.name, data_format)
                        sheet.write(row, 4, move.product_id.name, data_format)
                        for line in ins.operation_line_ids:
                            sheet.write(row, 5, line.defect_production_id.name, data_format)
                            sheet.write(row, 6, line.defect_pre_finishing_id.name, data_format)
                            sheet.write(row, 7, line.defect_kbl_id.name, data_format)
                        sheet.write(row, 8, move.su_prodution, data_format)
                        sheet.write(row, 9, None, data_format) 
                        sheet.write(row, 10, move.su_pre_finishing, data_format)
                        sheet.write(row, 11, None, data_format) 
                        sheet.write(row, 12, move.su_kbl, data_format)
                        sheet.write(row, 13, None, data_format) 
                        sheet.write(row, 14, move.no_lp, data_format)
                        sheet.write(row, 15, move.tk_qty, data_format)
                        sheet.write(row, 16, None, data_format) 
                        row+=1
                        
                sum_su_production = sum(move.su_prodution for move in inspection.product_line_ids) 
                sum_su_pre_finishing = sum(move.su_pre_finishing for move in inspection.product_line_ids) 
                sum_su_kbl = sum(move.su_kbl for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_no_tk = sum(move.no_tk for move in inspection.product_line_ids)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,None, label_table)
                sheet.write(row, 8,sum_su_production, label_table)
                sheet.write(row, 9,None, label_table)
                sheet.write(row, 10,sum_su_pre_finishing, label_table)
                sheet.write(row, 11,None, label_table)
                sheet.write(row, 12,sum_su_kbl, label_table)
                sheet.write(row, 13,None, label_table)
                sheet.write(row, 14,sum_no_lp, label_table)
                sheet.write(row, 15,sum_no_tk, label_table)
                sheet.write(row, 16,None, label_table3)
                row+=1
                
            elif obj.type_qc == 'top_coat' or obj.type_qc == 'packing':
                if obj.type_qc == 'top_coat':
                    sheet.merge_range(0, 0, 0, 16, "SERVICE RATE TOP COAT FINISHING", text_top_style)
                elif obj.type_qc == 'packing':
                    sheet.merge_range(0, 0, 0, 16, "SERVICE RATE PACKING", text_top_style)
                sheet.merge_range(6, 0, 7, 0, "ITEM", label_table)
                sheet.merge_range(6, 1, 7, 1,"PO", label_table)
                sheet.merge_range(6, 2, 7, 2,"PO QTY", label_table)
                sheet.merge_range(6, 3, 7, 3,"COLOR", label_table)
                sheet.merge_range(6, 4, 7, 4,"KOMPONEN", label_table)
                sheet.merge_range(6, 5, 7, 5,"DEFECT PROSES", label_table)
                sheet.merge_range(6, 6, 7, 6,"DEFECT PRE FINISHING", label_table)
                sheet.merge_range(6, 7, 7, 7,"DEFECT TOP COAT FINISHING", label_table)
                sheet.merge_range(6, 8, 7, 8,"SU PROSES", label_table)
                sheet.merge_range(6, 9, 7, 9,"% PROSES", label_table)
                sheet.merge_range(6, 10, 7, 10,"SU PRE FINISHING", label_table)
                sheet.merge_range(6, 11, 7, 11,"% PRE FINISHING", label_table)
                sheet.merge_range(6, 12, 7, 12,"SU TOP COAT FINISHING", label_table)
                sheet.merge_range(6, 13, 7, 13,"% TOP COAT FINISHING", label_table)
                sheet.merge_range(6, 14, 7, 14,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 15, 7, 15,"TOTAL KIRIM", label_table)
                sheet.merge_range(6, 16, 7, 16,"% HARIAN", label_table)
                
                row = 7
                for ins in inspection:
                    for move in ins.product_line_ids:
                        sheet.write(row, 0, ins.product_template_id.name, data_format)
                        sheet.write(row, 1, ins.no_mo_id.name, data_format)
                        sheet.write(row, 2, move.product_uom_qty, data_format)
                        sheet.write(row, 3, ins.fabric_colour_id.name, data_format)
                        sheet.write(row, 4, move.product_id.name, data_format)
                        for line in ins.operation_line_ids:
                            sheet.write(row, 5, line.defect_proses_id.name, data_format)
                            sheet.write(row, 6, line.defect_pre_finishing_id.name, data_format)
                            sheet.write(row, 7, line.defect_coat_finishing_id.name, data_format)
                        sheet.write(row, 8, move.no_su_proses, data_format)
                        sheet.write(row, 9, None, data_format) 
                        sheet.write(row, 10, move.su_pre_finishing, data_format)
                        sheet.write(row, 11, None, data_format) 
                        sheet.write(row, 12, move.su_coat_finishing, data_format)
                        sheet.write(row, 13, None, data_format) 
                        sheet.write(row, 14, move.no_lp, data_format)
                        sheet.write(row, 15, move.tk_qty, data_format)
                        sheet.write(row, 16, None, data_format) 
                        row+=1
                        
                sum_no_su_proses = sum(move.no_su_proses for move in inspection.product_line_ids) 
                sum_su_pre_finishing = sum(move.su_pre_finishing for move in inspection.product_line_ids) 
                sum_su_coat_finishing = sum(move.su_coat_finishing for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_no_tk = sum(move.no_tk for move in inspection.product_line_ids)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,None, label_table)
                sheet.write(row, 8,sum_no_su_proses, label_table)
                sheet.write(row, 9,None, label_table)
                sheet.write(row, 10,sum_su_pre_finishing, label_table)
                sheet.write(row, 11,None, label_table)
                sheet.write(row, 12,sum_su_coat_finishing, label_table)
                sheet.write(row, 13,None, label_table)
                sheet.write(row, 14,sum_no_lp, label_table)
                sheet.write(row, 15,sum_no_tk, label_table)
                sheet.write(row, 16,None, label_table3)
                row+=1
                
            elif obj.type_qc == 'bras_component':
                sheet.merge_range(0, 0, 0, 12, "SERVICE RATE BRAS & KOMPONEN", text_top_style)
                sheet.merge_range(6, 0, 7, 0, "ITEM", label_table)
                sheet.merge_range(6, 1, 7, 1,"PROSES", label_table)
                sheet.merge_range(6, 2, 7, 2,"COLOR", label_table)
                sheet.merge_range(6, 3, 7, 3,"JENIS KOMPONEN", label_table)
                sheet.merge_range(6, 4, 7, 4,"DEFECT PROSES", label_table)
                sheet.merge_range(6, 5, 7, 5,"DEFECT MATERAIL", label_table)
                sheet.merge_range(6, 6, 7, 6,"SU PROSES", label_table)
                sheet.merge_range(6, 7, 7, 7,"% PROSES", label_table)
                sheet.merge_range(6, 8, 7, 8,"SU MATERIAL", label_table)
                sheet.merge_range(6, 9, 7, 9,"% MATERIAL", label_table)
                sheet.merge_range(6, 10, 7, 10,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 11, 7, 11,"TOTAL KIRIM", label_table)
                sheet.merge_range(6, 12, 7, 12,"% HARIAN", label_table)
                
                row = 7
                for ins in inspection:
                    for move in ins.product_line_ids:
                        sheet.write(row, 0, ins.product_template_id.name, data_format)
                        sheet.write(row, 1, ins.no_mo_id.name, data_format)
                        sheet.write(row, 2, ins.fabric_colour_id.name, data_format)
                        sheet.write(row, 3, move.product_id.name, data_format)
                        for line in ins.operation_line_ids:
                            sheet.write(row, 4, line.defect_proses_id.name, data_format)
                            sheet.write(row, 5, line.defect_material_id.name, data_format)
                        sheet.write(row, 6, move.no_su_proses, data_format)
                        sheet.write(row, 7, None, data_format) 
                        sheet.write(row, 8, move.no_su_material, data_format)
                        sheet.write(row, 9, None, data_format) 
                        sheet.write(row, 10, move.no_lp, data_format)
                        sheet.write(row, 11, move.tk_qty, data_format)
                        sheet.write(row, 12, None, data_format) 
                        row+=1
                        
                sum_no_su_proses = sum(move.no_su_proses for move in inspection.product_line_ids) 
                sum_no_su_material = sum(move.no_su_material for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_no_tk = sum(move.no_tk for move in inspection.product_line_ids)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,sum_no_su_proses, label_table)
                sheet.write(row, 7,None, label_table)
                sheet.write(row, 8,sum_no_su_material, label_table)
                sheet.write(row, 9,None, label_table)
                sheet.write(row, 10,sum_no_lp, label_table)
                sheet.write(row, 11,sum_no_tk, label_table)
                sheet.write(row, 12,None, label_table3)
                row+=1
            
            elif obj.type_qc == 'kawai_top_coat':
                sheet.merge_range(0, 0, 0, 9, "SERVICE RATE TOP COAT KAWAI", text_top_style)
                sheet.merge_range(6, 0, 7, 0, "ITEM", label_table)
                sheet.merge_range(6, 1, 7, 1,"MO", label_table)
                sheet.merge_range(6, 2, 7, 2,"COLOR", label_table)
                sheet.merge_range(6, 3, 7, 3,"KOMPONEN", label_table)
                sheet.merge_range(6, 4, 7, 4,"DEFECT", label_table)
                sheet.merge_range(6, 5, 7, 5,"SU", label_table)
                sheet.merge_range(6, 6, 7, 6,"%", label_table)
                sheet.merge_range(6, 7, 7, 7,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 8, 7, 8,"TOTAL KIRIM (TK)", label_table)
                sheet.merge_range(6, 9, 7, 9,"% HARIAN", label_table)
                
                row = 7
                for ins in inspection:
                    for move in ins.product_line_ids:
                        sheet.write(row, 0, ins.product_template_id.name, data_format)
                        sheet.write(row, 1, ins.no_mo_id.name, data_format)
                        sheet.write(row, 2, ins.fabric_colour_id.name, data_format)
                        sheet.write(row, 3, move.product_id.name, data_format)
                        for line in ins.operation_line_ids:
                            sheet.write(row, 4, line.ket_masalah_id.name, data_format)
                        sheet.write(row, 5, move.no_su, data_format)
                        sheet.write(row, 6, None, data_format) 
                        sheet.write(row, 7, move.no_lp, data_format)
                        sheet.write(row, 8, move.tk_qty, data_format)
                        sheet.write(row, 9, None, data_format) 
                        row+=1
                        
                sum_no_su = sum(move.no_su for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_qty = sum(move.tk_qty for move in inspection.product_line_ids)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,sum_no_su, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,sum_no_lp, label_table)
                sheet.write(row, 8,sum_tk_qty, label_table)
                sheet.write(row, 9,None, label_table3)
                row+=1
                
            elif obj.type_qc == '':
                sheet.merge_range(0, 0, 0, 9, "SERVICE RATE CUSHION", text_top_style)
                sheet.merge_range(6, 0, 7, 0, "ITEM", label_table)
                sheet.merge_range(6, 1, 7, 1,"MO", label_table)
                sheet.merge_range(6, 2, 7, 2,"COLOR", label_table)
                sheet.merge_range(6, 3, 7, 3,"KOMPONEN", label_table)
                sheet.merge_range(6, 4, 7, 4,"DEFECT", label_table)
                sheet.merge_range(6, 5, 7, 5,"JUMLAH", label_table)
                sheet.merge_range(6, 6, 7, 6,"%", label_table)
                sheet.merge_range(6, 7, 7, 7,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 8, 7, 8,"TOTAL KIRIM (TK)", label_table)
                sheet.merge_range(6, 9, 7, 9,"% HARIAN", label_table)
                
                row = 7
                for ins in inspection:
                    for move in ins.product_line_ids:
                        sheet.write(row, 0, ins.product_template_id.name, data_format)
                        sheet.write(row, 1, ins.no_mo_id.name, data_format)
                        sheet.write(row, 2, ins.fabric_colour_id.name, data_format)
                        sheet.write(row, 3, move.product_id.name, data_format)
                        for line in ins.operation_line_ids:
                            sheet.write(row, 4, line.ket_masalah_id.name, data_format)
                        sheet.write(row, 5, move.product_uom_qty, data_format)
                        sheet.write(row, 6, None, data_format) 
                        sheet.write(row, 7, move.no_lp, data_format)
                        sheet.write(row, 8, move.tk_qty, data_format)
                        sheet.write(row, 9, None, data_format) 
                        row+=1
                        
                sum_jumlah = sum(move.product_uom_qty for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_qty = sum(move.tk_qty for move in inspection.product_line_ids)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,sum_jumlah, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,sum_no_lp, label_table)
                sheet.write(row, 8,sum_tk_qty, label_table)
                sheet.write(row, 9,None, label_table3)
                row+=1