### Truy xuất tài liệu bằng FAISS, vectorstore, langchain và OpenAI
1. Nó sẽ lập chỉ mục các tài liệu pdf của bạn từ thư mục /data và lưu trữ nó trong /faiss_db.
2. Sau đó, bạn có thể truy xuất thông tin từ tài liệu của mình, thông tin này sẽ yêu cầu khóa api OpenAI.
Bạn có thể chạy tệp document_chat.py để truy vấn tài liệu của mình.
3. Bạn có thể thêm tài liệu mới vào index của mình bằng cách đặt các tệp pdf mới vào thư mục /new_document 
và chạy add_document.py.
4. Nếu bạn muốn chạy mọi thứ trên gpu, chỉ cần cài đặt faiss-gpu (sau đó bạn phải gỡ cài đặt faiss-cpu),
và đặt các phần nhúng vào gpu bằng cách xác định nó trong config.yaml