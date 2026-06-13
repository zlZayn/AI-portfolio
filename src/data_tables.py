"""
Read project CSV/JSON data and produce HTML comparison tables.
Each gen_* function reads from the corresponding sibling project directory
(e.g. AI-decision-maker) and returns an HTML fragment.
"""

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def read_csv(path: Path) -> list[dict]:
    with open(str(path), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def table_css() -> str:
    return """
.data-table { width:100%; border-collapse:collapse; font-size:14px; margin-bottom:28px; }
.data-table th { background:#f1f5f9; padding:8px 12px; text-align:left; font-weight:600; border-bottom:2px solid #d1d5db; white-space:nowrap; color:#2d2b55; }
.data-table td { padding:7px 12px; border-bottom:1px solid #e5e7eb; vertical-align:middle; color:#2d2b55; }
.data-table tr:hover { background:#f8fafc; }
.data-table .dirty { color:#f97316; font-weight:600; }
.data-table .clean { color:#6366f1; font-weight:600; }
.data-table .changed-row { background:#fffbeb; }
.data-table tr.changed-row:hover { background:#fef3c7; }
.data-table .diff { background:#fffbeb; }
.data-table tr:hover td.diff { background:#f8fafc; }
.data-table tr.changed-row:hover td.diff { background:#fef3c7; }
.compare-wrapper { display:flex; gap:24px; margin-bottom:24px; }
.compare-wrapper .data-table { flex:1; }
.compare-wrapper .data-table th:first-child { min-width:50px; }
.arrow-between { display:flex; align-items:center; color:#9ca3af; font-size:24px; font-weight:300; flex-shrink:0; }
.pass-badge { display:inline-block; padding:1px 8px; border-radius:4px; font-size:12px; font-weight:600; }
.pass-badge.pass { background:#f0fdf4; color:#15803d; }
.pass-badge.block { background:#fef2f2; color:#dc2626; }
.pass-badge.review { background:#fffbeb; color:#b45309; }
.section-label { font-weight:700; color:#2d2b55; font-size:14px; margin:24px 0 12px; }
.tabs input[type="radio"] { display:none; }
.tab-headers { display:flex; gap:0; background:#f1f5f9; border-radius:10px; padding:4px; width:fit-content; margin-bottom:20px; flex-wrap:wrap; }
.tab-label { padding:7px 18px; cursor:pointer; font-size:13px; font-weight:600; color:#6c757d; border-radius:8px; transition:all 0.15s; user-select:none; }
.tab-label:hover { color:#2d2b55; }
.tab-panel { display:none; }
.tabs .tab-panel .compare-wrapper { margin-bottom:0; }
#tab-dm-med:checked ~ .tab-headers [for="tab-dm-med"],
#tab-dm-fin:checked ~ .tab-headers [for="tab-dm-fin"],
#tab-dm-user:checked ~ .tab-headers [for="tab-dm-user"] { background:#fff; color:#2d2b55; box-shadow:0 1px 3px rgba(0,0,0,0.1); }
#tab-dm-med:checked ~ .tab-panels [data-tab="med"],
#tab-dm-fin:checked ~ .tab-panels [data-tab="fin"],
#tab-dm-user:checked ~ .tab-panels [data-tab="user"] { display:block; }
"""


def _cmp_span(dirty_val: str, clean_val: str) -> tuple[str, str, bool]:
    d = dirty_val.strip() if dirty_val else ""
    c = clean_val.strip() if clean_val else ""
    changed = d != c and bool(d) and bool(c)
    ds = (
        f'<span class="dirty">{d}</span>'
        if changed and d
        else (d or '<span style="color:#d1d5db">-</span>')
    )
    cs = (
        f'<span class="clean">{c}</span>'
        if changed and c
        else (c or '<span style="color:#d1d5db">-</span>')
    )
    return ds, cs, changed


def _render_comparison(
    dirty_rows: list[dict],
    clean_rows: list[dict],
    id_dirty: str,
    id_clean: str,
    fields: list[str],
    cmap: dict[str, str],
    headers: list[str],
    extra_clean: list[tuple[str, str]] | None = None,
    n: int = 10,
) -> str:
    extra = extra_clean or []
    parts = ['<div class="compare-wrapper">']

    parts.append('<table class="data-table">')
    parts.append("<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>")
    for i in range(n):
        d = dirty_rows[i]
        pid = d.get(id_dirty, "")
        vals = [d.get(f, "").strip() for f in fields]
        parts.append(
            "<tr><td>"
            + pid
            + "</td>"
            + "".join(f"<td>{v}</td>" for v in vals)
            + "</tr>"
        )
    parts.append("</table>")

    parts.append('<div class="arrow-between">→</div>')

    clean_headers = headers + [h for _, h in extra]
    parts.append('<table class="data-table">')
    parts.append("<tr>" + "".join(f"<th>{h}</th>" for h in clean_headers) + "</tr>")
    for i in range(n):
        d = dirty_rows[i]
        c = clean_rows[i]
        pid = c.get(id_clean, "")
        changed = any(
            d.get(f, "").strip() != c.get(cmap.get(f, f), "").strip() for f in fields
        )
        cls = ' class="changed-row"' if changed else ""
        parts.append(f"<tr{cls}>")
        parts.append(f"<td>{pid}</td>")
        for f in fields:
            cf = cmap.get(f, f)
            dv = d.get(f, "").strip()
            cv = c.get(cf, "").strip()
            _, cs, ch = _cmp_span(dv, cv)
            parts.append(f"<td{(' class=diff' if ch else '')}>{cs}</td>")
        for cf, _ in extra:
            parts.append(f"<td>{c.get(cf, '').strip()}</td>")
        parts.append("</tr>")
    parts.append("</table>")
    parts.append("</div>")
    return "".join(parts)


def gen_decision_maker(project_dir: Path) -> str:
    parts = []
    datasets = [
        {
            "id": "med",
            "label": "Medical Data",
            "dirty": read_csv(project_dir / "data" / "dirty" / "medical.csv"),
            "clean": read_csv(project_dir / "data" / "clean" / "medical_clean.csv"),
            "id_dirty": "PID",
            "id_clean": "id",
            "fields": ["SEX/Gender", "AGE", "DEPT", "MED"],
            "cmap": {
                "PID": "id",
                "SEX/Gender": "gender",
                "AGE": "age",
                "DEPT": "department",
                "MED": "drug_name",
            },
            "headers": ["#", "SEX/Gender", "AGE", "DEPT", "MED"],
        },
        {
            "id": "fin",
            "label": "Finance Data",
            "dirty": read_csv(project_dir / "data" / "dirty" / "finance.csv"),
            "clean": read_csv(project_dir / "data" / "clean" / "finance_clean.csv"),
            "id_dirty": "TXN_ID",
            "id_clean": "id",
            "fields": ["AMOUNT", "DATE"],
            "cmap": {"TXN_ID": "id", "AMOUNT": "amount_value", "DATE": "date"},
            "headers": ["#", "AMOUNT", "DATE"],
            "extra_clean": [("amount_currency", "CURRENCY")],
        },
        {
            "id": "user",
            "label": "User Data",
            "dirty": read_csv(project_dir / "data" / "dirty" / "user.csv"),
            "clean": read_csv(project_dir / "data" / "clean" / "user_clean.csv"),
            "id_dirty": "UID",
            "id_clean": "id",
            "fields": ["SEX", "AGE", "E-MAIL", "PHONE_number"],
            "cmap": {
                "UID": "id",
                "SEX": "gender",
                "AGE": "age",
                "E-MAIL": "email",
                "PHONE_number": "phone",
            },
            "headers": ["#", "SEX", "AGE", "E-MAIL", "PHONE_number"],
        },
    ]

    parts.append(
        '<p style="color:#6c757d;font-size:13px;margin-bottom:12px;">同一份数据，左边是原始输入，右边是清洗后输出。AI 只识别字段类型（每次 1 字符），所有清洗操作由代码执行。切换三个数据集看效果。</p>'
    )
    parts.append('<div class="section-label">Before vs After</div>')
    parts.append('<div class="tabs">')

    for i, ds in enumerate(datasets):
        checked = " checked" if i == 0 else ""
        parts.append(
            f'<input type="radio" name="dm-tabs" id="tab-dm-{ds["id"]}"{checked}>'
        )
    parts.append('<div class="tab-headers">')
    for ds in datasets:
        parts.append(
            f'<label class="tab-label" for="tab-dm-{ds["id"]}">{ds["label"]}</label>'
        )
    parts.append("</div>")

    parts.append('<div class="tab-panels">')
    for ds in datasets:
        parts.append(f'<div class="tab-panel" data-tab="{ds["id"]}">')
        parts.append(
            _render_comparison(
                ds["dirty"],
                ds["clean"],
                ds["id_dirty"],
                ds["id_clean"],
                ds["fields"],
                ds["cmap"],
                ds["headers"],
                extra_clean=ds.get("extra_clean"),
            )
        )
        parts.append("</div>")
    parts.append("</div>")
    parts.append("</div>")

    cat_json = project_dir / "data" / "categorical" / "output" / "report.json"
    if cat_json.exists():
        with open(str(cat_json), encoding="utf-8") as f:
            cat_data = json.load(f)
        parts.append(
            '<p style="color:#6c757d;font-size:13px;margin-bottom:12px;">LLM 筛选分类变量 → 判断有序/无序 → R 根据类型组合自动选统计方法（Spearman / Cramer V / Kruskal-Wallis / 卡方检验），全程 AI + 脚本 + R 协作。</p>'
        )
        parts.append(
            '<div class="section-label">Categorical Analysis - Statistical Results</div>'
        )
        parts.append('<table class="data-table">')
        parts.append(
            "<tr><th>File</th><th>Var 1</th><th>Type</th><th>Var 2</th><th>Type</th><th>Method</th><th>Stat</th><th>p-value</th></tr>"
        )
        for row in cat_data:
            parts.append("<tr>")
            parts.append(f"<td>{row.get('file', '')}</td>")
            parts.append(f"<td>{row.get('var1', '')}</td>")
            parts.append(f"<td>{row.get('var1_type', '')}</td>")
            parts.append(f"<td>{row.get('var2', '')}</td>")
            parts.append(f"<td>{row.get('var2_type', '')}</td>")
            parts.append(f"<td>{row.get('method', '')}</td>")
            parts.append(f"<td>{row.get('stat', '')}</td>")
            parts.append(f"<td>{row.get('p', '')}</td>")
            parts.append("</tr>")
        parts.append("</table>")

    return "\n".join(parts)


def gen_schema_mapper(project_dir: Path) -> str:
    parts = []
    dirty = read_csv(project_dir / "data" / "super_dirty_data.csv")
    clean = read_csv(project_dir / "output" / "final_cleaned.csv")
    fields = ["gender", "age", "dept_name", "drug_name", "diagnosis_code"]

    parts.append(
        '<div class="section-label">Before vs After - Medical Data (first 10 rows)</div>'
    )
    parts.append('<div class="compare-wrapper">')

    parts.append('<table class="data-table">')
    parts.append(
        "<tr><th>#</th><th>Gender</th><th>Age</th><th>Dept</th><th>Drug</th><th>Code</th></tr>"
    )
    for d in dirty[:10]:
        pid = d.get("patient_id", "")
        vals = [d.get(f, "").strip() for f in fields]
        parts.append(
            f"<tr><td>{pid}</td>" + "".join(f"<td>{v}</td>" for v in vals) + "</tr>"
        )
    parts.append("</table>")

    parts.append(
        '<div style="display:flex;align-items:center;color:#9ca3af;font-size:24px;font-weight:300;">→</div>'
    )

    parts.append('<table class="data-table">')
    parts.append(
        "<tr><th>#</th><th>Gender</th><th>Age</th><th>Dept</th><th>Drug</th><th>Code</th></tr>"
    )
    for i, c in enumerate(clean[:10]):
        pid = c.get("patient_id", "")
        changed = any(
            dirty[i].get(f, "").strip() != c.get(f, "").strip() for f in fields
        )
        cls = ' class="changed-row"' if changed else ""
        parts.append(f"<tr{cls}>")
        parts.append(f"<td>{pid}</td>")
        for f in fields:
            dv = dirty[i].get(f, "").strip()
            cv = c.get(f, "").strip()
            _, cs, ch = _cmp_span(dv, cv)
            parts.append(f"<td{(' class=diff' if ch else '')}>{cs}</td>")
        parts.append("</tr>")
    parts.append("</table>")
    parts.append("</div>")

    qr = project_dir / "output" / "quality_report.json"
    if qr.exists():
        with open(str(qr), encoding="utf-8") as f:
            qdata = json.load(f)
        parts.append('<div class="section-label">Quality Report</div>')
        parts.append('<table class="data-table">')
        parts.append(
            "<tr><th>Field</th><th>Completeness</th><th>Non-null</th><th>Null</th></tr>"
        )
        for fname, finfo in qdata.get("fields", {}).items():
            parts.append(f"<tr><td>{fname}</td>")
            parts.append(f"<td>{finfo.get('completeness_pct', 0):.1f}%</td>")
            parts.append(f"<td>{finfo.get('non_null_count', 0)}</td>")
            parts.append(f"<td>{finfo.get('null_count', 0)}</td></tr>")
        parts.append(
            f"<tr style='font-weight:700'><td>Overall</td><td>{qdata.get('overall_completeness_pct', 0):.1f}%</td><td colspan=2></td></tr>"
        )
        parts.append("</table>")

    return "\n".join(parts)


def gen_tier_guardian(project_dir: Path) -> str:
    parts = []
    tj = project_dir / "test_results.json"
    if not tj.exists():
        return ""
    with open(str(tj), encoding="utf-8") as f:
        data = json.load(f)

    parts.append('<div class="section-label">Batch Test Results - 10 Cases</div>')
    parts.append('<table class="data-table">')
    parts.append(
        "<tr><th>#</th><th>Text</th><th>Category</th><th>Expected</th><th>Actual</th><th>Intent</th></tr>"
    )
    matches = 0
    for row in data:
        m = row.get("match", False)
        if m:
            matches += 1
        exp = row.get("expected", "")
        act = row.get("actual", "")
        parts.append("<tr>")
        parts.append(f"<td>{row.get('index', '')}</td>")
        parts.append(f"<td style='max-width:200px'>{row.get('text', '')}</td>")
        parts.append(f"<td>{row.get('category', '')}</td>")
        parts.append(f"<td><span class='pass-badge {exp.lower()}'>{exp}</span></td>")
        parts.append(f"<td><span class='pass-badge {act.lower()}'>{act}</span></td>")
        parts.append(f"<td>{row.get('intent', '')}</td>")
        parts.append("</tr>")
    parts.append("</table>")
    parts.append(
        f'<p style="color:#6c757d;font-size:13px">Match rate: {matches}/{len(data)} ({100 * matches // len(data)}%)</p>'
    )

    return "\n".join(parts)


def generate_all() -> dict[str, str]:
    root = BASE_DIR.parent
    result = {}

    dm = root / "AI-decision-maker"
    if dm.exists():
        result["decision-maker"] = gen_decision_maker(dm)

    sm = root / "AI-schema-mapper"
    if sm.exists():
        result["schema-mapper"] = gen_schema_mapper(sm)

    tg = root / "AI-tier-guardian"
    if tg.exists():
        result["tier-guardian"] = gen_tier_guardian(tg)

    return result
