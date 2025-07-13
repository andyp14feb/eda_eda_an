# eda_core/io/render_markdown.py

import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from eda_core.utils.logger_utils import setup_logger

logger = setup_logger("render_markdown")

# def render_markdown(column_profiles, table_summary, file_meta, template_dir="eda_core/io/templates") -> str:
#     """
#     📝 Render Markdown Report using Jinja2 Template

#     Parameters:
#         column_profiles (list): List of dicts containing column info + insights
#         table_summary (dict): Overall table-level stats
#         file_meta (dict): Metadata (e.g. source_name, created_at)
#         template_dir (str): Location of Jinja2 template

#     Returns:
#         str: Rendered markdown string
#     """
#     logger.info(f"📄 Rendering markdown report for {file_meta['source_name']}")

#     try:
#         env = Environment(loader=FileSystemLoader(template_dir))
#         template = env.get_template("markdown_template.md.j2")

#         # Inject variables into the template
#         markdown_text = template.render(
#             column_profiles=column_profiles,
#             table_summary=table_summary,
#             file_meta=file_meta
#         )
#         return markdown_text

#     except Exception as e:
#         logger.error(f"❌ Failed to render markdown: {e}")
#         return ""


def render_markdown(column_profiles, table_summary, file_meta, template_dir="eda_core/io/templates") -> str:
    """
    Render a Markdown report using Jinja2 template
    Includes statistics from column_profiles and table_summary.
    """
    logger.info(f"\ud83d\udcc4 Rendering markdown report for {file_meta['source_name']}")

    try:
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("markdown_template.md.j2")

        # Ensure default values for missing table summary keys
        default_table_summary = {
            "total_rows": "-",
            "total_columns": "-",
            "missing_pct": "0.00%",
            "total_outliers": "0"
        }
        for k, v in default_table_summary.items():
            table_summary.setdefault(k, v)

        for col in column_profiles:
            col.setdefault("missing", 0)
            col.setdefault("missing_pct", "0.00%")
            col.setdefault("outlier_count", 0)
            col.setdefault("dtype", "unknown")
            col.setdefault("column", "Unnamed")
            col.setdefault("insight", "(No insight provided)")

        markdown_text = template.render(
            column_profiles=column_profiles,
            table_summary=table_summary,
            file_meta=file_meta
        )
        return markdown_text

    except Exception as e:
        logger.error(f"\u274c Failed to render markdown: {e}")
        return ""
