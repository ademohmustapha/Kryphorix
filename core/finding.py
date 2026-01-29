SEVERITY_SCORE = {"Info":1,"Low":3,"Medium":6,"High":9,"Critical":10}

class Finding:
    def __init__(self, title, severity, desc, fix, ref=None):
        self.title = str(title)
        self.severity = severity if severity in SEVERITY_SCORE else "Info"
        self.desc = str(desc)
        self.fix = str(fix)
        self.ref = ref
        self.score = SEVERITY_SCORE.get(self.severity, 1)

    def to_dict(self):
        return {
            "title": self.title,
            "severity": self.severity,
            "desc": self.desc,
            "fix": self.fix,
            "ref": self.ref,
            "score": self.score
        }

    def to_html(self):
        from html import escape

        color_map = {
            "Info": "blue",
            "Low": "green",
            "Medium": "orange",
            "High": "red",
            "Critical": "darkred"
        }

        color = color_map.get(self.severity, "black")

        return (
            "<tr>"
            f"<td>{escape(self.title)}</td>"
            f"<td style='color:{color}'>{escape(self.severity)}</td>"
            f"<td>{escape(self.desc)}</td>"
            f"<td>{escape(self.fix)}</td>"
            "</tr>"
        )

    def __str__(self):
        return f"[{self.severity}] {self.title}\n Issue: {self.desc}\n Fix: {self.fix}\n"

