
# Barınak Portalı

## Kurulum
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install flask pandas openpyxl
```
## Özellikler
- Herkes için **kayıtsız** gezinti + filtreleme
- **Sahip girişi**: barınak seçimi + şifre (şifre `shelters` sayfasındaki `password` kolonundan okunur)
- Sahibin kendi barınağı için **Hayvan/Çalışan Ekle-Düzenle-Sil**
- Veriler Excel'e **persist** edilir (overwrite).


