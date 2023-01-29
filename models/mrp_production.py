# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    prepress_proof_id = fields.Many2one('prepress.proof',string='Prepress proof',readonly=True)
    prepress_proof_client_ref = fields.Char(string='Customer Prepress proof reference',
                                            related='prepress_proof_id.client_ref')

    @api.onchange('product_id', 'picking_type_id', 'company_id')
    def _onchange_product_id(self):
        res = super(MrpProduction, self)._onchange_product_id()
        self._update_prepress_proof()
        return res

    def _update_prepress_proof(self):
        if not self.product_id:
            return
        prepress_proof = self.env['prepress.proof']._get_by_product(self.product_id)
        self.update({'prepress_proof_id': prepress_proof and prepress_proof.ids[0] or False})

    @api.model
    def create(self,vals):
        production_orders = super(MrpProduction, self).create(vals)
        for order in production_orders:
            if not order.prepress_proof_id:
                prepress_proof = self.env['prepress.proof']._get_by_product(order.product_id)
                order.prepress_proof_id = prepress_proof and prepress_proof.ids[0] or False
        return production_orders











