"""
Mühendislik Asistanı - CLI Arayüzü

Komut satırından asistanı kullanmak için ana script.
"""

import sys
import argparse
from dotenv import load_dotenv
from src.assistant import EngineeringAssistant


def main():
    """Ana CLI fonksiyonu"""
    
    # .env dosyasını yükle
    load_dotenv()
    
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Mühendislik Asistanı - Offline RAG Sistemi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python main.py query "Yağ değişimi nasıl yapılır?"
  python main.py fault E101
  python main.py symptom titreşim
  python main.py interactive
  python main.py critical
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Komut')
    
    # Query komutu
    query_parser = subparsers.add_parser('query', help='Soru sor')
    query_parser.add_argument('question', type=str, help='Soru metni')
    query_parser.add_argument(
        '-k', '--top-k',
        type=int,
        default=3,
        help='Kaç doküman chunk\'ı kullanılacak (varsayılan: 3)'
    )
    
    # Fault komutu
    fault_parser = subparsers.add_parser('fault', help='Arıza kodu analizi')
    fault_parser.add_argument('code', type=str, help='Arıza kodu (örn: E101)')
    
    # Symptom komutu
    symptom_parser = subparsers.add_parser('symptom', help='Belirtiye göre ara')
    symptom_parser.add_argument('symptom', type=str, help='Belirti (örn: titreşim)')
    
    # Critical komutu
    subparsers.add_parser('critical', help='Kritik arıza kodlarını listele')
    
    # Interactive komutu
    subparsers.add_parser('interactive', help='İnteraktif mod')
    
    # Train komutu (train_rag.py'ye yönlendirme)
    subparsers.add_parser('train', help='RAG sistemini eğit (PDF\'leri işle)')
    
    args = parser.parse_args()
    
    # Komut girilmemişse help göster
    if not args.command:
        parser.print_help()
        return
    
    # Train komutu
    if args.command == 'train':
        print("🔄 Training scripti çalıştırılıyor...\n")
        import subprocess
        result = subprocess.run([sys.executable, 'scripts/train_rag.py'])
        sys.exit(result.returncode)
    
    # Asistanı başlat
    try:
        assistant = EngineeringAssistant()
    except Exception as e:
        print(f"❌ Asistan başlatılamadı: {str(e)}")
        return
    
    # Komutları işle
    try:
        if args.command == 'query':
            answer = assistant.query(args.question, top_k=args.top_k)
            print(f"\n🤖 Cevap:\n{answer}\n")
        
        elif args.command == 'fault':
            result = assistant.analyze_fault(args.code)
            print(f"\n{result}\n")
        
        elif args.command == 'symptom':
            result = assistant.search_faults_by_symptom(args.symptom)
            print(f"\n{result}\n")
        
        elif args.command == 'critical':
            result = assistant.get_critical_faults()
            print(f"\n{result}\n")
        
        elif args.command == 'interactive':
            assistant.interactive_mode()
    
    except KeyboardInterrupt:
        print("\n\n👋 Görüşmek üzere!")
    
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
