from flask import Blueprint, request, jsonify
from app.database import db
from app.models.pipeline import Pipeline
from app.models.project import Project
from app.models.client import Client
from app.models.material import Material
from app.models.weld import Weld

pipelines_bp = Blueprint("pipelines", __name__)


@pipelines_bp.route("", methods=["GET"])
def get_pipelines():
    archived = request.args.get("archived", "false").lower() == "true"
    project_id = request.args.get("projectId", type=int)
    query = Pipeline.query.filter_by(archived=archived)
    if project_id:
        query = query.filter_by(project_id=project_id)
    rows = query.all()
    return jsonify([_serialize(p) for p in rows])


@pipelines_bp.route("/<int:pipeline_id>", methods=["GET"])
def get_pipeline(pipeline_id):
    p = Pipeline.query.get_or_404(pipeline_id)
    return jsonify(_serialize(p))


@pipelines_bp.route("", methods=["POST"])
def create_or_update_pipeline():
    data = request.get_json()
    if "id" in data and data["id"]:
        p = Pipeline.query.get_or_404(data["id"])
        p.project_id = data.get("projectId", p.project_id)
        p.no = data.get("no", p.no)
        p.plant = data.get("plant", p.plant)
        p.status = data.get("status", p.status)
        p.doc_iso = data.get("docIso", p.doc_iso)
        p.doc_builder = data.get("docBuilder", p.doc_builder)
        p.doc_final = data.get("docFinal", p.doc_final)
        if "archived" in data:
            p.archived = data["archived"]
    else:
        p = Pipeline(
            project_id=data["projectId"],
            no=data["no"],
            plant=data.get("plant", ""),
            status=data.get("status", 0),
        )
        db.session.add(p)
    db.session.commit()
    return jsonify(_serialize(p)), 200


def _serialize(p):
    return {
        "id": p.id,
        "projectId": p.project_id,
        "no": p.no,
        "plant": p.plant,
        "status": p.status,
        "docIso": p.doc_iso,
        "docBuilder": p.doc_builder,
        "docFinal": p.doc_final,
        "archived": p.archived,
    }


@pipelines_bp.route("/<int:pipeline_id>/detail", methods=["GET"])
def get_pipeline_detail(pipeline_id):
    """Single endpoint returning all data needed for the pipeline detail page."""
    pl = Pipeline.query.get_or_404(pipeline_id)
    pr = Project.query.get(pl.project_id) if pl.project_id else None
    cli = Client.query.get(pr.client_id) if pr and pr.client_id else None
    siblings = Pipeline.query.filter_by(project_id=pl.project_id, archived=False).all()
    mats = Material.query.filter_by(pipeline_id=pipeline_id, archived=False).order_by(Material.position).all()
    wlds = Weld.query.filter_by(pipeline_id=pipeline_id, archived=False).order_by(Weld.id).all()

    def ser_client(c):
        return {"id": c.id, "name": c.name, "street": c.street, "zipCode": c.zip_code, "location": c.location, "remarks": c.remarks, "archived": c.archived}

    def ser_project(p):
        return {"id": p.id, "clientId": p.client_id, "istProjectNo": p.ist_project_no, "title": p.title, "location": p.location, "orderNo": p.order_no, "description": p.description, "status": p.status, "archived": p.archived}

    def ser_material(m):
        return {"id": m.id, "pipelineId": m.pipeline_id, "position": m.position, "category": m.category, "dn1": m.dn1, "dn2": m.dn2, "dn3": m.dn3, "dn4": m.dn4, "dn5": m.dn5, "dn6": m.dn6, "diameter": m.diameter, "thickness": m.thickness, "surface": m.surface, "itemDescription": m.item_description, "materialCode": m.material_code, "dienNo": m.dien_no, "certificate": m.certificate, "heatNo": m.heat_no, "wazNo": m.waz_no, "wazPdfUrl": m.waz_pdf_url, "startOfPlumbing": m.start_of_plumbing, "endOfPlumbing": m.end_of_plumbing, "archived": m.archived, "connections": [c.id for c in m.connections]}

    def ser_weld(w):
        return {"id": w.id, "pipelineId": w.pipeline_id, "weldNo": w.weld_no, "betweenA": w.between_a, "betweenB": w.between_b, "type": w.type, "procedure": w.procedure, "weldingWire": w.welding_wire, "welder": w.welder, "inspector": w.inspector, "date": w.date, "endoscopyVideoUrl": w.endoscopy_video_url, "endoscopyImageUrl": w.endoscopy_image_url, "remarks": w.remarks, "archived": w.archived}

    return jsonify({
        "client": ser_client(cli) if cli else None,
        "project": ser_project(pr) if pr else None,
        "pipelines": [_serialize(s) for s in siblings],
        "materials": [ser_material(m) for m in mats],
        "welds": [ser_weld(w) for w in wlds],
    })
