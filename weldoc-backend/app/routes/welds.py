from flask import Blueprint, request, jsonify
from app.database import db
from app.models.weld import Weld

welds_bp = Blueprint("welds", __name__)


@welds_bp.route("", methods=["GET"])
def get_welds():
    pipeline_id = request.args.get("pipelineId", type=int)
    archived = request.args.get("archived", "false").lower() == "true"
    query = Weld.query.filter_by(archived=archived)
    if pipeline_id:
        query = query.filter_by(pipeline_id=pipeline_id)
    rows = query.all()
    return jsonify([_serialize(w) for w in rows])


@welds_bp.route("/<int:weld_id>", methods=["GET"])
def get_weld(weld_id):
    w = Weld.query.get_or_404(weld_id)
    return jsonify(_serialize(w))


@welds_bp.route("", methods=["POST"])
def create_or_update_weld():
    data = request.get_json()
    if "id" in data and data["id"]:
        w = Weld.query.get_or_404(data["id"])
        _update(w, data)
    else:
        # Check if weld with same pipeline_id + weld_no already exists
        existing = None
        if "pipelineId" in data and "weldNo" in data:
            existing = Weld.query.filter_by(
                pipeline_id=data["pipelineId"],
                weld_no=data["weldNo"],
                archived=False,
            ).first()
        if existing:
            w = existing
            _update(w, data)
        else:
            w = Weld(pipeline_id=data["pipelineId"])
            _update(w, data)
            db.session.add(w)
    db.session.commit()
    return jsonify(_serialize(w)), 200


def _update(w, data):
    w.pipeline_id = data.get("pipelineId", w.pipeline_id)
    w.weld_no = data.get("weldNo", w.weld_no)
    w.between_a = data.get("betweenA", w.between_a)
    w.between_b = data.get("betweenB", w.between_b)
    w.type = data.get("type", w.type)
    w.procedure = data.get("procedure", w.procedure)
    w.welding_wire = data.get("weldingWire", w.welding_wire)
    w.welder = data.get("welder", w.welder)
    w.inspector = data.get("inspector", w.inspector)
    w.date = data.get("date", w.date)
    w.endoscopy_video_url = data.get("endoscopyVideoUrl", w.endoscopy_video_url)
    w.endoscopy_image_url = data.get("endoscopyImageUrl", w.endoscopy_image_url)
    w.remarks = data.get("remarks", w.remarks)
    if "archived" in data:
        w.archived = data["archived"]


def _serialize(w):
    return {
        "id": w.id,
        "pipelineId": w.pipeline_id,
        "weldNo": w.weld_no,
        "betweenA": w.between_a,
        "betweenB": w.between_b,
        "type": w.type,
        "procedure": w.procedure,
        "weldingWire": w.welding_wire,
        "welder": w.welder,
        "inspector": w.inspector,
        "date": w.date,
        "endoscopyVideoUrl": w.endoscopy_video_url,
        "endoscopyImageUrl": w.endoscopy_image_url,
        "remarks": w.remarks,
        "archived": w.archived,
    }
