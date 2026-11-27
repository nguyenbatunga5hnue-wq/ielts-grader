# ielts-grader

Plugin Claude Code gộp 4 skill chấm IELTS và một agent điều phối `ielts-grader`.

| Thành phần | Việc |
|---|---|
| `agents/ielts-grader.md` | Agent: nhận bài (Doc, Sheets, audio), tự chọn skill phù hợp, chấm hàng loạt |
| `skills/ielts-writing-grader` | Writing Task 2: phân loại đề (Multifaceted / Comparative / Extreme), chấm 4 tiêu chí, sửa trên Google Docs ở chế độ đề xuất, ưu tiên tuyến tính (linearity) và theme–rheme |
| `skills/ielts-task1-grader` | Writing Task 1: đọc biểu đồ, chấm TA, key features, diễn đạt linh hoạt |
| `skills/ielts-ai-detector` | Nhận diện bài Writing do AI viết/sửa: số đo + so với bài cũ của học sinh, báo mức nghi ngờ riêng cho thầy |
| `skills/ielts-speaking-analyzer` | Speaking: nghe file ghi âm, đo fluency, chunking, âm vị, chấm FC/LR/GRA/P |

## Cài đặt

Trong Claude Code:

```
/plugin marketplace add nguyenbatunga5hnue-wq/ielts-grader
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
- "bài này có phải AI viết không?" + link doc

Writing cần kết nối Google Docs/Drive/Sheets.

## Quy tắc đang áp dụng

- Xưng **thầy**, gọi học sinh là **con** (dặn "gọi em" thì đổi).
- Sửa trên Google Docs ở **chế độ đề xuất**; không bao giờ tạo comment thử trên bài học sinh.
- **Kiểm tra AI trước khi chấm writing**: tỉ lệ văn AI < 30% thì chấm bình thường; ≥ 30% thì **dừng bài đó** (không sửa, không điền điểm), báo riêng cho thầy rồi chấm người tiếp theo. Đổi ngưỡng: "ngưỡng 40%".
- Điểm từng tiêu chí là **số nguyên** (không có .5); chỉ band tổng mới có .5.
- Speaking: bài dưới ~30 giây chỉ cho điểm ước lượng tạm.
- Writing: lỗi tuyến tính và Theme–Rheme (phương pháp THIỂU, `references/linearity.md`, `references/thematic-progression.md`) quy đổi sang band C&C/TR theo descriptor chính thức trong `references/band-loi-linearity-tp.md` (lỗi → trần điểm, lấy trần thấp nhất). Không áp dụng cho Speaking.

## Dùng ở phiên sau

- **Cách nhanh nhất:** mở phiên Claude Code (máy tính hoặc claude.ai/code) **với repo này**. Skill gộp `ielts-grader` nằm ở `.claude/skills/ielts-grader/` nên được nạp tự động, không cần cài plugin. Đây là cùng bản với skill `ielts-grader` trên claude.ai (Writing Task 1/2 có linearity, theme–rheme, bảng quy đổi lỗi sang band; Speaking; kiểm tra AI; chấm hàng loạt).

- **Claude Code trên máy tính**: cài plugin một lần bằng 2 lệnh ở trên; các phiên sau tự có.
- **Claude Code trên web (claude.ai/code)**: mở phiên mới với repo này, rồi cài plugin bằng 2 lệnh ở trên (môi trường cloud là tạm thời, mỗi phiên mới cần cài lại). Speaking cần chạy thêm `setup.sh`.
- Cập nhật bản mới: `/plugin marketplace update ielts-grader`.
