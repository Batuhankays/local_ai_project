"""
Arıza Kodu Sistemi Testleri
"""

import pytest
import sys
import os

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fault_code_manager import FaultCodeManager


def test_load_fault_codes():
    """Arıza kodları yükleme testi"""
    manager = FaultCodeManager()
    assert len(manager.fault_codes) > 0
    print(f"✓ {len(manager.fault_codes)} arıza kodu yüklendi")


def test_search_by_code():
    """Kod ile arama testi"""
    manager = FaultCodeManager()
    
    # Var olan kod
    fault = manager.search_by_code("E101")
    assert fault is not None
    assert fault['code'] == 'E101'
    assert fault['name'] == 'Düşük Yağ Basıncı'
    print(f"✓ E101 bulundu: {fault['name']}")
    
    # Olmayan kod
    fault = manager.search_by_code("E999")
    assert fault is None
    print("✓ Olmayan kod testi geçti")


def test_search_by_symptom():
    """Belirti ile arama testi"""
    manager = FaultCodeManager()
    
    # Titreşim belirtisi
    results = manager.search_by_symptom("titreşim")
    assert len(results) > 0
    print(f"✓ 'titreşim' için {len(results)} sonuç bulundu")
    
    # Yağ belirtisi
    results = manager.search_by_symptom("yağ")
    assert len(results) > 0
    print(f"✓ 'yağ' için {len(results)} sonuç bulundu")


def test_search_by_category():
    """Kategori ile arama testi"""
    manager = FaultCodeManager()
    
    results = manager.search_by_category("Elektrik")
    assert len(results) > 0
    print(f"✓ Elektrik kategorisinde {len(results)} arıza bulundu")


def test_get_solution():
    """Çözüm bilgisi alma testi"""
    manager = FaultCodeManager()
    
    solution = manager.get_solution("E101")
    assert solution is not None
    assert 'solutions' in solution
    assert len(solution['solutions']) > 0
    print(f"✓ E101 için {len(solution['solutions'])} çözüm adımı")


def test_get_critical_faults():
    """Kritik arıza kodları testi"""
    manager = FaultCodeManager()
    
    critical = manager.get_critical_faults()
    assert len(critical) > 0
    
    for fault in critical:
        assert fault['severity'] == 'CRITICAL'
    
    print(f"✓ {len(critical)} kritik arıza kodu bulundu")


def test_format_fault_info():
    """Formatlama testi"""
    manager = FaultCodeManager()
    
    fault = manager.search_by_code("E101")
    formatted = manager.format_fault_info(fault)
    
    assert "E101" in formatted
    assert "Düşük Yağ Basıncı" in formatted
    assert "Belirtiler" in formatted
    assert "Çözüm" in formatted
    print("✓ Formatlama testi geçti")


if __name__ == "__main__":
    # Manuel test çalıştırma
    print("=" * 60)
    print("Arıza Kodu Sistemi Testleri")
    print("=" * 60 + "\n")
    
    test_load_fault_codes()
    test_search_by_code()
    test_search_by_symptom()
    test_search_by_category()
    test_get_solution()
    test_get_critical_faults()
    test_format_fault_info()
    
    print("\n" + "=" * 60)
    print("✅ Tüm testler başarılı!")
    print("=" * 60)
