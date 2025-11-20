"""
Ví dụ sử dụng chatbot API trong Python
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chatbot import StudentSupportChatbot


def example_basic_usage():
    """
    Ví dụ cơ bản: Hỏi 1 câu
    """
    print("=" * 70)
    print("VÍ DỤ 1: SỬ DỤNG CƠ BẢN")
    print("=" * 70)
    
    # Khởi tạo chatbot
    chatbot = StudentSupportChatbot()
    
    # Hỏi câu hỏi
    question = "Điều kiện để được xét tốt nghiệp là gì?"
    response = chatbot.ask(question)
    
    # In kết quả
    print(f"\n❓ Câu hỏi: {question}")
    print(f"\n🤖 Trả lời:\n{response['answer']}")
    
    if response.get('sources'):
        print(f"\n📚 Nguồn tham khảo:")
        for i, source in enumerate(response['sources'], 1):
            print(f"  {i}. {source['source']}")


def example_multiple_questions():
    """
    Ví dụ: Hỏi nhiều câu
    """
    print("\n" + "=" * 70)
    print("VÍ DỤ 2: HỎI NHIỀU CÂU")
    print("=" * 70)
    
    chatbot = StudentSupportChatbot()
    
    questions = [
        "Quy định về điểm danh là gì?",
        "Học phí được tính như thế nào?",
        "Làm thế nào để đăng ký môn học?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n--- Câu hỏi {i} ---")
        response = chatbot.ask(question, include_sources=False)
        print(f"❓ {question}")
        print(f"🤖 {response['answer'][:200]}...")  # Chỉ in 200 ký tự đầu


def example_with_custom_parameters():
    """
    Ví dụ: Sử dụng với tham số tùy chỉnh
    """
    print("\n" + "=" * 70)
    print("VÍ DỤ 3: TÙY CHỈNH PARAMETERS")
    print("=" * 70)
    
    chatbot = StudentSupportChatbot()
    
    question = "Quy trình xin học lại môn học?"
    
    # Tăng số lượng documents để retrieve
    response = chatbot.ask(
        question,
        top_k=10,  # Retrieve 10 documents thay vì 5
        include_sources=True
    )
    
    print(f"\n❓ {question}")
    print(f"\n🤖 {response['answer']}")
    print(f"\n📊 Stats:")
    print(f"  - Số documents tham khảo: {response['num_sources']}")
    print(f"  - Số nguồn unique: {len(response['sources'])}")


def example_batch_processing():
    """
    Ví dụ: Xử lý hàng loạt câu hỏi
    """
    print("\n" + "=" * 70)
    print("VÍ DỤ 4: BATCH PROCESSING")
    print("=" * 70)
    
    chatbot = StudentSupportChatbot()
    
    # Load questions từ file (giả sử)
    questions = [
        "Điều kiện tốt nghiệp?",
        "Quy định học phí?",
        "Cách đăng ký môn học?",
        "Quy trình xin nghỉ học?",
        "Điều kiện học bổng?"
    ]
    
    results = []
    
    print("\n⏳ Đang xử lý batch questions...")
    
    for question in questions:
        response = chatbot.ask(question, include_sources=False)
        results.append({
            'question': question,
            'answer': response['answer']
        })
    
    print(f"\n✅ Đã xử lý {len(results)} câu hỏi")
    
    # Export results
    import json
    output_file = "output_answers.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Kết quả đã được lưu vào {output_file}")


def example_integration_api():
    """
    Ví dụ: Tích hợp vào API endpoint
    """
    print("\n" + "=" * 70)
    print("VÍ DỤ 5: TÍCH HỢP VÀO API")
    print("=" * 70)
    
    print("""
    # Flask API Example
    
    from flask import Flask, request, jsonify
    from src.chatbot import StudentSupportChatbot
    
    app = Flask(__name__)
    chatbot = StudentSupportChatbot()
    
    @app.route('/api/ask', methods=['POST'])
    def ask():
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'Missing question'}), 400
        
        response = chatbot.ask(question)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': response['answer'],
            'sources': response.get('sources', [])
        })
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    
    # Sử dụng:
    # curl -X POST http://localhost:5000/api/ask \\
    #      -H "Content-Type: application/json" \\
    #      -d '{"question": "Điều kiện tốt nghiệp?"}'
    """)


def example_error_handling():
    """
    Ví dụ: Xử lý lỗi
    """
    print("\n" + "=" * 70)
    print("VÍ DỤ 6: XỬ LÝ LỖI")
    print("=" * 70)
    
    try:
        chatbot = StudentSupportChatbot()
        
        # Test với câu hỏi rỗng
        response = chatbot.ask("")
        print(response)
        
        # Test với câu hỏi không liên quan
        response = chatbot.ask("Thời tiết hôm nay thế nào?")
        print(f"\n🤖 {response['answer']}")
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        print("\nCách xử lý:")
        print("1. Kiểm tra API keys")
        print("2. Kiểm tra vectorstore đã tạo chưa")
        print("3. Kiểm tra network connection")


def main():
    """
    Chạy tất cả examples
    """
    print("\n" + "=" * 70)
    print("CHATBOT EXAMPLES - HƯỚNG DẪN SỬ DỤNG")
    print("=" * 70)
    
    try:
        # Uncomment để chạy từng example
        
        example_basic_usage()
        # example_multiple_questions()
        # example_with_custom_parameters()
        # example_batch_processing()
        # example_integration_api()
        # example_error_handling()
        
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy examples: {str(e)}")
        print("\nĐảm bảo bạn đã:")
        print("1. Cài đặt dependencies: pip install -r requirements.txt")
        print("2. Cấu hình .env với API keys")
        print("3. Chạy process_documents.py để tạo vectorstore")


if __name__ == "__main__":
    main()







