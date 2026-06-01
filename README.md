# Data Compression

## Giới thiệu

Dự án **Data Compression** được xây dựng nhằm nghiên cứu và triển khai các thuật toán nén dữ liệu cơ bản. Mục tiêu của dự án là giúp người học hiểu rõ nguyên lý hoạt động của các phương pháp nén dữ liệu, quy trình mã hóa/giải mã và đánh giá hiệu quả của từng thuật toán.

Nén dữ liệu là kỹ thuật giảm kích thước dữ liệu để tiết kiệm không gian lưu trữ và băng thông truyền tải, đồng thời vẫn đảm bảo khả năng khôi phục dữ liệu gốc (đối với nén không mất dữ liệu).

## Mục tiêu

* Tìm hiểu nguyên lý của các thuật toán nén dữ liệu.
* Triển khai thuật toán bằng ngôn ngữ lập trình.
* Đánh giá hiệu quả nén thông qua tỷ lệ nén và tốc độ xử lý.
* So sánh ưu, nhược điểm của từng phương pháp.

## Các thuật toán được sử dụng

Dự án có thể bao gồm một hoặc nhiều thuật toán sau:

* Huffman Coding
* Run-Length Encoding (RLE)
* LZW (Lempel-Ziv-Welch)
* Arithmetic Coding
* Các phương pháp mã hóa entropy khác


## Cài đặt

Sao chép dự án về máy:

```bash
git clone https://github.com/tlinh5488/Data-compression.git
cd Data-compression
```

Biên dịch và chạy chương trình:


### Đối với Python

```bash
python main.py
```

## Ví dụ

Dữ liệu đầu vào:

```text
AAAAABBBBCCCCDDDD
```

Sau khi nén bằng RLE:

```text
A5B4C4D4
```

Kết quả:

```text
Kích thước ban đầu: 16 byte
Kích thước sau nén: 8 byte
Tỷ lệ nén: 50%
```

## Giao diện hệ thống
<img width="1920" height="1080" alt="43f0facd-ed7e-495a-8f32-391276b920e1" src="https://github.com/user-attachments/assets/f3211732-2c22-4d0d-b70b-6c1fa13a8737" />


## Tiêu chí đánh giá

Dự án đánh giá hiệu quả thuật toán dựa trên:

* Tỷ lệ nén (Compression Ratio)
* Tốc độ nén
* Tốc độ giải nén
* Mức sử dụng bộ nhớ
* Khả năng khôi phục dữ liệu

## Ứng dụng thực tế

Nén dữ liệu được ứng dụng rộng rãi trong:

* Lưu trữ tập tin
* Truyền dữ liệu qua mạng
* Hệ thống cơ sở dữ liệu
* Dịch vụ điện toán đám mây
* Định dạng hình ảnh, âm thanh và video
* Hệ thống nhúng và IoT

## Hướng phát triển

* Bổ sung thêm nhiều thuật toán nén khác.
* Xây dựng giao diện người dùng trực quan.
* Hỗ trợ nén dữ liệu nhị phân.
* Thực hiện đánh giá hiệu năng trên tập dữ liệu lớn.
* Trực quan hóa quá trình nén và giải nén.


## Tác giả: Tlinh5488

GitHub: https://github.com/tlinh5488/Data-compression

## Giấy phép

Dự án được phát triển phục vụ mục đích học tập và nghiên cứu.
