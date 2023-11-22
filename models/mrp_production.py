# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import math

# if the related prepress proof are in one of this states,we have to prevent the confirming of the manufacturing order,
AVOIDED_CONFIRM_RELATED_PROOFS_STATES = ['in_progress','quarantined','cancel']

class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    prepress_proof_id = fields.Many2one('prepress.proof',string='Prepress proof',readonly=True)
    prepress_proof_client_ref = fields.Char(string='Customer Prepress proof reference',
                                            related='prepress_proof_id.client_ref')
    draw_nbr = fields.Integer(string='Draw',compute='_compute_draw_nbr',store=True)
    prepress_type = fields.Many2one(related='product_id.prepress_type',store=True)


    @api.depends('product_qty','bom_id.exposure_nbr')
    def _compute_draw_nbr(self):
        for each in self:
            if each.bom_id and each.bom_id.exposure_nbr:
                not_rounded_draw_nbr = each.product_qty/each.bom_id.exposure_nbr
                each.draw_nbr = math.ceil(not_rounded_draw_nbr)
            else:
                each.draw_nbr = False


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

    def action_confirm(self):
        self._check_prepress_proofs()
        return super(MrpProduction,self).action_confirm()

    def _check_prepress_proofs(self):
        for each in self:
            if each.prepress_proof_id and each.prepress_proof_id.state in AVOIDED_CONFIRM_RELATED_PROOFS_STATES:
                raise ValidationError(_("Can not confirm the Manufacturing order %s,the related proof must be Validated or Flashed!")%each.name)










