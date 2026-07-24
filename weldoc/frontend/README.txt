WeldDoc — Pharma Piping Documentation (Milestone 1 interactive mockup)
=====================================================================

HOW TO OPEN
-----------
Unzip anywhere and open  role.html  in a browser (Chrome recommended).
Pick a role (Office staff / Welder-vendor) to reach the Home dashboard.
Navigate with the LEFT SIDEBAR, breadcrumbs, and in-row links.
(Serve over http:// if your browser blocks file:// — e.g. `python -m http.server`.)

FILES
-----
  role.html             Role selection — ENTRY POINT (Office staff vs Welder/Vendor)
  home.html             Home dashboard. Office = pipelines grouped by pending step
                        + certificate tabs (with counts). Vendor = assigned /
                        unassigned pipelines.
  index.html            Clients
  projects.html         Projects (?client=ID to pre-filter)
  project-detail.html   One project: switch projects (of the client) via the name
                        dropdown; its pipelines + stats  (?id=ID)
  pipelines.html        Pipelines (?project=ID or ?client=ID to pre-filter)
  pipeline-detail.html  One pipeline: name dropdown switches pipelines in the same
                        project; workflow stepper + mark-as-done buttons; Material
                        list + Weld list tabs; Seam detail view
                        (?id=ID [&tab=materials|weldlist] [&seam=WELDID])
  material-detail.html  One material: details, connections, welds on it  (?id=ID)
  waz.html              WAZ documents across all clients/projects (grouped, filters)
  materials.html        All materials across all pipelines (filters)
  welders.html          Certificate register
  welder-profile.html   One welder: stats + certificates  (?id=ID)
  styles.css            Shared styling
  app.js                Shared data + logic for every page

NAVIGATION
----------
The top tabs were replaced by a LEFT SIDEBAR:
  Workspace : Home · Clients · Projects · Pipelines
  Documents : WAZ Documents · Materials · Welders
Each item shows a live count. The sidebar footer shows the signed-in role and a
"Switch role" link back to role.html.

PIPELINE LIFECYCLE (6 states)
-----------------------------
  0 Created                       → pending material list creation
  1 Material list done            → pending weld list creation
  2 Weld list done                → builder document ready to download / print
  3 Builder document downloaded   → pending welding-detail update
  4 Welding details updated       → pending export of final document
  5 Exported                      → complete
"Mark material list as done" (material tab) advances 0→1. "Mark weld list as done"
(weld tab, enabled only after step 1) advances 1→2. The builder-document download
button advances 2→3. "Update welding details" (verification modal) advances 3→4.
"Export final document" advances 4→5. Statuses drive the office Home tabs & counts.

DATA / PERSISTENCE
------------------
This is a front-end mockup with no backend. Sample data is stored in the
browser's local storage (key weldoc_db_v3), so edits persist as you move between
pages. "Delete" is now "Archive" (soft-hide). Use "Reset demo data" (top-right)
to restore the original sample and un-archive everything.

KEY BEHAVIOURS
--------------
- Material list is the first tab; Weld list second.
- Add/Edit material: material code, item description, dimension, certificate,
  heat/melt No. and WAZ No. are all dropdown + free-text (pick or type new).
  Selecting a catalogue item description auto-fills its material code (& vice-versa).
- Connections: each material lists the other materials it joins to. Minimum
  connections depend on the plumbing flags (start OR end = 1, middle = 2,
  both = 0, first material = 0). Saving creates ONE weld per connection
  automatically (dimension pre-filled; other weld fields completed later in the
  weld list). Connections are reciprocal.
- Weld modal procedure is dropdown + free-text.
- Multiple welders/inspectors per pipeline/weld: first name shown + "+N" badge
  (click for the full list). Names are colour-coded by certificate validity
  (red = invalid, amber = expiring, blue = valid) unless the pipeline is already
  "Welding completed - submitted".
- Renew certificate: editable new dates + attachment (to SharePoint).

UX IMPROVEMENTS IN THIS VERSION
-------------------------------
1. Real, clickable breadcrumbs in the header carry context between pages.
2. A context bar (Client > Project > Pipeline) on the detail pages, all links.
3. URL-driven filters — every filtered view is a shareable/bookmarkable link.
4. Persistent top nav with live counts; consistent active-tab highlighting.
5. Consistent "click the row / the name / the number" affordances everywhere.
6. Reset-demo control so a reviewer can always get back to a known state.

FURTHER UX IDEAS (not yet built — for discussion)
-------------------------------------------------
- A global search / command palette (jump to any client, pipeline, welder, WAZ).
- "Recently viewed" shortcuts and pinned pipelines.
- A left context rail on detail pages listing sibling pipelines/materials.
- Inline completeness meters (red/green) on list rows, not just tiles.
- Keyboard navigation and bulk actions for office-staff data entry.

Sample line IDs, welder names and certificate numbers are realistic in format
but fictional.
