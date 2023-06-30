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
            sheet.set_tab_color('#F0F8FF')
            text_top_style = workbook.add_format({'align': 'center','font_size': 12,'color': 'white','bold': True,'valign': 'vcenter','text_wrap': True,'bg_color': 'black','italic': True})
            label_title = workbook.add_format({'align':'center','font_size': 11,'bold': True})
            label_table = workbook.add_format({'align': 'center','font_size': 11,'bold':True,'valign': 'vcenter','text_wrap': True,'bg_color': '#B0E0E6'})
            label_table3 = workbook.add_format({'align': 'center','font_size': 11,'bold':True,'valign': 'vcenter','bg_color': '#90EE90'})
            label_table2 = workbook.add_format({'align': 'center','font_size': 11,'valign': 'vcenter','text_wrap': True,'bg_color': '#B0E0E6'})
            data_format = workbook.add_format({'align':'center','font_size': 11})
            filter = []
            inspection_obj = self.env['inspection.tag.card']
            sheet.set_row(0, 30)
            sheet.set_column(0, 16, 15)
            
            if obj.type_qc == 'reguler':
                filter.append(('type_qc', '=', 'reguler'))
            elif obj.type_qc == 'pembahanan':
                filter.append(('type_qc', '=', 'pembahanan'))
            elif obj.type_qc == 'bras_component':
                filter.append(('type_qc', '=', 'bras_component'))
            elif obj.type_qc == 'proses_pengiriman':
                filter.append(('type_qc', '=', 'proses_pengiriman'))
            elif obj.type_qc == 'pre_finishing':
                filter.append(('type_qc', '=', 'pre_finishing'))
            elif obj.type_qc == 'top_coat':
                filter.append(('type_qc', '=', 'top_coat'))
            elif obj.type_qc == 'packing':
                filter.append(('type_qc', '=', 'packing'))
            elif obj.type_qc == 'cushion':
                filter.append(('type_qc', '=', 'cushion'))
            elif obj.type_qc == 'kawai_top_coat':
                filter.append(('type_qc', '=', 'kawai_top_coat'))
            filter.append(('date','>=',start_date))
            filter.append(('date','<=',end_date))
            inspection = inspection_obj.search(filter, order="date asc")
            previous1 = None
            previous2 = None
            previous3 = None
            previous4 = None
            previous5 = None
            previous6 = None
            previous7 = None
            previous8 = None
            previous9 = None
            previous10 = None
            previous11 = None
            
            for ins in inspection: 
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
                
            if obj.type_qc == 'reguler':
                sheet.merge_range(0, 0, 0, 11, "SERVICE RATE REGULER", text_top_style)
                sheet.merge_range(6, 0, 7, 0, "ITEM", label_table)
                sheet.merge_range(6, 1, 7, 1,"PO", label_table)
                sheet.merge_range(6, 2, 7, 2,"PO QTY", label_table)
                sheet.merge_range(6, 3, 7, 3,"COLOR", label_table)
                sheet.merge_range(6, 4, 7, 4,"KOMPONEN", label_table)
                sheet.merge_range(6, 5, 7, 5,"DEFECT", label_table)
                sheet.merge_range(6, 6, 7, 6,"KBL", label_table)
                sheet.merge_range(6, 7, 7, 7,"SU", label_table)
                sheet.merge_range(6, 8, 7, 8,"%", label_table)
                sheet.merge_range(6, 9, 7, 9,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 10, 7, 10,"TOTAL KIRIM", label_table)
                sheet.merge_range(6, 11, 7, 11,"% HARIAN", label_table)
                
                row = 8
                for ins in inspection: 
                    sheet.write(row, 11, round(ins.persentase_harian, 2), data_format)
                    for move in ins.product_line_ids:
                        sheet.write(row, 8, round(move.persentase, 2), data_format)
                        for line in ins.operation_line_ids:
                            product_template_name = ins.product_template_id.name if ins.product_template_id else ""
                            no_mo_id = ins.no_mo_id.name if ins.no_mo_id else ""
                            fabric_colour_id = line.fabric_colour_id.name if line.fabric_colour_id else ""
                            product_uom_qty = move.product_uom_qty
                            no_lp = move.no_lp
                            no_tk = move.no_tk
                            if product_template_name != previous1:
                                sheet.write(row, 0, product_template_name, data_format)
                                previous1 = product_template_name
                            if no_mo_id != previous2:
                                sheet.write(row, 1, no_mo_id, data_format)
                                previous2 = no_mo_id
                            if product_uom_qty != previous3:
                                sheet.write(row, 2, product_uom_qty, data_format)
                                previous3 = product_uom_qty
                            if fabric_colour_id != previous4:
                                sheet.write(row, 3, fabric_colour_id, data_format)
                                previous4 = fabric_colour_id
                            else:
                                fabric_colour_id = ""
                            sheet.write(row, 4, line.product_id.name, data_format)
                            sheet.write(row, 5, line.ket_masalah_id.name if line.ket_masalah_id.name else "", data_format)
                            sheet.write(row, 6, line.no_kbl, data_format)
                            sheet.write(row, 7, line.no_su, data_format)
                            if no_lp != previous6:
                                sheet.write(row, 9, no_lp, data_format)
                                previous6 = no_lp
                            if no_tk != previous7:
                                sheet.write(row, 10, no_tk, data_format)
                                previous7 = no_tk
                            sheet.write(row, 3, fabric_colour_id, data_format)
                            row+=1
                        
                sum_no_su = sum(line.no_su for line in inspection.operation_line_ids) 
                sum_persentase = sum(move.persentase for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_no_tk = sum(move.no_tk for move in inspection.product_line_ids)  
                sum_persentase_harian = sum(ins.persentase_harian for ins in inspection)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,sum_no_su, label_table)
                sheet.write(row, 8,round(sum_persentase, 2), label_table)
                sheet.write(row, 9,sum_no_lp, label_table)
                sheet.write(row, 10,sum_no_tk, label_table)
                sheet.write(row, 11,round(sum_persentase_harian, 2), label_table3)
                row+=1
                
            elif obj.type_qc == 'pembahanan':
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
                
                row = 8
                for ins in inspection:
                    sheet.write(row, 9, round(ins.persentase_harian, 2), data_format)
                    for move in ins.product_line_ids:
                        sheet.write(row, 6, round(move.persentase, 2), data_format)
                        for line in ins.operation_line_ids:
                            product_pembahanan_id = ins.product_pembahanan_id.name if ins.product_pembahanan_id else ""
                            ukuran_pembahanan = move.ukuran_pembahanan
                            jenis_kayu_pembahanan_id = move.jenis_kayu_pembahanan_id.name if move.jenis_kayu_pembahanan_id else ""
                            no_lp = move.no_lp
                            tk_pembahanan = move.tk_pembahanan
                            if product_pembahanan_id != previous1:
                                sheet.write(row, 0, product_pembahanan_id, data_format)
                                previous1 = product_pembahanan_id
                            if ukuran_pembahanan != previous2:
                                sheet.write(row, 2, ukuran_pembahanan, data_format)
                                previous2 = ukuran_pembahanan
                            if jenis_kayu_pembahanan_id != previous3:
                                sheet.write(row, 3, jenis_kayu_pembahanan_id, data_format)
                                previous3 = jenis_kayu_pembahanan_id
                            sheet.write(row, 1, line.product_id.name, data_format)
                            sheet.write(row, 4, line.ket_masalah_id.name if line.ket_masalah_id.name else "", data_format)
                            sheet.write(row, 5, line.no_su, data_format)
                            if no_lp != previous5:
                                sheet.write(row, 7, no_lp, data_format)
                                previous5 = no_lp
                            if tk_pembahanan != previous6:
                                sheet.write(row, 8, tk_pembahanan, data_format)
                                previous6 = tk_pembahanan
                            row+=1
                             
                sum_no_su = sum(line.no_su for line in inspection.operation_line_ids) 
                sum_persentase = sum(move.persentase for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_total_kirim = sum(move.tk_pembahanan for move in inspection.product_line_ids)  
                sum_persentase_harian = sum(ins.persentase_harian for ins in inspection)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,sum_no_su, label_table)
                sheet.write(row, 6,round(sum_persentase, 2), label_table)
                sheet.write(row, 7,sum_no_lp, label_table)
                sheet.write(row, 8,sum_total_kirim, label_table)
                sheet.write(row, 9,round(sum_persentase_harian, 2), label_table3)
                row+=1
                
            elif obj.type_qc == 'bras_component':
                sheet.merge_range(0, 0, 0, 12, "SERVICE RATE BRAS & KOMPONEN", text_top_style)
                sheet.merge_range(6, 0, 7, 0, "ITEM", label_table)
                sheet.merge_range(6, 1, 7, 1,"PROSES", label_table)
                sheet.merge_range(6, 2, 7, 2,"COLOR", label_table)
                sheet.merge_range(6, 3, 7, 3,"JENIS KOMPONEN", label_table)
                sheet.merge_range(6, 4, 7, 4,"DEFECT PROSES", label_table)
                sheet.merge_range(6, 5, 7, 5,"DEFECT MATERIAL", label_table)
                sheet.merge_range(6, 6, 7, 6,"SU PROSES", label_table)
                sheet.merge_range(6, 7, 7, 7,"% PROSES", label_table)
                sheet.merge_range(6, 8, 7, 8,"SU MATERIAL", label_table)
                sheet.merge_range(6, 9, 7, 9,"% MATERIAL", label_table)
                sheet.merge_range(6, 10, 7, 10,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 11, 7, 11,"TOTAL KIRIM", label_table)
                sheet.merge_range(6, 12, 7, 12,"% HARIAN", label_table)
                
                row = 8
                for ins in inspection: 
                    sheet.write(row, 12, round(ins.persentase_harian_component, 2), data_format)
                    for line in ins.operation_line_ids:
                        for move in ins.product_line_ids:
                            product_template_name = ins.product_template_id.name if ins.product_template_id else ""
                            no_mo_name = ins.no_mo_id.name if ins.no_mo_id else ""
                            fabric_colour_id = line.fabric_colour_id.name if line.fabric_colour_id else ""
                            persentase_proses_component = round(move.persentase_proses_component, 2)
                            persentase_component_material = round(move.persentase_component_material, 2)
                            no_lp = move.no_lp
                            tk_component = move.tk_component
                            if product_template_name != previous1:
                                sheet.write(row, 0, product_template_name, data_format)
                                previous1 = product_template_name
                            if no_mo_name != previous2:
                                sheet.write(row, 1, no_mo_name, data_format)
                                previous2 = no_mo_name
                            if fabric_colour_id != previous3:
                                sheet.write(row, 2, fabric_colour_id, data_format)
                                previous3 = fabric_colour_id
                            else:
                                fabric_colour_id = ""
                            sheet.write(row, 3, line.product_id.name, data_format)
                            sheet.write(row, 4, line.defect_proses_component_id.name if line.defect_proses_component_id.name else "", data_format)
                            sheet.write(row, 5, line.defect_material_component_id.name if line.defect_material_component_id.name else "", data_format)
                            sheet.write(row, 6, line.su_proses_component, data_format)
                            sheet.write(row, 8, line.su_component_material, data_format)
                            if persentase_proses_component != previous4:
                                sheet.write(row, 7, persentase_proses_component, data_format)
                                previous4 = persentase_proses_component
                            if persentase_component_material != previous5:
                                sheet.write(row, 9, persentase_component_material, data_format)
                                previous5 = persentase_component_material
                            if no_lp != previous6:
                                sheet.write(row, 10, no_lp, data_format)
                                previous6 = no_lp
                            if tk_component != previous7:
                                sheet.write(row, 11, tk_component, data_format)
                                previous7 = tk_component
                            sheet.write(row, 2, fabric_colour_id, data_format)
                            row+=1
                        
                sum_su_proses_component = sum(line.su_proses_component for line in inspection.operation_line_ids) 
                sum_persentase_proses_component = sum(move.persentase_proses_component for move in inspection.product_line_ids)
                sum_su_component_material = sum(line.su_component_material for line in inspection.operation_line_ids) 
                sum_persentase_component_material = sum(move.persentase_component_material for move in inspection.product_line_ids)
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_component = sum(move.tk_component for move in inspection.product_line_ids)  
                sum_persentase_harian_component = sum(ins.persentase_harian_component for ins in inspection)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,sum_su_proses_component, label_table)
                sheet.write(row, 7,round(sum_persentase_proses_component, 2), label_table)
                sheet.write(row, 8,sum_su_component_material, label_table)
                sheet.write(row, 9,round(sum_persentase_component_material, 2), label_table)
                sheet.write(row, 10,sum_no_lp, label_table)
                sheet.write(row, 11,sum_tk_component, label_table)
                sheet.write(row, 12,round(sum_persentase_harian_component, 2), label_table3)
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
                
                row = 8
                for ins in inspection:
                    sheet.write(row, 13, round(ins.persentase_harian_pengiriman, 2), data_format)
                    for move in ins.product_line_ids:
                        for line in ins.operation_line_ids:
                            product_template_name = ins.product_template_id.name if ins.product_template_id else ""
                            fabric_colour_id = line.fabric_colour_id.name if line.fabric_colour_id else ""
                            no_mo_name = ins.no_mo_id.name if ins.no_mo_id else ""
                            product_uom_qty = move.product_uom_qty
                            persentase_proses = round(move.persentase_proses, 2)
                            persentase_material = round(move.persentase_material, 2)
                            no_lp = move.no_lp
                            tk_pengiriman = move.tk_pengiriman
                            if product_template_name != previous1:
                                sheet.write(row, 0, product_template_name, data_format)
                                previous1 = product_template_name
                            if no_mo_name != previous2:
                                sheet.write(row, 1, no_mo_name, data_format)
                                previous2 = no_mo_name
                            if product_uom_qty != previous3:
                                sheet.write(row, 2, product_uom_qty, data_format)
                                previous3 = product_uom_qty
                            if fabric_colour_id != previous4:
                                sheet.write(row, 3, fabric_colour_id, data_format)
                                previous4 = fabric_colour_id
                            else:
                                fabric_colour_id = ""
                            sheet.write(row, 4, line.product_id.name, data_format)
                            sheet.write(row, 5, line.defect_proses_id.name if line.defect_proses_id.name else "", data_format)
                            sheet.write(row, 6, line.defect_material_id.name if line.defect_material_id.name else "", data_format)
                            sheet.write(row, 7, line.no_su_proses, data_format)
                            sheet.write(row, 9, line.no_su_material, data_format)
                            if persentase_proses != previous5:
                                sheet.write(row, 8, persentase_proses, data_format)
                                previous5 = persentase_proses
                            if persentase_material != previous6:
                                sheet.write(row, 10, persentase_material, data_format)
                                previous6 = persentase_material
                            if no_lp != previous7:
                                sheet.write(row, 11, no_lp, data_format)
                                previous7 = no_lp
                            if tk_pengiriman != previous8:
                                sheet.write(row, 12, tk_pengiriman, data_format)
                                previous8 = tk_pengiriman
                            row+=1
                    
                sum_su_proses = sum(line.no_su_proses for line in inspection.operation_line_ids) 
                sum_persentase_proses = sum(move.persentase_proses for move in inspection.product_line_ids) 
                sum_su_material = sum(line.no_su_material for line in inspection.operation_line_ids) 
                sum_persentase_material = sum(move.persentase_material for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_pengiriman = sum(move.tk_pengiriman for move in inspection.product_line_ids)  
                sum_persentase_harian_pengiriman = sum(ins.persentase_harian_pengiriman for ins in inspection)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,sum_su_proses, label_table)
                sheet.write(row, 8,round(sum_persentase_proses, 2), label_table)
                sheet.write(row, 9,sum_su_material, label_table)
                sheet.write(row, 10,round(sum_persentase_material, 2), label_table)
                sheet.write(row, 11,sum_no_lp, label_table)
                sheet.write(row, 12,sum_tk_pengiriman, label_table)
                sheet.write(row, 13,round(sum_persentase_harian_pengiriman, 2), label_table3)
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
                
                row = 8
                for ins in inspection:
                    sheet.write(row, 16, round(ins.persentase_harian_finishing, 2), data_format)
                    for move in ins.product_line_ids:
                        for line in ins.operation_line_ids:
                            product_template_name = ins.product_template_id.name if ins.product_template_id else ""
                            no_mo_name = ins.no_mo_id.name if ins.no_mo_id else ""
                            fabric_colour_id = line.fabric_colour_id.name if line.fabric_colour_id else ""
                            product_uom_qty = move.product_uom_qty
                            persentase_production = round(move.persentase_production, 2)
                            persentase_pre_finishing = round(move.persentase_pre_finishing, 2)
                            persentase_kbl = round(move.persentase_kbl, 2)
                            no_lp = move.no_lp
                            tk_finishing = move.tk_finishing
                            if product_template_name != previous1:
                                sheet.write(row, 0, product_template_name, data_format)
                                previous1 = product_template_name
                            if no_mo_name != previous2:
                                sheet.write(row, 1, no_mo_name, data_format)
                                previous2 = no_mo_name
                            if product_uom_qty != previous3:
                                sheet.write(row, 2, product_uom_qty, data_format)
                                previous3 = product_uom_qty
                            if fabric_colour_id != previous4:
                                sheet.write(row, 3, fabric_colour_id, data_format)
                                previous4 = fabric_colour_id
                            else:
                                fabric_colour_id = ""
                            sheet.write(row, 4, line.product_id.name, data_format)
                            sheet.write(row, 5, line.defect_production_id.name if line.defect_production_id.name else "", data_format)
                            sheet.write(row, 6, line.defect_pre_finishing_id.name if line.defect_pre_finishing_id.name else "", data_format)
                            sheet.write(row, 7, line.defect_kbl_id.name if line.defect_kbl_id.name else "", data_format)
                            sheet.write(row, 8, line.su_prodution, data_format)
                            sheet.write(row, 10, line.su_pre_finishing, data_format)
                            sheet.write(row, 12, line.su_kbl, data_format)
                            if persentase_production != previous5:
                                sheet.write(row, 9, persentase_production, data_format)
                                previous5 = persentase_production
                            if persentase_pre_finishing != previous6:
                                sheet.write(row, 11, persentase_pre_finishing, data_format)
                                previous6 = persentase_pre_finishing
                            if persentase_kbl != previous7:
                                sheet.write(row, 13, persentase_kbl, data_format)
                                previous7 = persentase_kbl
                            if no_lp != previous8:
                                sheet.write(row, 14, no_lp, data_format)
                                previous8 = no_lp
                            if tk_finishing != previous9:
                                sheet.write(row, 15, tk_finishing, data_format)
                                previous9 = tk_finishing
                            sheet.write(row, 3, fabric_colour_id, data_format)
                            row+=1
                        
                sum_su_prodution = sum(line.su_prodution for line in inspection.operation_line_ids) 
                sum_persentase_production = sum(move.persentase_production for move in inspection.product_line_ids) 
                sum_su_pre_finishing = sum(line.su_pre_finishing for line in inspection.operation_line_ids) 
                sum_persentase_pre_finishing = sum(move.persentase_pre_finishing for move in inspection.product_line_ids) 
                sum_su_kbl = sum(line.su_kbl for line in inspection.operation_line_ids) 
                sum_persentase_kbl = sum(move.persentase_kbl for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_finishing = sum(move.tk_finishing for move in inspection.product_line_ids)  
                sum_persentase_harian_finishing = sum(ins.persentase_harian_finishing for ins in inspection) 
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,None, label_table)
                sheet.write(row, 8,sum_su_prodution, label_table)
                sheet.write(row, 9,round(sum_persentase_production, 2), label_table)
                sheet.write(row, 10,sum_su_pre_finishing, label_table)
                sheet.write(row, 11,round(sum_persentase_pre_finishing, 2), label_table)
                sheet.write(row, 12,sum_su_kbl, label_table)
                sheet.write(row, 13,round(sum_persentase_kbl, 2), label_table)
                sheet.write(row, 14,sum_no_lp, label_table)
                sheet.write(row, 15,sum_tk_finishing, label_table)
                sheet.write(row, 16,round(sum_persentase_harian_finishing, 2), label_table3)
                row+=1
                
            elif obj.type_qc == 'top_coat':
                sheet.merge_range(0, 0, 0, 16, "SERVICE RATE TOP COAT FINISHING", text_top_style)
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
                
                row = 8
                for ins in inspection: 
                    sheet.write(row, 16, round(ins.persentase_harian_coat, 2), data_format)
                    for move in ins.product_line_ids:
                        sheet.write(row, 9, round(move.persentase_proeses, 2), data_format)
                        sheet.write(row, 15, move.tk_coat, data_format)
                        for line in ins.operation_line_ids:
                            product_template_name = ins.product_template_id.name if ins.product_template_id else ""
                            no_mo_name = ins.no_mo_id.name if ins.no_mo_id else ""
                            fabric_colour_id = line.fabric_colour_id.name if line.fabric_colour_id else ""
                            su_proses_coat = line.su_proses_coat
                            su_pre_finishing_coat = line.su_pre_finishing_coat
                            su_coat_finishing = line.su_coat_finishing
                            product_uom_qty = move.product_uom_qty
                            persentase_pre_finishing_coat = round(move.persentase_pre_finishing_coat, 2)
                            persentase_coat_finishing = round(move.persentase_coat_finishing, 2)
                            no_lp = move.no_lp
                            if product_template_name != previous1:
                                sheet.write(row, 0, product_template_name, data_format)
                                previous1 = product_template_name
                            if no_mo_name != previous2:
                                sheet.write(row, 1, no_mo_name, data_format)
                                previous2 = no_mo_name
                            if product_uom_qty != previous3:
                                sheet.write(row, 2, product_uom_qty, data_format)
                                previous3 = product_uom_qty
                            if fabric_colour_id != previous4:
                                sheet.write(row, 3, fabric_colour_id, data_format)
                                previous4 = fabric_colour_id
                            else:
                                fabric_colour_id = ""
                            sheet.write(row, 4, line.product_id.name, data_format)
                            sheet.write(row, 5, line.defect_proses_coat_id.name if line.defect_proses_coat_id.name else "", data_format)
                            sheet.write(row, 6, line.defect_pre_finishing_coat_id.name if line.defect_pre_finishing_coat_id.name else "", data_format)
                            sheet.write(row, 7, line.defect_coat_finishing_id.name if line.defect_coat_finishing_id.name else "", data_format)
                            if su_proses_coat != previous5:
                                sheet.write(row, 8, su_proses_coat, data_format)
                                previous5 = su_proses_coat
                            if su_pre_finishing_coat != previous6:
                                sheet.write(row, 10, su_pre_finishing_coat, data_format)
                                previous6 = su_pre_finishing_coat
                            if su_coat_finishing != previous7:
                                sheet.write(row, 12, su_coat_finishing, data_format)
                                previous7 = su_coat_finishing
                            if persentase_pre_finishing_coat != previous8:
                                sheet.write(row, 11, persentase_pre_finishing_coat, data_format)
                                previous8 = persentase_pre_finishing_coat
                            if persentase_coat_finishing != previous9:
                                sheet.write(row, 13, persentase_coat_finishing, data_format)
                                previous9 = persentase_coat_finishing
                            if no_lp != previous10:
                                sheet.write(row, 14, no_lp, data_format)
                                previous10 = no_lp
                            sheet.write(row, 3, fabric_colour_id, data_format)
                            row+=1
                        
                sum_su_proses_coat = sum(line.su_proses_coat for line in inspection.operation_line_ids) 
                sum_persentase_proeses = sum(move.persentase_proeses for move in inspection.product_line_ids) 
                sum_su_pre_finishing_coat = sum(line.su_pre_finishing_coat for line in inspection.operation_line_ids) 
                sum_persentase_pre_finishing_coat = sum(move.persentase_pre_finishing_coat for move in inspection.product_line_ids) 
                sum_su_coat_finishing = sum(line.su_coat_finishing for line in inspection.operation_line_ids) 
                sum_persentase_coat_finishing = sum(move.persentase_coat_finishing for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_coat = sum(move.tk_coat for move in inspection.product_line_ids)  
                sum_persentase_harian_coat = sum(ins.persentase_harian_coat for ins in inspection)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,None, label_table)
                sheet.write(row, 8,sum_su_proses_coat, label_table)
                sheet.write(row, 9,round(sum_persentase_proeses, 2), label_table)
                sheet.write(row, 10,sum_su_pre_finishing_coat, label_table)
                sheet.write(row, 11,round(sum_persentase_pre_finishing_coat, 2), label_table)
                sheet.write(row, 12,sum_su_coat_finishing, label_table)
                sheet.write(row, 13,round(sum_persentase_coat_finishing, 2), label_table)
                sheet.write(row, 14,sum_no_lp, label_table)
                sheet.write(row, 15,sum_tk_coat, label_table)
                sheet.write(row, 16,round(sum_persentase_harian_coat, 2), label_table3)
                row+=1
                
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
                sheet.merge_range(6, 9, 7, 9,"% PRODUKSI", label_table)
                sheet.merge_range(6, 10, 7, 10,"SU PRE FINISHING", label_table)
                sheet.merge_range(6, 11, 7, 11,"% PRE FINISHING", label_table)
                sheet.merge_range(6, 12, 7, 12,"SU TOP PACKING FINISHING", label_table)
                sheet.merge_range(6, 13, 7, 13,"% TOP PACKING FINISHING", label_table)
                sheet.merge_range(6, 14, 7, 14,"TOTAL OK/LP", label_table)
                sheet.merge_range(6, 15, 7, 15,"TOTAL KIRIM", label_table)
                sheet.merge_range(6, 16, 7, 16,"% HARIAN", label_table)
                
                row = 8
                for ins in inspection: 
                    for move in ins.product_line_ids:
                        sheet.write(row, 9, round(move.persentase_proeses_packing, 2), data_format) #not loop
                        for line in ins.operation_line_ids:
                            product_template_name = ins.product_template_id.name if ins.product_template_id else ""
                            no_mo_name = ins.no_mo_id.name if ins.no_mo_id else ""
                            fabric_colour_id = line.fabric_colour_id.name if line.fabric_colour_id else ""
                            product_uom_qty = move.product_uom_qty
                            persentase_pre_finishing_packing = round(move.persentase_pre_finishing_packing, 2)
                            persentase_packing_finishing = round(move.persentase_packing_finishing, 2)
                            no_lp = move.no_lp
                            tk_packing = move.tk_packing
                            persentase_harian_packing = round(ins.persentase_harian_packing, 2)
                            if product_template_name != previous1:
                                sheet.write(row, 0, product_template_name, data_format)
                                previous1 = product_template_name
                            if no_mo_name != previous2:
                                sheet.write(row, 1, no_mo_name, data_format)
                                previous2 = no_mo_name
                            if product_uom_qty != previous3:
                                sheet.write(row, 2, product_uom_qty, data_format)
                                previous3 = product_uom_qty
                            if fabric_colour_id != previous4:
                                sheet.write(row, 3, fabric_colour_id, data_format)
                                previous4 = fabric_colour_id
                            else:
                                fabric_colour_id = ""
                            sheet.write(row, 4, line.product_id.name, data_format)
                            sheet.write(row, 5, line.defect_proses_packing_id.name if line.defect_proses_packing_id.name else "", data_format)
                            sheet.write(row, 6, line.defect_pre_finishing_packing_id.name if line.defect_pre_finishing_packing_id.name else "", data_format)
                            sheet.write(row, 7, line.defect_packing_finishing_id.name if line.defect_packing_finishing_id.name else "", data_format)
                            sheet.write(row, 8, line.su_proses_packing, data_format)
                            sheet.write(row, 10, line.su_pre_finishing_packing, data_format)
                            sheet.write(row, 12, line.su_packing_finishing, data_format)
                            if persentase_pre_finishing_packing != previous5:
                                sheet.write(row, 11, persentase_pre_finishing_packing, data_format)
                                previous5 = persentase_pre_finishing_packing
                            if persentase_packing_finishing != previous6:
                                sheet.write(row, 13, persentase_packing_finishing, data_format)
                                previous6 = persentase_packing_finishing
                            if no_lp != previous7:
                                sheet.write(row, 14, no_lp, data_format)
                                previous7 = no_lp
                            if tk_packing != previous8:
                                sheet.write(row, 15, tk_packing, data_format)
                                previous8 = tk_packing
                            if persentase_harian_packing != previous9:
                                sheet.write(row, 16, persentase_harian_packing, data_format)
                                previous9 = persentase_harian_packing
                            sheet.write(row, 3, fabric_colour_id, data_format)
                            row+=1
                        
                sum_su_proses_packing = sum(line.su_proses_packing for line in inspection.operation_line_ids) 
                sum_persentase_proeses = sum(move.persentase_proeses_packing for move in inspection.product_line_ids) 
                sum_su_pre_finishing_packing = sum(line.su_pre_finishing_packing for line in inspection.operation_line_ids) 
                sum_persentase_pre_finishing_coat = sum(move.persentase_pre_finishing_packing for move in inspection.product_line_ids) 
                sum_su_packing_finishing = sum(line.su_packing_finishing for line in inspection.operation_line_ids) 
                sum_persentase_coat_finishing = sum(move.persentase_packing_finishing for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_packing = sum(move.tk_packing for move in inspection.product_line_ids)  
                sum_persentase_harian_packing = sum(ins.persentase_harian_packing for ins in inspection)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,None, label_table)
                sheet.write(row, 6,None, label_table)
                sheet.write(row, 7,None, label_table)
                sheet.write(row, 8,sum_su_proses_packing, label_table)
                sheet.write(row, 9,round(sum_persentase_proeses, 2), label_table)
                sheet.write(row, 10,sum_su_pre_finishing_packing, label_table)
                sheet.write(row, 11,round(sum_persentase_pre_finishing_coat, 2), label_table)
                sheet.write(row, 12,sum_su_packing_finishing, label_table)
                sheet.write(row, 13,round(sum_persentase_coat_finishing, 2), label_table)
                sheet.write(row, 14,sum_no_lp, label_table)
                sheet.write(row, 15,sum_tk_packing, label_table)
                sheet.write(row, 16,round(sum_persentase_harian_packing, 2), label_table3)
                row+=1
            
            elif obj.type_qc == 'cushion':
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
                
                row = 8
                for ins in inspection: 
                    for move in ins.product_line_ids:#if line multiple=move x line
                        sheet.write(row, 6, round(move.persentase_cushion, 2), data_format) #display even same value
                        sheet.write(row, 9, round(ins.persentase_harian_cushion, 2), data_format)
                        for line in ins.operation_line_ids:
                            product_template_name = ins.product_template_id.name if ins.product_template_id else ""
                            no_mo_name = ins.no_mo_id.name if ins.no_mo_id else ""
                            fabric_colour_id = line.fabric_colour_id.name if line.fabric_colour_id else ""
                            no_lp = move.no_lp
                            tk_cushion = move.tk_cushion
                            if product_template_name != previous1:#if .ins before .line = inside, else = outside
                                sheet.write(row, 0, product_template_name, data_format)
                                previous1 = product_template_name
                            if no_mo_name != previous2:
                                sheet.write(row, 1, no_mo_name, data_format)
                                previous2 = no_mo_name
                            if fabric_colour_id != previous3: #not display if same value
                                sheet.write(row, 2, fabric_colour_id, data_format)
                                previous3 = fabric_colour_id
                            else:
                                fabric_colour_id = ""
                            sheet.write(row, 3, line.product_id.name, data_format)
                            sheet.write(row, 4, line.defect_cushion_id.name if line.defect_cushion_id.name else "", data_format)
                            sheet.write(row, 5, line.jumlah_cushion, data_format) 
                            if no_lp != previous5:
                                sheet.write(row, 7, no_lp, data_format)
                                previous5 = no_lp
                            if tk_cushion != previous6:
                                sheet.write(row, 8, tk_cushion, data_format)
                                previous6 = tk_cushion
                            sheet.write(row, 2, fabric_colour_id, data_format)
                            row+=1
                        
                sum_jumlah = sum(line.jumlah_cushion for line in inspection.operation_line_ids) 
                sum_persentase_cushion = sum(move.persentase_cushion for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_cushion = sum(move.tk_cushion for move in inspection.product_line_ids)  
                sum_persentase_harian_cushion = sum(ins.persentase_harian_cushion for ins in inspection)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,sum_jumlah, label_table)
                sheet.write(row, 6,round(sum_persentase_cushion, 2), label_table)
                sheet.write(row, 7,sum_no_lp, label_table)
                sheet.write(row, 8,sum_tk_cushion, label_table)
                sheet.write(row, 9,round(sum_persentase_harian_cushion, 2), label_table3)
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
                
                row = 8
                for ins in inspection: 
                    sheet.write(row, 9, round(ins.persentase_harian_kawai_top, 2), data_format)
                    for move in ins.product_line_ids:
                        sheet.write(row, 6, round(move.persentese_kawai, 2), data_format)
                        for line in ins.operation_line_ids:
                            product_template_name = ins.product_template_id.name if ins.product_template_id else ""
                            no_mo_name = ins.no_mo_id.name if ins.no_mo_id else ""
                            fabric_colour_id = line.fabric_colour_id.name if line.fabric_colour_id else ""
                            no_lp = move.no_lp
                            tk_kawai_top = move.tk_kawai_top
                            if product_template_name != previous1:
                                sheet.write(row, 0, product_template_name, data_format)
                                previous1 = product_template_name
                            if no_mo_name != previous2:
                                sheet.write(row, 1, no_mo_name, data_format)
                                previous2 = no_mo_name
                            if fabric_colour_id != previous3:
                                sheet.write(row, 2, fabric_colour_id, data_format)
                                previous3 = fabric_colour_id
                            else:
                                fabric_colour_id = ""
                            sheet.write(row, 3, line.product_id.name, data_format)
                            sheet.write(row, 4, line.defect_kawai_id.name if line.defect_kawai_id.name else "", data_format)
                            sheet.write(row, 5, line.su_kawai_top, data_format)
                            if no_lp != previous5:
                                sheet.write(row, 7, no_lp, data_format)
                                previous5 = no_lp
                            if tk_kawai_top != previous6:
                                sheet.write(row, 8, tk_kawai_top, data_format)
                                previous6 = tk_kawai_top
                            sheet.write(row, 2, fabric_colour_id, data_format)
                            row+=1
                        
                sum_su_kawai_top = sum(line.su_kawai_top for line in inspection.operation_line_ids) 
                sum_persentese_kawai = sum(move.persentese_kawai for move in inspection.product_line_ids) 
                sum_no_lp = sum(move.no_lp for move in inspection.product_line_ids)  
                sum_tk_kawai_top = sum(move.tk_kawai_top for move in inspection.product_line_ids)  
                sum_persentase_harian_kawai_top = sum(ins.persentase_harian_kawai_top for ins in inspection)  
                
                sheet.write(row, 0,"Grand Total", label_table)
                sheet.write(row, 1,None, label_table)
                sheet.write(row, 2,None, label_table)
                sheet.write(row, 3,None, label_table)
                sheet.write(row, 4,None, label_table)
                sheet.write(row, 5,sum_su_kawai_top, label_table)
                sheet.write(row, 6,round(sum_persentese_kawai, 2), label_table)
                sheet.write(row, 7,sum_no_lp, label_table)
                sheet.write(row, 8,sum_tk_kawai_top, label_table)
                sheet.write(row, 9,round(sum_persentase_harian_kawai_top, 2), label_table3)
                row+=1