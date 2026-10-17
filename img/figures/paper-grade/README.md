# Editable industrial-agent method figure examples

Two original conceptual design examples, not measured results or validated novel methods. All records, boolean conditions and signal traces are illustrative fixtures. No source-paper figure artwork is reused.

Each diagram includes a `.drawio` file with native objects and anchored connectors, a grouped `.svg` with whole editable text, vector `.pdf` and `.png` preview. Open `.drawio` in diagrams.net; open `.svg` in Inkscape. SVG paths do not automatically track moved modules, so recheck connections after moving them.

Read `docs/figures-paper-grade/README.md` for the SOP and `design-contract.md` for the design. Run from the unpacked project root:

```
python scripts/build_paper_grade_figures.py
python scripts/check_paper_grade_figures.py
```

The generator requires Python and Inkscape on PATH. The checker needs Pillow, PyMuPDF and Linux Liberation Sans font files. Renderers may have minor font/rounding differences. The print proof uses provisional 182 mm width (minimum type 7.27 pt); it is an A4 reading proof, not official conference-template compliance.

Keep manual revisions separately and record which file is the current master. Regeneration overwrites generated outputs and does not synchronize edits back from draw.io or Inkscape. Current QA is in verification.json and the review record. Object-structure checks are separate from actual editor-import/export validation.


本轮编辑器状态：SVG/Inkscape 的模块移动、整句改字和 PDF 重导出已实测通过；draw.io 对象和连线引用结构检查通过，但网页编辑器打开／导出验收受网络阻断，未计为通过。当前经过实际验证的人工编辑路线是 SVG → Inkscape。详见 editor-validation.json。
