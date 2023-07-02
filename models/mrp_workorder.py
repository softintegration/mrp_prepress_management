# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_round
import math


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    passes_nbr = fields.Integer(string='Number of passes',compute='_compute_passes_nbr')
    is_printer = fields.Boolean(related='workcenter_id.equipment_id.is_printer')

    @api.depends('product_id.color_cpt','workcenter_id.equipment_id.color_cpt')
    def _compute_passes_nbr(self):
        for each in self:
            if each.workcenter_id.equipment_id and each.workcenter_id.equipment_id.is_printer:
                not_rounded_passes_nbr = each.product_id.color_cpt/(each.workcenter_id.equipment_id.color_cpt or 1)
                each.passes_nbr = math.ceil(not_rounded_passes_nbr)
            else:
                each.passes_nbr = 1





    def _get_duration_expected(self, alternative_workcenter=False, ratio=1):
        self.ensure_one()
        if not self.workcenter_id:
            return self.duration_expected
        if not self.operation_id:
            duration_expected_working = (self.duration_expected - self.workcenter_id.time_start - self.workcenter_id.time_stop) * self.workcenter_id.time_efficiency / 100.0
            if duration_expected_working < 0:
                duration_expected_working = 0
            return self.workcenter_id.time_start + self.workcenter_id.time_stop + duration_expected_working * ratio * 100.0 / self.workcenter_id.time_efficiency
        if self.operation_id.draw_based_duration:
            qty_production = self.production_id.draw_nbr
        else:
            qty_production = self.production_id.product_uom_id._compute_quantity(self.qty_production, self.production_id.product_id.uom_id)
        cycle_number = float_round(qty_production / self.workcenter_id.capacity, precision_digits=0, rounding_method='UP')
        if alternative_workcenter:
            # TODO : find a better alternative : the settings of workcenter can change
            duration_expected_working = (self.duration_expected - self.workcenter_id.time_start - self.workcenter_id.time_stop) * self.workcenter_id.time_efficiency / (100.0 * cycle_number)
            if duration_expected_working < 0:
                duration_expected_working = 0
            alternative_wc_cycle_nb = float_round(qty_production / alternative_workcenter.capacity, precision_digits=0, rounding_method='UP')
            return alternative_workcenter.time_start + alternative_workcenter.time_stop + alternative_wc_cycle_nb * duration_expected_working * 100.0 / alternative_workcenter.time_efficiency
        time_cycle = self.operation_id.time_cycle
        return self.workcenter_id.time_start + self.workcenter_id.time_stop + cycle_number * time_cycle * 100.0 / self.workcenter_id.time_efficiency