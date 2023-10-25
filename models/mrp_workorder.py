# -*- coding: utf-8 -*- 

import datetime

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from .mrp_production import AVOIDED_CONFIRM_RELATED_PROOFS_STATES
from odoo.exceptions import ValidationError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    planning_id = fields.Many2one('mrp.production.planning')
    partner_id = fields.Many2one(related='product_id.partner_id', string='Customer',store=True,readonly=True)

    def button_start(self):
        self._check_manufacturing_order_proof()
        return super(MrpWorkorder,self).button_start()


    def _check_manufacturing_order_proof(self):
        self.ensure_one()
        if self.production_id.prepress_proof_id and self.production_id.prepress_proof_id.state in AVOIDED_CONFIRM_RELATED_PROOFS_STATES:
            raise ValidationError(
                _("Can not start the Workorder %s,the manufacturing order related proof must be Validated or Flashed!") % self.name)
