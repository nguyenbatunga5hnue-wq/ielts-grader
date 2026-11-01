# Dấu hiệu văn bản AI trong bài IELTS và cách đọc số đo

## Số đo từ `ai_signals.py`

| Chỉ số | Ý nghĩa | Gợi ý |
|---|---|---|
| `ai_words_per_100w` | mật độ từ LLM hay dùng (delve, pivotal, foster, multifaceted, navigate, tapestry, underscore, holistic…) | ≥1.5: đáng chú ý · ≥3: rất cao. Thử nghiệm: bài kiểu ChatGPT 4.4, bài học sinh thật 0 |
| `ai_phrases` | cụm sáo kiểu AI (in today's fast-paced world, it is important to note, plays a pivotal role, striking a balance, this in turn…) | ≥4 cụm: đáng chú ý. Một số cụm (On the one hand, Moreover) cũng do giáo viên dạy, nên xét tổng thể |
| `sent_len_cv` | độ biến thiên độ dài câu (burstiness) | <0.30: câu đều bất thường (AI) · người viết thật thường 0.4–0.7. Thử nghiệm: AI 0.23, học sinh 0.42–0.44 |
| `para_len_cv` | độ chênh độ dài các đoạn | <0.15 với ≥4 đoạn: đoạn đều như đúc |
| `connectors_per_sentence` | tỉ lệ câu mở bằng Moreover, Furthermore, Additionally, Consequently, Ultimately… | ≥0.4: dày đặc kiểu AI |
| `triads_X_Y_and_Z` | liệt kê bộ ba "A, B, and C" | AI rất hay dùng; nhiều (≥4 trong 250 từ) là đáng chú ý |
| `mattr50`, `mean_zipf`, `pct_rare_words` | độ đa dạng và độ hiếm của từ | **Chỉ có giá trị khi so với baseline** của chính học sinh: tăng vọt là bất thường |
| `non_dictionary_words` | từ không có trong từ điển, tức là lỗi chính tả | Bài có lỗi chính tả kiểu người học thì ít khả năng AI viết nguyên văn. Không có lỗi nào chưa đủ để nghi |
| `typography` | em dash (—), ngoặc cong/thẳng lẫn lộn, ký tự ẩn, markdown | Học sinh gõ trên Docs/Word hiếm khi gõ "—". Markdown `**` hay ký tự ẩn gần như chắc chắn là dán từ chatbot. **Lưu ý:** Google Docs tự đổi ngoặc thẳng sang ngoặc cong khi gõ, nên chỉ đáng chú ý khi **lẫn lộn** cả hai loại |

Ngưỡng là kinh nghiệm, không phải xác suất. Một cờ đơn lẻ không nói lên gì.

## Dấu hiệu đọc bằng mắt

### Ngôn ngữ
- Từ vựng "đẹp" đồng đều từ đầu đến cuối, không có chỗ nào vụng. Người học thật thường có chỗ hay chỗ vụng.
- Collocation chuẩn **tuyệt đối** nhưng lặp các từ kiểu AI (foster, enhance, crucial, significant).
- Câu nào cũng dài 18–25 từ, cấu trúc giống nhau: mệnh đề chính + ", which…" / ", thereby…" / ", leading to…".
- Câu kết đoạn kiểu tổng kết sáo: "This, in turn, …", "Ultimately, …".

### Nội dung và lập luận
- Ví dụ chung chung ("many studies show", "for instance, in many countries"), không có số liệu hay tên cụ thể. Đối lập: học sinh thật hay đưa ví dụ Việt Nam, trải nghiệm cá nhân, hoặc tên cụ thể kiểu Cristiano Ronaldo.
- "Cân bằng giả": luôn nói hai phía rồi kết "striking a balance", kể cả khi đề hỏi quan điểm rõ ràng.
- Đúng cấu trúc bài văn mẫu hoàn hảo: 4 đoạn, mỗi đoạn có topic sentence, 2 ý, kết đoạn.
- Task 1: AI hay viết sai **số liệu** (đọc nhầm biểu đồ, bịa số) hoặc mô tả quá chung không bám số. Đối chiếu với biểu đồ thật như trong skill task 1.

### Hồ sơ lỗi (quan trọng nhất với học sinh Việt)
- Lỗi điển hình của học sinh Việt: thiếu hoặc thừa mạo từ, quên -s/-es, sai thì, sai hoà hợp chủ–vị, sai danh từ đếm được/không đếm được, dịch word-by-word ("make the economy develop"), chính tả.
- **Bài AI viết nguyên văn**: gần như không có lỗi nào.
- **Bài AI sửa từng phần**: câu hoàn hảo chen câu lỗi cơ bản; đoạn mở và kết rất trơn nhưng thân bài còn lỗi; từ vựng C2 ("aforementioned", "exacerbate") đi cùng lỗi A2 ("people is").
- **So với baseline**: bài trước con sai mạo từ 8 lần, bài này 0 lần mà band các tiêu chí khác cũng tăng vọt. Đây là tín hiệu mạnh.

## Những thứ dễ gây nghi oan
- Template và cụm học thuộc từ lớp hoặc từ sách mẫu (Simon, IELTS Liz…).
- Học sinh giỏi thật: band cao đều qua nhiều bài, viết trên lớp cũng tốt.
- Grammarly hoặc công cụ sửa lỗi: hết lỗi chính tả và mạo từ, nhưng giọng văn và ý vẫn của con.
- Bài ngắn (<150 từ): số đo không ổn định.
