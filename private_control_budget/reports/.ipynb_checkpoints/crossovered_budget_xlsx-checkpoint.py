from odoo import _, models


class CrossoveredBudgetXslx(models.AbstractModel):
    _name = 'report.c_b.report_crossovered_budget_xlsx'
    _inherit = 'report.control_budget.abstract_report_xlsx'

    def _get_report_name(self, report):
        report_name = _('Suivi Budgetaire')
        return self._get_report_complete_name(report, report_name)


    def _get_report_columns(self, report):
        res = {
            0: {'header': _('Poste budgétaire'), 'field': 'general_budget', 'width': 20},
            1: {'header': _('Compte analytique'), 'field': 'account_analytic', 'width': 20},
            2: {'header': _('Montant prevu'), 'field': 'planned_amount', 'width': 20},
            3: {'header': _('Montant engage'), 'field': 'engage_amount', 'width': 20},
            4: {'header': _('Montant realise'), 'field': 'practical_amount', 'width': 20},
            5: {'header': _('Montant disponible'), 'field': 'available_amount', 'width': 20},
        }

        return res

    def _get_report_filters(self, report):
        return [
            [
                _('Periode'),
                _('Du: %s Au: %s') % (report.date_from, report.date_to),
            ],
        ]

    def _get_col_count_filter_name(self):
        return 2

    def _get_col_count_filter_value(self):
        return 4

    def _generate_report_content(self, workbook, report):
        self.write_array_header()
        for line in report.line_ids:
            self.write_line(line)
