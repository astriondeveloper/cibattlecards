"""CLI: python3 -m tools <validate|build|report|export ...>"""
from __future__ import annotations

import argparse
import sys


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="tools", description="Battle card library build tooling")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate", help="check schema, vocab, links, completeness")
    sub.add_parser("build", help="validate and render the static site")
    sub.add_parser("report", help="staleness, pending reviews, coverage gaps")

    export = sub.add_parser("export", help="PDF/DOCX exports")
    what = export.add_subparsers(dest="what", required=True)
    pdf = what.add_parser("pdf", help="print cards to PDF via Chromium")
    pdf.add_argument("slug", nargs="?", help="competitor slug")
    pdf.add_argument("--all", action="store_true", help="every card")
    pdf.add_argument("--share-safe", action="store_true")
    docx = what.add_parser("docx", help="card as a Word document")
    docx.add_argument("slug")
    docx.add_argument("--share-safe", action="store_true")
    pack = what.add_parser("pack", help="ghosting & discriminator pack (DOCX)")
    pack.add_argument("slug")

    args = parser.parse_args(argv)

    if args.cmd == "validate":
        from . import validate
        errors, warnings = validate.run()
        for warning in warnings:
            print(f"WARN  {warning}")
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        if errors:
            print(f"\n{len(errors)} error(s)", file=sys.stderr)
            return 1
        print("validation OK")
        return 0

    if args.cmd == "build":
        from . import build
        build.build()
        return 0

    if args.cmd == "report":
        from . import report
        report.run()
        return 0

    if args.cmd == "export":
        from . import export
        if args.what == "pdf":
            if not args.all and not args.slug:
                print("export pdf: give a slug or --all", file=sys.stderr)
                return 2
            export.export_pdf(slug=args.slug, share_safe=args.share_safe,
                              everything=args.all)
        elif args.what == "docx":
            export.export_docx(args.slug, share_safe=args.share_safe)
        elif args.what == "pack":
            export.export_pack(args.slug)
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
