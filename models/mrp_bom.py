# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    prepress_proof_id = fields.Many2one('prepress.proof',string='Prepress proof',readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(MrpBom, self)._onchange_product_id()
        self._update_prepress_proof()
        return res

    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        res = super(MrpBom, self).onchange_product_tmpl_id()
        self._update_prepress_proof(product_tmpl=self.product_tmpl_id)
        return res

    def _update_prepress_proof(self,product_tmpl=False):
        if not self.product_id and not product_tmpl:
            return
        if not product_tmpl:
            prepress_proof = self.env['prepress.proof']._get_by_product(self.product_id)
        else:
            prepress_proof = self.env['prepress.proof']._get_by_product_tmpl_id(product_tmpl.id)
        self.update({'prepress_proof_id': prepress_proof and prepress_proof.ids[0] or False})

    @api.model
    def create(self,vals):
        mrp_boms = super(MrpBom, self).create(vals)
        for bom in mrp_boms:
            if not bom.prepress_proof_id:
                if bom.product_id:
                    prepress_proof = self.env['prepress.proof']._get_by_product(bom.product_id)
                elif bom.product_tmpl_id:
                    prepress_proof = self.env['prepress.proof']._get_by_product_tmpl_id(bom.product_tmpl_id.id)
                bom.prepress_proof_id = prepress_proof and prepress_proof.ids[0] or False
        return mrp_boms











