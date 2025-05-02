import json
from urllib.parse import parse_qs


def application(environ, start_response):
    params = parse_qs(environ.get("QUERY_STRING", ""))
    file_name = params.get("file", [""])[0]
    file_path = f"/var/www/html/{file_name}"

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            headers = data["Mainline"]["Table"]["Header"]["Data"]
            rows = data["Mainline"]["Table"]["Row"]

            html = "<html><body><table border='1'><tr>"
            for h in headers:
                html += f"<th>{h}</th>"
            html += "</tr>"

            for row in rows:
                html += "<tr>"
                html += f"<td>{row.get('Company', '')}</td>"
                html += f"<td>{row.get('Services', '')}</td>"
                html += f"<td>{', '.join(row.get('Hubs', {}).get('Hub', []))}</td>"
                html += f"<td>{row.get('Revenue', '')}</td>"
                html += f"<td><a href='{row.get('HomePage', '')}' target='_blank'>HomePage</a></td>"
                html += f"<td><img src='/static/{row.get('Logo', '')}' width='50'></td>"
                html += "</tr>"

            html += "</table></body></html>"
            start_response(
                "200 OK",
                [("Content-Type", "text/html"), ("Access-Control-Allow-Origin", "*")],
            )
            return [html.encode("utf-8")]

    except Exception as e:
        import traceback

        start_response(
            "500 Internal Server Error",
            [("Content-Type", "text/plain"), ("Access-Control-Allow-Origin", "*")],
        )
        return [traceback.format_exc().encode("utf-8")]
