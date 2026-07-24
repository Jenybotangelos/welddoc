from app.database import db


class Weld(db.Model):
    __tablename__ = "weldoc_welds"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pipeline_id = db.Column(db.Integer, db.ForeignKey("weldoc_pipelines.id"), nullable=False)
    weld_no = db.Column(db.String(20))
    between_a = db.Column(db.String(5))
    between_b = db.Column(db.String(5))
    type = db.Column(db.String(10))
    procedure = db.Column(db.String(50))
    welding_wire = db.Column(db.String(200))
    welder = db.Column(db.String(200))
    inspector = db.Column(db.String(200))
    date = db.Column(db.String(20))
    endoscopy_video_url = db.Column(db.String(500))
    endoscopy_image_url = db.Column(db.String(500))
    remarks = db.Column(db.Text)
    archived = db.Column(db.Boolean, default=False)
