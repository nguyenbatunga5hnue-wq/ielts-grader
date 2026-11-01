# ielts-grader

Plugin Claude Code gộp 3 skill chấm IELTS và một agent điều phối `ielts-grader`.

| Thành phần | Việc |
|---|---|
| `agents/ielts-grader.md` | Agent: nhận bài (Doc, Sheets, audio), tự chọn skill phù hợp, chấm hàng loạt |
| `skills/ielts-writing-grader` | Writing Task 2: chấm 4 tiêu chí, sửa trên Google Docs ở chế độ đề xuất, ưu tiên theme–rheme |
| `skills/ielts-task1-grader` | Writing Task 1: đọc biểu đồ, chấm TA, key features, diễn đạt linh hoạt |
| `skills/ielts-speaking-analyzer` | Speaking: nghe file ghi âm, đo fluency, chunking, âm vị, chấm FC/LR/GRA/P |

## Cài đặt

Trong Claude Code:

```
/plugin marketplace add <owner>/<repo>
/plugin install ielts-grader@ielts-grader
```

Speaking cần chạy một lần trong mỗi môi trường mới:

```bash
bash skills/ielts-speaking-analyzer/scripts/setup.sh
```

## Dùng

Gọi agent `ielts-grader` (hoặc chỉ cần gửi link bài / bảng điểm / file ghi âm và nhờ chấm), ví dụ:

- "chấm bài này: https://docs.google.com/document/d/…"
- "chấm hết các bài trong bảng điểm: https://docs.google.com/spreadsheets/d/…"
- "nghe và nhận xét bài nói này" + file m4a

Writing cần kết nối Google Docs/Drive/Sheets.
