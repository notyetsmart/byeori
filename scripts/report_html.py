import json
from pathlib import Path


REPORT_PATH = Path("reports/photo_report.json")
HTML_PATH = Path("reports/photo_report.html")


def image_src(path: str) -> str:
    return Path(path).as_uri()


def main():
    if not REPORT_PATH.exists():
        print(f"JSON 리포트가 없습니다: {REPORT_PATH}")
        print("먼저 실행하세요: uv run python -m scripts.report_photos")
        return

    with REPORT_PATH.open("r", encoding="utf-8") as f:
        report = json.load(f)

    similar_pairs = report.get("similar_pairs", [])
    similar_groups = report.get("similar_groups", [])
    exact_duplicates = report.get("exact_duplicates", [])

    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<title>Byeori Photo Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 32px;
    background: #f7f7f7;
}}
h1, h2 {{
    color: #222;
}}
.card {{
    background: white;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}
.row {{
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}}
.photo {{
    width: 260px;
}}
.photo img {{
    width: 260px;
    height: 180px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid #ddd;
}}
.filename {{
    font-weight: bold;
    margin-top: 8px;
}}
.path {{
    font-size: 12px;
    color: #666;
    word-break: break-all;
}}
.score {{
    font-size: 18px;
    font-weight: bold;
    color: #2563eb;
}}
.empty {{
    color: #777;
}}
</style>
</head>
<body>

<h1>Byeori Photo Report</h1>

<div class="card">
    <p><b>Total Photos:</b> {report.get("total_photos")}</p>
    <p><b>Similar Threshold:</b> {report.get("similar_threshold")}</p>
</div>
"""

    html += "<h2>Exact Duplicates</h2>\n"

    if not exact_duplicates:
        html += '<p class="empty">완전 중복 없음</p>\n'

    for i, group in enumerate(exact_duplicates, start=1):
        html += f'<div class="card"><h3>Duplicate Group {i}</h3><div class="row">'
        for item in group:
            html += f"""
            <div class="photo">
                <img src="{image_src(item["path"])}" />
                <div class="filename">{item.get("filename")}</div>
                <div class="path">{item.get("path")}</div>
            </div>
            """
        html += "</div></div>"

    html += "<h2>Similar Pairs</h2>\n"

    if not similar_pairs:
        html += '<p class="empty">유사 pair 없음</p>\n'

    for i, pair in enumerate(similar_pairs, start=1):
        a = pair["a"]
        b = pair["b"]

        html += f"""
        <div class="card">
            <h3>Pair {i}</h3>
            <p class="score">Score: {pair["score"]:.4f}</p>
            <div class="row">
                <div class="photo">
                    <img src="{image_src(a["path"])}" />
                    <div class="filename">{a.get("filename")}</div>
                    <div class="path">{a.get("path")}</div>
                </div>
                <div class="photo">
                    <img src="{image_src(b["path"])}" />
                    <div class="filename">{b.get("filename")}</div>
                    <div class="path">{b.get("path")}</div>
                </div>
            </div>
        </div>
        """

    html += "<h2>Similar Groups</h2>\n"

    if not similar_groups:
        html += '<p class="empty">유사 그룹 없음</p>\n'

    for i, group in enumerate(similar_groups, start=1):
        html += f'<div class="card"><h3>Similar Group {i}</h3><div class="row">'
        for item in group:
            html += f"""
            <div class="photo">
                <img src="{image_src(item["path"])}" />
                <div class="filename">{item.get("filename")}</div>
                <div class="path">{item.get("path")}</div>
            </div>
            """
        html += "</div></div>"

    html += """
</body>
</html>
"""

    HTML_PATH.write_text(html, encoding="utf-8")
    print(f"HTML report saved: {HTML_PATH}")


if __name__ == "__main__":
    main()