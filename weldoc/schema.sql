-- WeldDoc Database Schema for Azure SQL
-- Run this script in Azure Portal > Query Editor or SSMS


-- ============================================================
-- CLIENTS
-- ============================================================
CREATE TABLE weldoc_clients (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(200) NOT NULL,
    street NVARCHAR(200),
    zip_code NVARCHAR(20),
    location NVARCHAR(200),
    remarks NVARCHAR(MAX),
    archived BIT DEFAULT 0
);

-- ============================================================
-- PROJECTS
-- ============================================================
CREATE TABLE weldoc_projects (
    id INT IDENTITY(1,1) PRIMARY KEY,
    client_id INT NOT NULL,
    ist_project_no NVARCHAR(100) NOT NULL,
    title NVARCHAR(300),
    location NVARCHAR(200),
    order_no NVARCHAR(100),
    description NVARCHAR(MAX),
    status NVARCHAR(50) DEFAULT 'Not started',
    archived BIT DEFAULT 0,
    CONSTRAINT FK_projects_client FOREIGN KEY (client_id) REFERENCES weldoc_clients(id)
);

-- ============================================================
-- PIPELINES
-- ============================================================
CREATE TABLE weldoc_pipelines (
    id INT IDENTITY(1,1) PRIMARY KEY,
    project_id INT NOT NULL,
    no NVARCHAR(100) NOT NULL,
    plant NVARCHAR(50),
    status INT DEFAULT 0,
    doc_iso NVARCHAR(500),
    doc_builder NVARCHAR(500),
    doc_final NVARCHAR(500),
    archived BIT DEFAULT 0,
    CONSTRAINT FK_pipelines_project FOREIGN KEY (project_id) REFERENCES weldoc_projects(id)
);

-- ============================================================
-- MATERIALS
-- ============================================================
CREATE TABLE weldoc_materials (
    id INT IDENTITY(1,1) PRIMARY KEY,
    pipeline_id INT NOT NULL,
    position NVARCHAR(5),
    category NVARCHAR(100),
    dn1 NVARCHAR(50),
    dn2 NVARCHAR(50),
    dn3 NVARCHAR(50),
    dn4 NVARCHAR(50),
    dn5 NVARCHAR(50),
    dn6 NVARCHAR(50),
    diameter NVARCHAR(50),
    thickness NVARCHAR(50),
    surface NVARCHAR(100),
    item_description NVARCHAR(300),
    material_code NVARCHAR(50),
    dien_no NVARCHAR(100),
    certificate NVARCHAR(100),
    heat_no NVARCHAR(200),
    waz_no NVARCHAR(50),
    waz_pdf_url NVARCHAR(500),
    start_of_plumbing BIT DEFAULT 0,
    end_of_plumbing BIT DEFAULT 0,
    archived BIT DEFAULT 0,
    CONSTRAINT FK_materials_pipeline FOREIGN KEY (pipeline_id) REFERENCES weldoc_pipelines(id)
);

-- ============================================================
-- WELDS
-- ============================================================
CREATE TABLE weldoc_welds (
    id INT IDENTITY(1,1) PRIMARY KEY,
    pipeline_id INT NOT NULL,
    weld_no NVARCHAR(20),
    between_a NVARCHAR(5),
    between_b NVARCHAR(5),
    type NVARCHAR(10),
    [procedure] NVARCHAR(50),
    welding_wire NVARCHAR(200),
    welder NVARCHAR(200),
    inspector NVARCHAR(200),
    date NVARCHAR(20),
    endoscopy_video_url NVARCHAR(500),
    endoscopy_image_url NVARCHAR(500),
    remarks NVARCHAR(MAX),
    archived BIT DEFAULT 0,
    CONSTRAINT FK_welds_pipeline FOREIGN KEY (pipeline_id) REFERENCES weldoc_pipelines(id)
);


