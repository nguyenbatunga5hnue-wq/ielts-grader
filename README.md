# ielts-grader

Một skill duy nhất `ielts-grader` gộp mọi kỹ năng chấm IELTS của thầy.

```
skills/ielts-grader/
├── SKILL.md              # điều phối: chọn quy trình, quy tắc điểm, kiểm tra AI, chấm hàng loạt
├── guides/
│   ├── writing-task2.md  # Task 2: phân loại đề, chấm 4 tiêu chí, sửa trên Google Docs (đề xuất), theme–rheme
│   ├── writing-task1.md  # Task 1: đọc biểu đồ, chấm TA, key features, diễn đạt linh hoạt
│   ├── speaking.md       # Speaking: nghe file ghi âm, fluency, chunking, âm vị, chấm FC/LR/GRA/P
│   └── ai-detector.md    # Nhận diện bài do AI viết/sửa, báo riêng cho thầy
├── references/           # văn phong, band descriptors, mindset Task 2, ngưỡng số liệu
└── scripts/              # setup.sh, analyze_speech.py, ai_signals.py
```

**Cài không cần GitHub:** nén thư mục `skills/ielts-grader` thành zip để tải lên phần Skills của claude.ai, hoặc chép vào `~/.claude/skills/ielts-grader` trên máy.

## Cài đặt

Trong Claude Code:

```
/plugin marketplace add nguyenbatunga5hnue-wq/ielts-grader
/plugin install ielts-grader@ielts-grader
```

Speaking cần chạy một lần trong mỗi môi trường mới:

```bash
bash skills/ielts-grader/scripts/setup.sh
```

## Dùng

Chỉ cần gửi link bài / bảng điểm / file ghi âm và nhờ chấm, ví dụ:

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

## Dùng ở phiên sau

- **Claude Code trên máy tính**: cài plugin một lần bằng 2 lệnh ở trên; các phiên sau tự có.
- **Claude Code trên web (claude.ai/code)**: mở phiên mới với repo này, rồi cài plugin bằng 2 lệnh ở trên (môi trường cloud là tạm thời, mỗi phiên mới cần cài lại). Speaking cần chạy thêm `setup.sh`.
- Cập nhật bản mới: `/plugin marketplace update ielts-grader`.
