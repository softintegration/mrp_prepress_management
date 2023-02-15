# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    by_product_prepress_proof_id = fields.Many2one('prepress.proof',string='Prepress proof')

    @api.onchange('product_id')
    def _onchange_by_product_id(self):
        self._update_by_product_prepress_proof()

    def _update_by_product_prepress_proof(self):
        if not self.product_id:
            return
        prepress_proof = self.env['prepress.proof']._get_by_product(self.product_id)
        self.update({'by_product_prepress_proof_id': prepress_proof and prepress_proof.ids[0] or False})
