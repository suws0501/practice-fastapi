Em Bảo xin phép nộp bài tập tuần 4 ạ.

Những thứ em đã làm:

    - tạo todo_app, pass hết 16 test trong file test.

    - lúc test thì em thấy file test của a xảy ra hiện tượng là nếu k pass test thì 
      row khởi tạo trong DB sẽ ko bị xóa, chạy test lần 2 thì những test dò theo 
      title sẽ bị lỗi. nên em chỉnh lại file test 1 chút, bỏ hết assert vào trong 
      các block try -  finally.

      file test cũ của anh em để là test_fastapi_init.py, còn file em đã sua 
      là test_fastapi.py

    - em dùng module datetime để  khởi tạo tự động cho column created at 
      vs updated at cho bảng trong ORM model thì thấy datetime.utcnow()
      sắp bị deprecated nên em đổi hết thành datetime.now(timezone.utc). 
      em cũng để  datatype trong bảng là TIMESTAMPTZ thay vì TIMESTAMP luôn. 

      vì thế nên em cũng đổi cái REGEX check thời gian của anh 1 chút để  
      qua test ạ :)))) không biết vậy có thể có vấn đề gì, anh có nhận xét 
      gì anh chia sẻ với em nha

    - em dev local xong hết rồi em mới nhớ ra git init rồi git push --force 
      nên bị thiếu uv với docker
      Em sẽ làm đúng trình tự hơn lần sau ạ. em có viết lại CLI để anh test 
      rồi đấy ạ anh đổi const ở trong file .env là được hihi

       