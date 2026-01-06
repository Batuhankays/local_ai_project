"""
Arıza Kodu Yönetim Sistemi

Bu modül, jeneratör arıza kodlarını JSON dosyasından yükler,
kod veya belirtilere göre arama yapar ve çözüm önerileri sunar.
"""

import json
import os
from typing import Dict, List, Optional


class FaultCodeManager:
    """Arıza kodu veritabanı yöneticisi"""
    
    def __init__(self, db_path: str = "dokumanlar/ariza_kodlari.json"):
        """
        Args:
            db_path: Arıza kodları JSON dosyasının yolu
        """
        self.db_path = db_path
        self.fault_codes = []
        self.generators = []  # Jeneratör listesi
        self.load_fault_codes()
    
    def load_fault_codes(self) -> None:
        """JSON dosyasından arıza kodlarını yükle"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Arıza kodu veritabanı bulunamadı: {self.db_path}")
        
        with open(self.db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.fault_codes = data.get('fault_codes', [])
            self.generators = data.get('generators', [])
        
        print(f"✓ {len(self.generators)} jeneratör ve {len(self.fault_codes)} arıza kodu yüklendi")
    
    def search_by_code(self, code: str) -> Optional[Dict]:
        """
        Arıza koduna göre arama yap
        
        Args:
            code: Arıza kodu (örn: "E101")
        
        Returns:
            Arıza bilgileri veya None
        """
        code = code.upper().strip()
        for fault in self.fault_codes:
            if fault.get('code') == code:
                return fault
        return None
    
    def search_by_symptom(self, symptom: str) -> List[Dict]:
        """
        Belirtiye göre arama yap
        
        Args:
            symptom: Belirti metni (örn: "titreşim")
        
        Returns:
            İlgili arıza kodları listesi
        """
        symptom = symptom.lower()
        results = []
        
        for fault in self.fault_codes:
            # Belirtilerde ara
            symptoms = [s.lower() for s in fault.get('symptoms', [])]
            if any(symptom in s for s in symptoms):
                results.append(fault)
                continue
            
            # İsim ve kategoride ara
            if symptom in fault.get('name', '').lower():
                results.append(fault)
                continue
            
            if symptom in fault.get('category', '').lower():
                results.append(fault)
        
        return results
    
    def search_by_category(self, category: str) -> List[Dict]:
        """
        Kategoriye göre arama yap
        
        Args:
            category: Kategori adı (örn: "Elektrik Sistemi")
        
        Returns:
            İlgili arıza kodları listesi
        """
        category = category.lower()
        results = []
        
        for fault in self.fault_codes:
            if category in fault.get('category', '').lower():
                results.append(fault)
        
        return results
    
    def get_solution(self, code: str) -> Optional[Dict]:
        """
        Arıza kodu için detaylı çözüm bilgisi al
        
        Args:
            code: Arıza kodu
        
        Returns:
            Çözüm bilgileri (kod, isim, nedenler, çözümler)
        """
        fault = self.search_by_code(code)
        if not fault:
            return None
        
        return {
            'code': fault.get('code'),
            'name': fault.get('name'),
            'severity': fault.get('severity'),
            'category': fault.get('category'),
            'symptoms': fault.get('symptoms', []),
            'causes': fault.get('causes', []),
            'solutions': fault.get('solutions', []),
            'maintenance_interval_hours': fault.get('maintenance_interval_hours'),
            'priority': fault.get('priority')
        }
    
    def get_all_codes(self) -> List[str]:
        """Tüm arıza kodlarını listele"""
        return [fault.get('code') for fault in self.fault_codes]
    
    def get_critical_faults(self) -> List[Dict]:
        """Kritik arıza kodlarını getir"""
        return [
            fault for fault in self.fault_codes 
            if fault.get('severity') == 'CRITICAL'
        ]
    
    def get_generators(self) -> List[Dict]:
        """Tüm jeneratörleri getir"""
        return self.generators
    
    def search_by_generator(self, generator_id: str) -> List[Dict]:
        """
        Belirli bir jeneratöre ait arıza kodlarını getir
        
        Args:
            generator_id: Jeneratör ID'si (örn: "general", "caterpillar_3406")
        
        Returns:
            İlgili arıza kodları listesi
        """
        results = []
        for fault in self.fault_codes:
            gen_ids = fault.get('generator_ids', [])
            if generator_id in gen_ids:
                results.append(fault)
        return results
    
    def get_generator_by_id(self, generator_id: str) -> Optional[Dict]:
        """
        ID'ye göre jeneratör bilgisi getir
        
        Args:
            generator_id: Jeneratör ID'si
        
        Returns:
            Jeneratör bilgisi veya None
        """
        for gen in self.generators:
            if gen.get('id') == generator_id:
                return gen
        return None
    
    def format_fault_info(self, fault: Dict) -> str:
        """
        Arıza bilgisini okunabilir formatta döndür
        
        Args:
            fault: Arıza bilgi sözlüğü
        
        Returns:
            Formatlanmış metin
        """
        if not fault:
            return "Arıza bulunamadı"
        
        output = []
        output.append(f"🔧 Arıza Kodu: {fault.get('code')}")
        output.append(f"📋 İsim: {fault.get('name')}")
        output.append(f"⚠️ Önem: {fault.get('severity')}")
        output.append(f"📁 Kategori: {fault.get('category')}")
        output.append("")
        
        output.append("🔍 Belirtiler:")
        for symptom in fault.get('symptoms', []):
            output.append(f"  • {symptom}")
        output.append("")
        
        output.append("🔎 Olası Nedenler:")
        for cause in fault.get('causes', []):
            output.append(f"  • {cause}")
        output.append("")
        
        output.append("✅ Çözüm Adımları:")
        for solution in fault.get('solutions', []):
            output.append(f"  {solution}")
        output.append("")
        
        if fault.get('maintenance_interval_hours'):
            output.append(f"🕐 Bakım Periyodu: {fault.get('maintenance_interval_hours')} saat")
        
        return "\n".join(output)


if __name__ == "__main__":
    # Test
    manager = FaultCodeManager()
    
    # Kod ile arama testi
    print("=" * 60)
    fault = manager.search_by_code("E101")
    print(manager.format_fault_info(fault))
    
    # Belirti ile arama testi
    print("\n" + "=" * 60)
    print("'titreşim' belirtisi için arama:")
    results = manager.search_by_symptom("titreşim")
    for r in results:
        print(f"  - {r.get('code')}: {r.get('name')}")
