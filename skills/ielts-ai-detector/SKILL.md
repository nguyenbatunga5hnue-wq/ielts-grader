---
name: ielts-ai-detector
description: "Đánh giá khả năng bài IELTS Writing (Task 1 hoặc Task 2) do AI viết hoặc AI sửa nhiều (ChatGPT, Gemini, QuillBot...). Kết hợp số đo văn bản (từ/cụm kiểu AI, độ đều của câu, dấu vết copy-paste), so sánh với bài cũ của chính học sinh, và đọc kỹ của Claude. Kết quả là mức nghi ngờ có bằng chứng, báo riêng cho thầy, kèm cách xác minh. Dùng khi người dùng hỏi bài có phải AI viết không, nghi học sinh dùng ChatGPT, \"check AI\", \"bài này tự viết không\", hoặc khi đang chấm writing thấy bài bất thường."
---

# Nhận diện bài Writing do AI viết

## Nguyên tắc (đọc trước tiên)

1. **Không có công cụ nào phát hiện AI chắc chắn.** Kể cả các detector thương mại vẫn báo sai, và nghiên cứu cho thấy chúng **hay bắt oan người viết không phải bản ngữ**, vì văn của người học thường đơn giản và dễ đoán. Skill này chỉ đưa ra **mức nghi ngờ có bằng chứng**, không bao giờ kết luận "bài này do AI viết".
2. **Kết quả chỉ báo riêng cho thầy trong chat.** Không bao giờ ghi nghi ngờ AI vào Google Doc của học sinh, comment, hay bảng điểm, trừ khi thầy yêu cầu rõ.
3. **Bằng chứng mạnh nhất là so với chính học sinh đó**: bài cũ, lỗi quen thuộc, cách viết trên lớp. Số đo trên một bài đơn lẻ chỉ là gợi ý.
4. **Văn mẫu thầy dạy không phải là AI.** Học sinh IELTS hay học thuộc cụm như "pale in significance", "the aforementioned", "I would argue that". Đây là template học từ lớp, nên chỉ tính là dấu hiệu AI khi đi kèm các dấu hiệu khác.
5. Phân biệt 3 mức sử dụng, vì mỗi mức thầy xử lý khác nhau:
   - **Tự viết**: có thể đã dùng công cụ sửa chính tả (Grammarly).
   - **Tự viết, AI sửa / paraphrase nhiều**: ý và cấu trúc bài là của học sinh, nhưng câu chữ bị "đánh bóng" (QuillBot, "rewrite this").
   - **AI viết phần lớn**: ý, bố cục và câu chữ đều từ AI.

## Quy trình

### 1. Lấy văn bản
- Đọc Google Doc bằng `read_doc`. Chỉ lấy chữ **gốc của học sinh**: bỏ phần đề xuất thầy đã chèn (`suggestedInsertionIds`), bỏ đề bài và khối điểm.
- Lưu mỗi bài ra một file `.txt`.
- **Tìm bài cũ của chính học sinh làm mốc so sánh** (baseline): các tab khác trong doc, hoặc các link khác trong sheet của học sinh đó trên bảng điểm. Bài viết trên lớp hoặc viết tay là baseline tốt nhất.

### 2. Chạy số đo

```bash
pip install -q wordfreq   # lần đầu
python3 <skill>/scripts/ai_signals.py bai.txt --baseline bai_cu1.txt bai_cu2.txt
```

Ý nghĩa các chỉ số và ngưỡng: xem `references/dau-hieu.md`.

### 3. Đọc kỹ (phần quan trọng nhất, máy không làm được)

Đọc bài như một giáo viên IELTS, đối chiếu với bảng dấu hiệu trong `references/dau-hieu.md`. Tập trung vào:
- **Hồ sơ lỗi**: học sinh Việt có lỗi quen (mạo từ, -s, thì, chia động từ, collocation dịch từ tiếng Việt). Bài **không có lỗi nào** mà từ vựng lại rất "sang" là bất thường. Bài có câu cực trơn chen giữa câu lỗi cơ bản là dấu hiệu **sửa từng phần** bằng AI. Ghi lại cụ thể câu nào.
- **So với baseline**: band nhảy vọt (5.5 → 7.5+), lỗi quen biến mất, giọng văn đổi hẳn.
- **Nội dung**: ví dụ chung chung, không có chi tiết cá nhân hay địa phương; lập luận "cân bằng" kiểu nói cho đủ hai phía; câu kết sáo kiểu "striking a balance is crucial".
- **Lạc đề tinh vi**: AI hay trả lời một câu hỏi gần giống đề, ví dụ đề hỏi "to what extent do you agree" mà bài viết kiểu discussion.
- **Dấu vết copy-paste**: em dash (—), ngoặc cong lẫn ngoặc thẳng, ký tự ẩn, markdown (`**`, `#`), font hoặc cỡ chữ khác giữa các đoạn (xem `textStyle` trong JSON của `read_doc`).

### 4. Ước tính tỉ lệ AI (%) và áp ngưỡng của thầy

**Định nghĩa:** tỉ lệ AI = % số chữ nằm trong các câu Claude kết luận là **AI viết hoặc AI viết lại** (không tính câu chỉ được sửa chính tả hay ngữ pháp lẻ tẻ).

Cách tính:
1. Script in ra từng câu kèm nhãn sơ bộ `AI?` và `ước tính máy: X%`. Đây chỉ là điểm xuất phát.
2. Claude **duyệt lại từng câu**:
   - **Bỏ nhãn** nếu marker chỉ là template lớp dạy (Moreover, On the other hand, In conclusion…), hoặc câu có lỗi kiểu người học Việt.
   - **Thêm nhãn** cho câu không có marker nhưng hoàn hảo bất thường so với hồ sơ lỗi hoặc baseline của con, hoặc nằm trong đoạn có dấu vết dán (font khác, em dash, markdown).
   - Đoạn mà phần lớn câu bị gắn nhãn và câu còn lại cùng giọng thì tính cả đoạn.
3. Tỉ lệ = tổng số chữ của các câu có nhãn / tổng số chữ của bài, làm tròn đến 5%.

**Ngưỡng (theo yêu cầu của thầy):**

| Tỉ lệ | Hành động |
|---|---|
| **< 30%** | Chấm bình thường. Nếu 15–29% thì thêm một dòng ghi chú trong báo cáo cho thầy |
| **≥ 30%** | **DỪNG chấm bài này**: không sửa, không comment trong doc, **không điền điểm** vào bảng (để trống ô GV chấm). Báo ngay cho thầy theo mẫu ở bước 6, rồi **chuyển sang học sinh/bài tiếp theo** |

Khi đã kết luận ≥30%, không chấm "một phần" bài đó. Nếu thầy xác minh xong và bảo "chấm tiếp bài của X" thì chấm bình thường.

Thầy có thể đổi ngưỡng (ví dụ "ngưỡng 40%"). Khi đó dùng ngưỡng mới cho cả phiên.

### 5. Kết luận mức nghi ngờ

| Mức | Khi nào |
|---|---|
| **Thấp** | Ít hoặc không có cờ; hồ sơ lỗi giống người học; không lệch nhiều so với baseline |
| **Trung bình** | Có vài dấu hiệu (từ hoặc cụm kiểu AI, câu rất trơn) nhưng có cách giải thích khác (template học thuộc, Grammarly), **hoặc** không có baseline để so |
| **Cao** | Nhiều dấu hiệu **độc lập** cùng chỉ một hướng: số đo + hồ sơ lỗi bất thường + lệch hẳn baseline và/hoặc dấu vết copy-paste |

Không có baseline thì **tối đa là "Trung bình"**, trừ khi có dấu vết copy-paste rõ ràng (markdown, ký tự lạ).

### 6. Báo cho thầy (trong chat)

Mẫu:

```
Bài: <tên học sinh> – <đề>
Tỉ lệ AI ước tính: 45% (máy 50%, Claude duyệt lại) → ≥30%: ĐÃ DỪNG CHẤM, chưa ghi gì vào doc và bảng điểm
Mức nghi ngờ: Trung bình – nghi AI sửa/paraphrase (ý và bố cục có vẻ của con, câu chữ bị "đánh bóng")
Câu/đoạn nghi: body 1 toàn bộ; câu 2 của mở bài ("…")
Căn cứ:
1. <bằng chứng cụ thể, trích câu>
2. ...
Điểm ngược lại (ủng hộ con tự viết): <...>
Gợi ý xác minh: <2–3 cách bên dưới, chọn cái phù hợp>
```

**Cách xác minh** (gợi ý cho thầy, không tự làm):
- **Version history** của Google Doc (File → Version history → See version history): nếu cả bài xuất hiện trong **một lần** chỉnh sửa thì là dán từ nơi khác. Nếu bài lớn dần qua nhiều lần thì là gõ dần. Đây là bằng chứng mạnh nhất. Claude không đọc được lịch sử phiên bản qua kết nối hiện có, nên thầy tự mở.
- **Hỏi lại con**: nhờ con giải thích 2–3 từ hoặc cụm "sang" nhất trong bài (nghĩa, vì sao chọn), hoặc nói lại lập luận body 2 bằng lời của mình.
- **Viết lại trên lớp**: cho viết lại 1 đoạn cùng ý, có giới hạn thời gian, rồi so.

Giọng điệu khi đề xuất: trung lập, không buộc tội. Đây là thông tin để thầy cân nhắc, kèm lời nhắc rằng máy và Claude đều có thể sai.

## Khi đang chấm bài (dùng cùng skill writing)

**Mọi bài writing đều phải qua bước kiểm tra AI TRƯỚC khi chấm**, cả khi chấm lẻ lẫn chấm hàng loạt:

1. Lấy văn bản gốc, chạy `ai_signals.py` (có baseline nếu có), duyệt nhãn từng câu, tính tỉ lệ AI.
2. Nếu < 30%: chấm bình thường theo skill writing. **Không** ghi gì về AI vào doc.
3. Nếu ≥ 30%: dừng bài đó, ghi vào danh sách báo cáo cho thầy, chuyển sang bài tiếp theo.
4. Cuối lượt chấm, báo cáo có một mục riêng **"Bài dừng chấm do nghi AI (≥30%)"**: tên học sinh, bài, tỉ lệ, căn cứ ngắn, gợi ý xác minh.

Không trừ điểm vì nghi ngờ AI. Bài dưới ngưỡng thì chấm như mọi bài khác.
