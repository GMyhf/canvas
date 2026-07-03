# 批量下载 Canvas 作业评论附件

Canvas 页面上的“下载提交内容”通常只下载学生正式提交的文件，比如图中 `assignmentA.pdf`。评论区里另附的 `assignmentA.md` 属于 submission comment attachment，需要走 Canvas API 单独抓取。

## 1. 准备 Token

Canvas 右上角头像 -> Settings / 设置 -> Approved Integrations / 已批准的集成 -> New Access Token。

不要把 token 写进代码或提交到 git。建议在终端里临时设置：

```bash
export CANVAS_TOKEN='你的 Canvas access token'
```

## 2. 找 course_id 和 assignment_id

打开该作业页面，URL 一般类似：

```text
https://pku.instructure.com/courses/12345/assignments/67890
```

其中 `12345` 是 `course_id`，`67890` 是 `assignment_id`。

## 3. 先预览

整个课程所有作业的评论区 `.md` 附件：

```bash
python3 download_canvas_comment_attachments.py \
  --course-id 1843 \
  --extension .md \
  --dry-run
```

单个作业：

```bash
python3 download_canvas_comment_attachments.py \
  --course-id 12345 \
  --assignment-id 67890 \
  --extension .md \
  --dry-run
```

## 4. 下载评论附件

整个课程所有作业的评论区 `.md` 附件：

```bash
python3 download_canvas_comment_attachments.py \
  --course-id 1843 \
  --extension .md \
  --out-dir course_1843_comment_md
```

单个作业：

```bash
python3 download_canvas_comment_attachments.py \
  --course-id 12345 \
  --assignment-id 67890 \
  --extension .md \
  --out-dir assignmentA_comment_md
```

下载结果会按“作业 / 学生”分目录保存，文件名前缀包含评论 ID，避免同名附件互相覆盖。

如果想下载评论区所有附件，去掉 `--extension .md`。
