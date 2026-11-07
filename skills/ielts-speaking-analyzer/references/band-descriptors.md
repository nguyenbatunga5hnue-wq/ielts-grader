# Tiêu chí chấm IELTS Speaking (tóm tắt tiếng Việt + dấu hiệu nhận biết)

Nguồn: IELTS Speaking Band Descriptors (bản người dùng cung cấp). Phần "Mô tả" là tóm tắt sát nghĩa bản gốc. Phần "Dấu hiệu" là cách skill nhận ra từng mô tả từ số liệu (`analyze_speech.py`) và transcript.

## Nguyên tắc cho điểm

1. Muốn được một band, học sinh phải **đáp ứng ĐỦ các đặc điểm tích cực** của band đó. Thiếu một ý thì xuống band dưới.
2. Điểm là **mức trung bình trên cả bài** (mọi Part). Không chấm theo câu hay nhất hay câu tệ nhất.
3. Bốn tiêu chí ngang nhau, mỗi tiêu chí chỉ cho **số nguyên** (không có .5). Overall = trung bình 4 tiêu chí, làm tròn đến 0.5 gần nhất (.25 → lên .5, .75 → lên band trên).
4. P band 7 = có **tất cả** đặc điểm của band 6 và **một phần** của band 8. P band 5 = tất cả đặc điểm band 4 và một phần band 6. P band 3 tương tự (giữa band 2 và 4).
5. Bài quá ngắn thì không đủ căn cứ cho band cao: band 7+ FC cần "long turns" (Part 2 khoảng 1.5–2 phút, Part 3 trả lời có phát triển).

---

## 1. Fluency and Coherence (FC)

| Band | Mô tả | Dấu hiệu (số liệu và transcript) |
|---|---|---|
| 9 | Trôi chảy, rất hiếm khi lặp hay tự sửa. Ngừng chỉ để chuẩn bị **nội dung**, không phải tìm từ hay ngữ pháp. Liên kết hoàn toàn phù hợp, triển khai chủ đề mạch lạc và đủ dài. | Gần như không có `**/(…)/**` giữa cụm; `repetitions` ≈ 0; run dài (>10 từ) |
| 8 | Trôi chảy, rất hiếm lặp hay tự sửa. **Thỉnh thoảng** ngừng để tìm từ/ngữ pháp, nhưng phần lớn ngừng là vì nội dung. Triển khai mạch lạc, phù hợp, đúng trọng tâm. | ngừng ≥1s hiếm, đa số rơi ở ranh giới ý; `pct_pauses_mid_chunk` <20% |
| 7 | Nói dài **không thấy gắng sức**. Có ngừng, lặp, tự sửa, thường **giữa câu**, do tìm từ, nhưng **không làm mất mạch**. Dùng **linh hoạt** discourse markers và liên từ. | speech rate khoảng ≥120 wpm, MLR ≥7; có ngừng giữa câu nhưng ý vẫn liền; transcript có nhiều loại marker (*actually, to be honest, the thing is, on top of that…*) |
| 6 | **Sẵn lòng** nói dài và giữ được mạch nói. **Đôi khi mất mạch** vì ngừng, lặp, tự sửa. Có nhiều loại marker và liên từ nhưng **không phải lúc nào cũng đúng**. | MLR khoảng 5–7; vài chỗ ngừng dài làm câu bị bỏ dở hoặc đổi hướng; marker dùng gượng hoặc sai |
| 5 | Thường giữ được mạch nói, nhưng **phải dựa vào** lặp, tự sửa và/hoặc nói chậm. Ngừng thường xảy ra **giữa câu để tìm từ/ngữ pháp khá cơ bản**. **Lạm dụng** một số marker. Nói phức tạp thì vấp, nói đơn giản thì trôi. | speech rate <100 wpm hoặc MLR <5; ngừng giữa cụm trước từ đơn giản; "and… and… so…" lặp; câu đơn trôi, câu phức vấp |
| 4 | **Không thể** nói tiếp mà không ngừng rõ rệt. Có thể nói chậm, lặp nhiều, hay tự sửa. Nối được câu đơn nhưng lặp liên từ. Có chỗ **mất mạch**. | pauses_per_min rất cao, MLR <3–4, nhiều ngừng >1s; chỉ có and/but/because |
| 3 | Ngừng thường xuyên, có khi lâu, để tìm từ. Khó nối câu đơn, khó vượt quá câu trả lời đơn giản. Thường không truyền được thông điệp cơ bản. | câu trả lời 1–2 câu ngắn, ngừng rất dài |
| 2 | Ngừng lâu trước gần như mỗi từ. Hầu như không giao tiếp được. | |
| 1 | Không có khả năng nói; hoàn toàn rời rạc. | |

## 2. Lexical Resource (LR)

| Band | Mô tả | Dấu hiệu (transcript) |
|---|---|---|
| 9 | Hoàn toàn linh hoạt và chính xác ở mọi ngữ cảnh. Dùng ngôn ngữ chính xác và idiomatic một cách ổn định. | |
| 8 | Vốn từ rộng, dùng sẵn sàng và linh hoạt cho mọi chủ đề, diễn đạt nghĩa chính xác. Dùng **khéo** từ ít phổ biến và idiomatic, dù thỉnh thoảng sai từ hoặc collocation. Paraphrase hiệu quả khi cần. | idiom và collocation tự nhiên, ít lỗi |
| 7 | Vốn từ linh hoạt cho nhiều chủ đề. **Có một số** từ ít phổ biến và idiomatic, có ý thức về style và collocation, dù còn chỗ chưa phù hợp. Paraphrase hiệu quả. | vài cụm "ăn điểm" (*it's not my cup of tea, keep me on my toes, a breath of fresh air*) dùng đúng chỗ |
| 6 | Đủ từ để bàn chủ đề **một cách dài hơi**. Có thể dùng từ chưa phù hợp nhưng **nghĩa vẫn rõ**. Nhìn chung paraphrase được. | từ an toàn (*good, nice, very, a lot of*) lặp lại; vài collocation sai nhưng hiểu được |
| 5 | Đủ từ cho chủ đề quen và lạ, nhưng **kém linh hoạt**. Có thử paraphrase nhưng không phải lúc nào cũng thành công. | lặp lại từ trong câu hỏi; bí từ ở chủ đề lạ (Part 3) |
| 4 | Đủ từ cho chủ đề quen; chủ đề lạ thì chỉ nói được ý cơ bản. Sai từ thường xuyên. Hiếm khi paraphrase. | |
| 3 | Từ vựng đơn giản, chủ yếu để nói về thông tin cá nhân. Không đủ cho chủ đề lạ. | |
| 2 | Rất hạn chế; chỉ là từ rời hoặc câu học thuộc. | |
| 1 | Chỉ vài từ rời. | |

## 3. Grammatical Range and Accuracy (GRA)

| Band | Mô tả | Dấu hiệu (transcript) |
|---|---|---|
| 9 | Cấu trúc chính xác mọi lúc (trừ kiểu "sai" mà người bản ngữ cũng mắc khi nói). | |
| 8 | Nhiều loại cấu trúc, dùng linh hoạt. **Đa số câu không lỗi**. Thỉnh thoảng có chỗ chưa phù hợp, lỗi không hệ thống. Có thể còn vài lỗi cơ bản. | |
| 7 | Nhiều cấu trúc, dùng linh hoạt. **Câu không lỗi xuất hiện thường xuyên**. Câu đơn và câu phức dùng hiệu quả dù còn lỗi. Vài lỗi cơ bản còn tồn tại. | mệnh đề quan hệ, câu điều kiện, bị động, so sánh… dùng tự nhiên, phần lớn đúng |
| 6 | Kết hợp câu ngắn và câu phức, nhiều cấu trúc nhưng **ít linh hoạt**. Lỗi **thường xảy ra trong câu phức** nhưng **hiếm khi cản trở** giao tiếp. | có câu phức nhưng hay sai thì/hoà hợp |
| 5 | Câu cơ bản kiểm soát khá tốt. Có thử câu phức nhưng ít loại, **gần như luôn có lỗi**, có thể phải nói lại. | |
| 4 | Nói được câu cơ bản, một số câu ngắn không lỗi. Hiếm mệnh đề phụ. Lượt nói ngắn, cấu trúc lặp, lỗi nhiều. | |
| 3 | Thử câu cơ bản nhưng lỗi rất nhiều, trừ câu có vẻ học thuộc. | |
| 2 | Không có câu cơ bản. | |
| 1 | Không có ngôn ngữ chấm được, trừ câu học thuộc. | |

**Lưu ý transcript máy:** máy chép lời có thể tự "sửa" ngữ pháp, ví dụ thêm -s, -ed mà học sinh không phát âm. Nếu `phones` báo **bỏ âm cuối /s/ /z/ /t/ /d/** ở đúng các từ đó, thì đó vừa là lỗi P, vừa có thể là lỗi GRA. Nói rõ là "nghe như thiếu", không khẳng định chắc.

## 4. Pronunciation (P)

| Band | Mô tả | Dấu hiệu (số liệu) |
|---|---|---|
| 9 | Dùng đầy đủ các đặc điểm ngữ âm để diễn đạt nghĩa chính xác, tinh tế. Nối âm (connected speech) linh hoạt, duy trì suốt bài. Hiểu được dễ dàng hoàn toàn. Giọng không ảnh hưởng đến độ dễ hiểu. | |
| 8 | Dùng rộng các đặc điểm ngữ âm. **Duy trì được nhịp** phù hợp. Nhấn và ngữ điệu linh hoạt trên câu dài, thỉnh thoảng hụt. Dễ hiểu suốt bài. Giọng **ảnh hưởng tối thiểu**. | `recurring_patterns` gần như trống; `[?]` rất ít; pitch range >7 |
| 7 | Có **tất cả** đặc điểm band 6 và **một phần** band 8. | chunking tốt (mid-chunk <25%), ít lỗi âm lặp lại, ngữ điệu có lên xuống |
| 6 | Có dùng nhiều đặc điểm ngữ âm, nhưng **kiểm soát chưa đều**. **Chunking nhìn chung phù hợp**, nhưng nhịp có thể bị ảnh hưởng do thiếu stress-timing và/hoặc nói quá nhanh. Có dùng ngữ điệu và trọng âm hiệu quả nhưng **không duy trì**. Từ hoặc âm vị đơn lẻ có thể phát âm sai, nhưng **chỉ thỉnh thoảng** gây khó hiểu. Nhìn chung hiểu được mà **không tốn nhiều công**. | mid-chunk 25–40%; có lỗi âm lặp (nuốt âm cuối) nhưng `[?]` ít; pitch range 4–7 |
| 5 | Có tất cả đặc điểm band 4 và một phần band 6. | |
| 4 | Dùng được một số đặc điểm ngữ âm nhưng hạn chế. **Có chút** chunking chấp nhận được, nhưng **thường xuyên hụt nhịp**. Có thử ngữ điệu và trọng âm nhưng kiểm soát kém. Từ và âm vị **thường xuyên** bị phát âm sai, gây khó hiểu. Người nghe phải **cố gắng**, có đoạn không hiểu được. | mid-chunk >45%; nhiều `flagged_words` và `[?]`; nhiều lỗi âm lặp lại; pitch range <4 |
| 3 | Có một số đặc điểm band 2 và một phần band 4. | |
| 2 | Rất ít đặc điểm ngữ âm chấp nhận được. Vấn đề phát âm làm hỏng nỗ lực nói liền mạch. Từ và âm vị phần lớn sai, ít nghĩa được truyền tải. Thường không hiểu được. | |
| 1 | Chỉ thỉnh thoảng nhận ra từ hoặc âm vị đơn lẻ; không truyền được nghĩa. | |

Các khái niệm trong P cần nói cho học sinh bằng ngôn ngữ đơn giản:
- **Chunking**: ngắt hơi theo cụm ý.
- **Stress-timing**: tiếng Anh nhấn vào từ nội dung và đọc lướt từ chức năng. Tiếng Việt đọc đều từng tiếng, nên nhiều em nói "đều như gõ trống".
- **Connected speech**: nối âm, nuốt âm, đồng hoá ("want to" → "wanna", "an apple" → "a‿napple").
- **Intonation**: lên xuống giọng để thể hiện nghĩa và thái độ.

Skill **chưa đo tự động** stress-timing, trọng âm từ và nối âm. Khi chấm P, nếu không có dấu hiệu rõ thì nhận xét các mục này ở mức "nghe có vẻ…" hoặc bỏ qua. Không bịa.
