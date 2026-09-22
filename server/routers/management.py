"""项目管理路由"""
import datetime
import json
import os
import re
import yaml
from fastapi import APIRouter, HTTPException
from server.config import MANAGEMENT_DIR, DOCS_FOLDER_ORDER
from server.utils.file_utils import read_file, safe_resolve, scan_directory
from server.parsers.team_parser import parse_team_list, parse_member_profile
from server.parsers.report_parser import get_report_list, get_report_detail
from server.parsers.tasks_parser import parse_tasks
from server.parsers.milestones_parser import parse_milestones
from server.parsers.projects_parser import (
    list_projects, get_project, get_project_tasks, get_task_note,
)

router = APIRouter(prefix="/api/management", tags=["management"])

# 日期/作者参数校验（防止路径遍历与非法文件名）
_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
_YEAR_RE = re.compile(r'^\d{4}$')
_MONTH_RE = re.compile(r'^(0[1-9]|1[0-2])$')
_DAY_RE = re.compile(r'^(0[1-9]|[12]\d|3[01])$')
_WEEK_RE = re.compile(r'^[1-5]?\d$')
_FILENAME_PART_RE = re.compile(r'^[^/\\\x00-\x1f\x7f]+$')


def _safe_report_path(base_dir, *parts):
    """安全拼接报告路径，确保位于 base_dir 内。"""
    filepath = safe_resolve(base_dir, *parts)
    if not filepath or not os.path.exists(filepath):
        return None
    return filepath


@router.get("/team")
async def get_team():
    """获取团队成员列表"""
    readme = read_file(os.path.join(MANAGEMENT_DIR, 'team', 'README.md'))
    return parse_team_list(readme)


@router.get("/team/{member_id}")
async def get_team_member(member_id: str):
    """获取成员档案详情"""
    team_dir = os.path.join(MANAGEMENT_DIR, 'team')
    # 遍历 .md 文件，找到英文标识匹配的成员
    for f in os.listdir(team_dir):
        if f.endswith('.md') and f != 'README.md':
            content = read_file(os.path.join(team_dir, f))
            if content:
                profile = parse_member_profile(content)
                if profile and profile['id'] == member_id:
                    return profile
    return {"detail": "Member not found"}, 404


@router.get("/daily")
async def get_daily_list():
    """获取日报列表"""
    return get_report_list('daily')


@router.get("/daily/{date}/{author}")
async def get_daily_detail(date: str, author: str):
    """获取指定日报内容"""
    # 从 date 解析年月日
    parts = date.split('-')
    if len(parts) != 3:
        raise HTTPException(status_code=400, detail="Invalid date")
    year, month, day = parts
    if not (_YEAR_RE.match(year) and _MONTH_RE.match(month) and _DAY_RE.match(day)):
        raise HTTPException(status_code=400, detail="Invalid date")
    if not _FILENAME_PART_RE.match(author):
        raise HTTPException(status_code=400, detail="Invalid author")

    # 尝试 YYYY/MM/DD-姓名.md
    filepath = _safe_report_path(
        os.path.join(MANAGEMENT_DIR, 'daily', year, month),
        f"{day}-{author}.md",
    )
    if filepath:
        result = get_report_detail(filepath)
        if result:
            result['title'] = f"日报 — {author} — {date}"
            result['author'] = author
            result['date'] = date
            return result
    raise HTTPException(status_code=404, detail="Report not found")


@router.get("/weekly")
async def get_weekly_list():
    """获取周报列表"""
    return get_report_list('weekly')


@router.get("/weekly/{year}/{week}/{author}")
async def get_weekly_detail(year: str, week: str, author: str):
    """获取指定周报内容"""
    if not (_YEAR_RE.match(year) and _WEEK_RE.match(week) and _FILENAME_PART_RE.match(author)):
        raise HTTPException(status_code=400, detail="Invalid parameters")

    filepath = _safe_report_path(
        os.path.join(MANAGEMENT_DIR, 'weekly', year),
        f"W{week}-{author}.md",
    )
    if filepath:
        result = get_report_detail(filepath)
        if result:
            result['title'] = f"周报 — {author} — {year} 第 {week} 周"
            result['author'] = author
            result['year'] = year
            result['week'] = week
            return result
    raise HTTPException(status_code=404, detail="Report not found")


@router.get("/monthly")
async def get_monthly_list():
    """获取月报列表"""
    return get_report_list('monthly')


@router.get("/monthly/{year}/{month}/{author}")
async def get_monthly_detail(year: str, month: str, author: str):
    """获取指定月报内容"""
    if not (_YEAR_RE.match(year) and _MONTH_RE.match(month) and _FILENAME_PART_RE.match(author)):
        raise HTTPException(status_code=400, detail="Invalid parameters")

    filepath = _safe_report_path(
        os.path.join(MANAGEMENT_DIR, 'monthly', year),
        f"{month}-{author}.md",
    )
    if filepath:
        result = get_report_detail(filepath)
        if result:
            result['title'] = f"月报 — {author} — {year} 年 {month} 月"
            result['author'] = author
            result['year'] = year
            result['month'] = month
            return result
    raise HTTPException(status_code=404, detail="Report not found")


@router.get("/tasks")
async def get_tasks(slug: str = None):
    """获取任务看板数据（从 per-project tasks.json 派生，按项目切换）。

    slug 缺省时取首个项目。返回 {in_progress, pending, completed} 三桶。
    """
    return parse_tasks(slug)


@router.get("/milestones")
async def get_milestones():
    """获取里程碑列表"""
    return parse_milestones()


@router.get("/meetings")
async def get_meetings():
    """获取会议纪要列表"""
    meetings_dir = os.path.join(MANAGEMENT_DIR, 'meetings')
    files = scan_directory(meetings_dir, pattern=r'.*\.md$')
    files = [f for f in files if 'template' not in os.path.basename(f).lower()]

    meetings = []
    for f in files:
        content = read_file(f)
        if content:
            import re
            # 提取日期
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(f))
            date = date_match.group(1) if date_match else os.path.basename(f)

            # 从内容中提取参会人和记录人
            participants = ''
            recorder = ''
            for line in content.split('\n'):
                if '参会人' in line:
                    participants = line.split('：')[-1].strip() if '：' in line else ''
                if '记录人' in line:
                    recorder = line.split('：')[-1].strip() if '：' in line else ''

            meetings.append({
                'date': date,
                'participants': participants,
                'recorder': recorder,
            })
    return meetings


@router.get("/meetings/{date}")
async def get_meeting_detail(date: str):
    """获取指定会议纪要内容"""
    if not _DATE_RE.match(date):
        raise HTTPException(status_code=400, detail="Invalid date")

    meetings_dir = os.path.join(MANAGEMENT_DIR, 'meetings')
    filepath = _safe_report_path(meetings_dir, f"{date}.md")
    if filepath:
        content = read_file(filepath)
        if content:
            return {'date': date, 'content': content}
    raise HTTPException(status_code=404, detail="Meeting not found")


# ========== 文档 (wiki) ==========

_DOCS_DIR = os.path.join(MANAGEMENT_DIR, 'docs')
# slug 允许 Unicode 单词字符（含中文）、空格、下划线、连字符与斜杠；
# 路径穿越由 _valid_doc_slug 显式拒绝 + safe_resolve 根目录约束双重防护。
_SLUG_RE = re.compile(r'^[\w][\w \-/]*$', re.UNICODE)


def _valid_doc_slug(slug: str) -> bool:
    """校验文档 slug：允许中文等 Unicode 字符，拒绝空与 .. 路径段。"""
    if not slug or not _SLUG_RE.match(slug):
        return False
    return '..' not in slug.split('/')


def _parse_frontmatter(content):
    """从 markdown 内容中解析 YAML frontmatter，返回 (meta_dict, body_str)。"""
    if not content or not content.startswith('---'):
        return {}, content or ''
    end = content.find('---', 3)
    if end < 0:
        return {}, content
    try:
        meta = yaml.safe_load(content[3:end]) or {}
    except yaml.YAMLError:
        meta = {}
    body = content[end + 3:].strip()
    return meta, body


def _normalize_date(value):
    """frontmatter 的 date 归一为字符串。

    YAML 会把无引号的 `date: 2026-07-16` 解析成 datetime.date，与缺省值 ''
    混在一起排序会抛 TypeError，故统一转 ISO 字符串。
    """
    if value is None:
        return ''
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    return str(value)


@router.get("/docs")
async def get_docs():
    """获取文档列表（management/docs/ 递归扫描所有 .md 文件，跳过 _assets 等下划线资产目录）"""
    if not os.path.isdir(_DOCS_DIR):
        return []
    docs = []
    for root, dirs, files in os.walk(_DOCS_DIR):
        # 下划线前缀目录（如 _assets/）存放资产，不是文档
        dirs[:] = [d for d in dirs if not d.startswith('_')]
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            filepath = os.path.join(root, f)
            content = read_file(filepath)
            meta, _ = _parse_frontmatter(content)
            rel = os.path.relpath(filepath, _DOCS_DIR)
            slug = rel[:-3].replace(os.sep, '/')
            docs.append({
                'slug': slug,
                'title': meta.get('title', slug),
                'author': meta.get('author', ''),
                'date': _normalize_date(meta.get('date')),
                'tags': meta.get('tags', []),
                'summary': meta.get('summary', ''),
                'id': meta.get('id'),
                'order': meta.get('order'),
            })
    docs.sort(key=_doc_sort_key)
    return docs


def _doc_number(value):
    """数字字段（order / id）转 float；缺失或非数字统一为 inf（排最后）。"""
    if value is None or isinstance(value, bool):
        return float('inf')
    try:
        return float(value)
    except (TypeError, ValueError):
        return float('inf')


def _doc_date_ordinal(value):
    """ISO 日期转 ordinal；缺失或非法返回 0，用于降序排序。"""
    if not value:
        return 0
    try:
        return datetime.date.fromisoformat(str(value)[:10]).toordinal()
    except ValueError:
        return 0


def _doc_sort_key(doc):
    """排序链：文件夹优先级 → order → id → date 降序 → slug 字典序。

    最后一级 slug 是必需的：前几级全部相同时若不确定，列表顺序会落到
    文件系统遍历顺序（APFS 无序），表现为刷新一次一个样。
    """
    slug = doc.get('slug') or ''
    top = slug.split('/')[0] if '/' in slug else ''
    folder_rank = DOCS_FOLDER_ORDER.index(top) if top in DOCS_FOLDER_ORDER else len(DOCS_FOLDER_ORDER)
    return (
        folder_rank,
        _doc_number(doc.get('order')),
        _doc_number(doc.get('id')),
        -_doc_date_ordinal(doc.get('date')),
        slug,
    )


@router.get("/docs/{slug:path}")
async def get_doc_detail(slug: str):
    """获取指定文档详情（支持子目录路径与中文文件名）"""
    if not _valid_doc_slug(slug):
        raise HTTPException(status_code=400, detail="Invalid slug")
    filepath = safe_resolve(_DOCS_DIR, f"{slug}.md")
    if not filepath or not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="Doc not found")
    content = read_file(filepath)
    meta, body = _parse_frontmatter(content)
    # 同名 sidecar json（可选）：承载 changelog / progress / appendix / related
    sidecar = {}
    sidecar_path = safe_resolve(_DOCS_DIR, f"{slug}.json")
    if sidecar_path and os.path.isfile(sidecar_path):
        try:
            sidecar = json.loads(read_file(sidecar_path) or '{}')
        except (json.JSONDecodeError, ValueError):
            sidecar = {}
    return {
        'slug': slug,
        'title': meta.get('title', slug),
        'author': meta.get('author', ''),
        'date': _normalize_date(meta.get('date')),
        'tags': meta.get('tags', []),
        'summary': meta.get('summary', ''),
        'id': meta.get('id'),
        'content': body,
        'sidecar': sidecar,
    }


# ========== 项目树 ==========

@router.get("/projects")
async def get_projects():
    """获取所有项目列表"""
    return list_projects()


@router.get("/projects/{slug}")
async def get_project_detail(slug: str):
    """获取项目 README 元信息 + 正文"""
    project = get_project(slug)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/projects/{slug}/tasks")
async def get_project_tasks_route(slug: str):
    """获取项目任务树"""
    tree = get_project_tasks(slug)
    if tree is None:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tree


@router.get("/projects/{slug}/notes/{note_path:path}")
async def get_task_note_route(slug: str, note_path: str):
    """获取任务笔记 markdown"""
    content = get_task_note(slug, note_path)
    if content is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {'content': content}
