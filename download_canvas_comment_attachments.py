#!/usr/bin/env python3
"""Download Canvas assignment submission comment attachments.

This targets files attached in the "Assignment Comments" area of SpeedGrader,
not the main submitted files. It uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def safe_name(value: object, fallback: str = "unknown") -> str:
    text = str(value or "").strip() or fallback
    text = re.sub(r'[\\/:*?"<>|\x00-\x1f]+', "_", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text[:120] or fallback


def parse_link_header(header: str | None) -> dict[str, str]:
    links: dict[str, str] = {}
    if not header:
        return links
    for part in header.split(","):
        match = re.search(r'<([^>]+)>;\s*rel="([^"]+)"', part)
        if match:
            links[match.group(2)] = match.group(1)
    return links


class CanvasClient:
    def __init__(self, base_url: str, token: str, timeout: int = 60) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def _request(self, url: str, accept: str = "application/json") -> urllib.response.addinfourl:
        request = urllib.request.Request(url)
        request.add_header("Authorization", f"Bearer {self.token}")
        request.add_header("Accept", accept)
        return urllib.request.urlopen(request, timeout=self.timeout)

    def get_json_pages(self, path: str, params: dict[str, object]) -> list[dict[str, object]]:
        url = f"{self.base_url}{path}?{urllib.parse.urlencode(params, doseq=True)}"
        rows: list[dict[str, object]] = []
        while url:
            with self._request(url) as response:
                payload = json.loads(response.read().decode("utf-8"))
                if isinstance(payload, list):
                    rows.extend(payload)
                else:
                    raise RuntimeError(f"Expected list response from {url}, got {type(payload).__name__}")
                url = parse_link_header(response.headers.get("Link")).get("next")
        return rows

    def download_file(self, url: str, destination: Path, retries: int = 3) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        last_error: Exception | None = None
        for attempt in range(1, retries + 1):
            try:
                with self._request(url, accept="*/*") as response:
                    with destination.open("wb") as out_file:
                        while True:
                            chunk = response.read(1024 * 1024)
                            if not chunk:
                                return
                            out_file.write(chunk)
            except (urllib.error.URLError, TimeoutError) as exc:
                last_error = exc
                if attempt < retries:
                    time.sleep(2 * attempt)
        raise RuntimeError(f"Failed to download {url}: {last_error}")


def attachment_download_url(attachment: dict[str, object]) -> str | None:
    for key in ("url", "download_url"):
        value = attachment.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def attachment_name(attachment: dict[str, object]) -> str:
    for key in ("filename", "display_name", "name"):
        value = attachment.get(key)
        if isinstance(value, str) and value:
            return safe_name(value, "attachment")
    attachment_id = attachment.get("id")
    return safe_name(f"attachment-{attachment_id}", "attachment")


def assignment_label(assignment: dict[str, object]) -> str:
    assignment_id = assignment.get("id")
    assignment_name = assignment.get("name")
    return safe_name(f"{assignment_id}_{assignment_name}", f"assignment_{assignment_id}")


def user_label(submission: dict[str, object]) -> str:
    user = submission.get("user")
    user_id = submission.get("user_id")
    if isinstance(user, dict):
        sortable_name = user.get("sortable_name")
        name = user.get("name")
        sis_user_id = user.get("sis_user_id")
        parts = [part for part in (sis_user_id, sortable_name or name, user_id) if part]
        if parts:
            return safe_name("_".join(str(part) for part in parts), f"user_{user_id}")
    return safe_name(f"user_{user_id}", "unknown_user")


def unique_destination(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for index in range(2, 10000):
        candidate = path.with_name(f"{stem}_{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Too many duplicate filenames under {path.parent}")


def list_assignments(client: CanvasClient, course_id: str, assignment_id: str | None) -> list[dict[str, object]]:
    if assignment_id:
        return [{"id": assignment_id, "name": f"assignment_{assignment_id}"}]
    return client.get_json_pages(
        f"/api/v1/courses/{course_id}/assignments",
        {
            "per_page": 100,
            "include[]": ["assignment_visibility"],
        },
    )


def download_assignment_comment_attachments(
    client: CanvasClient,
    course_id: str,
    assignment: dict[str, object],
    out_dir: Path,
    extensions: set[str] | None,
    dry_run: bool,
) -> tuple[int, int]:
    assignment_id = assignment.get("id")
    if not assignment_id:
        print(f"SKIP assignment without id: {assignment}", file=sys.stderr)
        return 0, 0

    submissions = client.get_json_pages(
        f"/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions",
        {
            "per_page": 100,
            "include[]": ["submission_comments", "user"],
        },
    )

    found = 0
    downloaded = 0
    assignment_dir = out_dir / assignment_label(assignment)

    for submission in submissions:
        student_dir = assignment_dir / user_label(submission)
        comments = submission.get("submission_comments") or []
        if not isinstance(comments, list):
            continue
        for comment_index, comment in enumerate(comments, start=1):
            if not isinstance(comment, dict):
                continue
            attachments = comment.get("attachments") or []
            if not isinstance(attachments, list):
                continue
            comment_id = safe_name(comment.get("id"), f"comment_{comment_index}")
            for attachment in attachments:
                if not isinstance(attachment, dict):
                    continue
                filename = attachment_name(attachment)
                if extensions and Path(filename).suffix.lower() not in extensions:
                    continue
                url = attachment_download_url(attachment)
                if not url:
                    print(f"SKIP no download URL: {student_dir.name}/{filename}", file=sys.stderr)
                    continue
                found += 1
                destination = unique_destination(student_dir / f"{comment_id}_{filename}")
                print(f"{assignment_dir.name}/{student_dir.name}/{destination.name}")
                if not dry_run:
                    client.download_file(url, destination)
                    downloaded += 1

    return found, downloaded


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download attachments from Canvas assignment submission comments."
    )
    parser.add_argument("--base-url", default="https://pku.instructure.com", help="Canvas base URL")
    parser.add_argument("--course-id", required=True, help="Canvas course id")
    parser.add_argument("--assignment-id", help="Canvas assignment id. Omit to process every assignment in the course")
    parser.add_argument("--token", default=os.environ.get("CANVAS_TOKEN"), help="Canvas access token")
    parser.add_argument("--out-dir", default="canvas_comment_attachments", help="Output directory")
    parser.add_argument("--extension", action="append", help="Only download this extension, e.g. --extension .md")
    parser.add_argument("--dry-run", action="store_true", help="List attachments without downloading")
    args = parser.parse_args()

    if not args.token:
        print("Missing token. Set CANVAS_TOKEN or pass --token.", file=sys.stderr)
        return 2

    extensions = None
    if args.extension:
        extensions = {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in args.extension}

    client = CanvasClient(args.base_url, args.token)
    out_dir = Path(args.out_dir)
    found = 0
    downloaded = 0

    assignments = list_assignments(client, args.course_id, args.assignment_id)
    for assignment_index, assignment in enumerate(assignments, start=1):
        print(f"[{assignment_index}/{len(assignments)}] {assignment_label(assignment)}", file=sys.stderr)
        assignment_found, assignment_downloaded = download_assignment_comment_attachments(
            client=client,
            course_id=args.course_id,
            assignment=assignment,
            out_dir=out_dir,
            extensions=extensions,
            dry_run=args.dry_run,
        )
        found += assignment_found
        downloaded += assignment_downloaded

    if args.dry_run:
        print(f"Found {found} matching comment attachment(s).")
    else:
        print(f"Downloaded {downloaded} comment attachment(s) to {out_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
