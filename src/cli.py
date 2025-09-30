import os
import sys
from dotenv import load_dotenv
from chatbot import TraderAnalysisChatbot

# Load environment variables
load_dotenv()

def show_banner():
    """시작 배너"""
    print("=" * 60)
    print("  TRADER PERFORMANCE ANALYSIS AI CHATBOT")
    print("  트레이더 성과 분석 AI 챗봇")
    print("=" * 60)
    print()

def show_help():
    """도움말 표시"""
    help_text = """
Available Commands:
  exit, quit     - Exit chatbot
  help           - Show this help
  status         - Check system status
  history        - Show conversation history
  clear          - Clear screen
  
Sample Questions:
  - "Top 3 traders by Sharpe ratio"
  - "T001 performance"
  - "Win rate above 90%"
  - "Compare traders"
  
Press Ctrl+C to exit anytime.
"""
    print(help_text)

def show_status(chatbot):
    """시스템 상태"""
    print("\n[SYSTEM STATUS]")
    status = chatbot.mcp.get_status()
    print(f"Data Directory: {status['data_directory']}")
    print(f"Total Files: {status['total_files']}")
    print(f"Traders Loaded: {len(chatbot.kb.traders)}")
    for fname, fstatus in status['files'].items():
        print(f"  - {fname}: {fstatus}")
    print()

def show_history(chatbot):
    """대화 히스토리"""
    history = chatbot.get_history()
    if not history:
        print("\n[No conversation history yet]\n")
        return
    
    print("\n[CONVERSATION HISTORY]")
    for i, item in enumerate(history, 1):
        print(f"\n{i}. Q: {item['query']}")
        print(f"   Intent: {item['intent']}")
        print(f"   A: {item['response'][:100]}...")
    print()

def clear_screen():
    """화면 클리어"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """메인 루프"""
    
    # 챗봇 초기화
    try:
        chatbot = TraderAnalysisChatbot()
    except Exception as e:
        print(f"[ERROR] Failed to initialize chatbot: {e}")
        sys.exit(1)
    
    show_banner()
    
    print("Type 'help' for available commands.\n")
    
    # 메인 루프
    while True:
        try:
            # 사용자 입력
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # 명령어 처리
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye! Thanks for using Trader Analysis Chatbot.\n")
                break
            
            elif user_input.lower() == 'help':
                show_help()
                continue
            
            elif user_input.lower() == 'status':
                show_status(chatbot)
                continue
            
            elif user_input.lower() == 'history':
                show_history(chatbot)
                continue
            
            elif user_input.lower() == 'clear':
                clear_screen()
                show_banner()
                continue
            
            # 질문 처리
            print("\nBot: ", end="", flush=True)
            response = chatbot.process_query(user_input)
            print(response)
            print()
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit properly.\n")
            continue
        
        except Exception as e:
            print(f"\n[ERROR] {e}\n")
            continue

if __name__ == "__main__":
    main()
