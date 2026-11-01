# Đọc số liệu bài nói

Các ngưỡng dưới đây là **tham khảo** cho người học IELTS, rút từ nghiên cứu về fluency của người học L2 và kinh nghiệm chấm. Luôn đối chiếu với cảm nhận tổng thể và Part của bài nói, đừng quy đổi máy móc.

## Fluency

| Chỉ số | Nghĩa | Gợi ý diễn giải |
|---|---|---|
| `speech_rate_wpm` | số từ / tổng thời gian (kể cả ngừng) | <90: chậm, ngắt quãng nhiều (≈ FC 4–5) · 90–120: chậm vừa (≈5–6) · 120–150: ổn (≈6–7) · >150: trôi chảy (≈7+), nếu vẫn rõ ràng |
| `articulation_rate_wpm` | số từ / thời gian thực sự phát âm | cao mà `speech_rate` thấp nghĩa là nói nhanh nhưng ngừng nhiều: vấn đề nằm ở **ngừng tìm ý/từ**, không phải tốc độ miệng |
| `phonation_ratio` | tỉ lệ thời gian có tiếng | <0.65: ngừng quá nhiều · 0.65–0.8: bình thường · >0.8: liền mạch |
| `pauses_per_min` | số lần ngừng ≥0.25s mỗi phút | >20: rất ngắt quãng · 10–20: trung bình · <10: liền mạch |
| `n_long_pauses_1s` | ngừng ≥1s | mỗi lần thường là lúc **bí ý / bí từ**. Xem transcript ngay sau đó để biết con bí gì |
| `mean_length_of_run_words` | trung bình số từ giữa hai lần ngừng | <4: nói từng mẩu (≈FC 4–5) · 4–7: (≈5.5–6.5) · >8: nói thành cụm dài, tự nhiên (≈7+) |
| `pct_pauses_mid_chunk` | % lần ngừng rơi **giữa cụm** | <25%: chunking tốt · 25–45%: cần luyện · >45%: ngắt hơi sai chỗ là thói quen |
| `repetitions` | lặp từ liền nhau ("I I", "the the") | nhiều = đang vừa nói vừa nghĩ, hoặc tự sửa |
| `probable_filled_pauses` + `explicit_fillers` | ừm/à | >6 lần/phút là dày. ASR thường bỏ "uh/um", nên mục `{uh}` là ước lượng |

**Ngừng ở ranh giới** (sau dấu câu, trước and/but/because/which/so…) là bình thường, thậm chí tốt. Ngừng **giữa cụm** (giữa mạo từ và danh từ, giữa động từ và tân ngữ, giữa "I think / that") là dấu hiệu đang dịch trong đầu hoặc bí từ.

Độ dài câu trả lời theo Part:
- Part 1: khoảng 2–4 câu (15–30 giây) mỗi câu hỏi.
- Part 2: nên nói đủ 1.5–2 phút. Dưới 1 phút là thiếu.
- Part 3: khoảng 30–60 giây, có lý do và ví dụ.

## Chunking

Khi viết lại câu cho con tập, ngắt `/` theo **thought groups**:
- Sau cụm chủ ngữ dài: "The main reason I like it / is that…"
- Trước mệnh đề phụ hoặc liên từ: "…every day / because it helps me relax."
- Quanh cụm trạng ngữ: "In my hometown, / people usually…"
- **Không** tách: mạo từ hoặc tính từ khỏi danh từ, giới từ khỏi tân ngữ, trợ động từ khỏi động từ chính, cụm collocation ("make / a decision" là sai).

## Lỗi phát âm điển hình của người Việt (đối chiếu với `recurring_patterns`)

| Máy báo | Lỗi | Mẹo cho học sinh |
|---|---|---|
| `bỏ âm cuối /s/ /z/ /t/ /d/ /k/ /v/…` | nuốt phụ âm cuối (tiếng Việt không bật âm cuối) | phát âm hết âm cuối, nhất là -s số nhiều / ngôi 3 và -ed quá khứ; luyện "bật hơi" nhẹ ở cuối từ |
| `/θ/ → /t/` hoặc `/s/` | "think" → "tink"/"sink" | đặt đầu lưỡi giữa hai hàm răng, thổi hơi |
| `/ð/ → /d/` hoặc `/z/` | "this" → "dis" | như /θ/ nhưng rung dây thanh |
| `/ʃ/ ↔ /s/` | "she" ↔ "see" | /ʃ/ tròn môi, lưỡi lùi về sau |
| `/ʒ/, /dʒ/ → /z/` | "measure", "job" | |
| `/i/ ↔ /ɪ/` | "sheep" ↔ "ship" (dài/ngắn) | /i/ căng môi, kéo dài; /ɪ/ ngắn, thả lỏng |
| `/æ/ → /ɛ/` | "bad" → "bed" | mở miệng rộng hơn, hạ hàm |
| `/aɪ/ /eɪ/ /oʊ/ → nguyên âm đơn` | "like" → "lik", "make" → "mek" | lướt đủ hai thành phần của nguyên âm đôi |
| `/p/ ↔ /b/`, `bỏ /p/` | | /p/ đầu từ cần bật hơi |
| `/ɹ/ → /z/` hoặc bỏ | "rice" → "zice" | cong lưỡi, không chạm vòm |
| `/l/ cuối → bỏ / /n/` | "school" → "schoo" | chạm đầu lưỡi lên lợi ở cuối từ |
| cụm phụ âm bị rút (`bỏ /k/`, `bỏ /t/` trong "texts", "asked") | | tách chậm từng âm rồi nối dần |
| `/v/ → /b/ hoặc /f/`, `/w/ ↔ /v/` | | răng trên chạm môi dưới cho /v/ |

Lỗi ở **từ chức năng** (the, to, and, of…) đọc thành schwa là dạng yếu **tự nhiên**; script đã bỏ qua. Riêng /ð/ → /d/ ở "the/this/that" thì vẫn tính.

## Ngữ điệu (`pitch`)

- `pitch_range_semitones_p10_p90` < 4: giọng đều đều, ít lên xuống (P thường ≤6).
- 4–7: bình thường.
- > 7: linh hoạt. Kiểm tra lại nếu audio có tiếng ồn, vì nhiễu cũng làm số này cao.

Chỉ dùng làm gợi ý kèm chữ "nghe có vẻ".

## Quy đổi band tham khảo cho FC và P (bản rút gọn, chấm chính thức theo `band-descriptors.md`)

**FC**: kết hợp `speech_rate`, `mean_length_of_run`, số ngừng dài, `pct_pauses_mid_chunk`, cùng độ phát triển ý và liên từ trong transcript.
- 5: nói chậm, ngừng nhiều, run ngắn, lặp/tự sửa nhiều, ý ngắn.
- 6: nói được dài nhưng còn ngừng và ừm/à rõ, liên từ đơn giản lặp lại.
- 7: nói dài không quá gắng sức, thỉnh thoảng ngừng tìm từ, dùng được nhiều liên từ/discourse markers.
- 8+: hiếm khi ngừng, ngừng chủ yếu để nghĩ ý chứ không phải tìm từ.

**P**:
- 5: nhiều âm lỗi gây khó hiểu (nhiều `[?]`, `flagged_words` dày).
- 6: hiểu được dù còn lỗi âm lặp lại và nuốt âm cuối; ngữ điệu còn hạn chế.
- 7: lỗi lẻ tẻ, chunking và ngữ điệu khá tự nhiên.
- 8+: rất dễ hiểu, gần như không lỗi âm lặp lại, nhấn nhá linh hoạt.
