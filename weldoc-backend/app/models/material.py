from app.database import db

# Association table for material connections (self-referential many-to-many)
material_connections = db.Table(
    "weldoc_material_connections",
    db.Column("material_id", db.Integer, db.ForeignKey("weldoc_materials.id")),
    db.Column("connected_id", db.Integer, db.ForeignKey("weldoc_materials.id")),
)


class Material(db.Model):
    __tablename__ = "weldoc_materials"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pipeline_id = db.Column(db.Integer, db.ForeignKey("weldoc_pipelines.id"), nullable=False)
    position = db.Column(db.String(5))
    category = db.Column(db.String(100))
    dn1 = db.Column(db.String(50))
    dn2 = db.Column(db.String(50))
    dn3 = db.Column(db.String(50))
    dn4 = db.Column(db.String(50))
    dn5 = db.Column(db.String(50))
    dn6 = db.Column(db.String(50))
    diameter = db.Column(db.String(50))
    thickness = db.Column(db.String(50))
    surface = db.Column(db.String(100))
    item_description = db.Column(db.String(300))
    material_code = db.Column(db.String(50))
    dien_no = db.Column(db.String(100))
    certificate = db.Column(db.String(100))
    heat_no = db.Column(db.String(200))
    waz_no = db.Column(db.String(50))
    waz_pdf_url = db.Column(db.String(500))
    start_of_plumbing = db.Column(db.Boolean, default=False)
    end_of_plumbing = db.Column(db.Boolean, default=False)
    archived = db.Column(db.Boolean, default=False)

    connections = db.relationship(
        "Material",
        secondary=material_connections,
        primaryjoin=id == material_connections.c.material_id,
        secondaryjoin=id == material_connections.c.connected_id,
        lazy="subquery",
    )
