
# Barınak Portalı

## Kurulum
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install flask pandas openpyxl
```

## Çalıştırma
```bash
cd shelter_app
export FLASK_APP=app.py
export EXCEL_PATH=./animal_shelter.xlsx  # İsterseniz dışarıdaki Excel yolunu gösterin
python app.py  # veya: flask run
```

Sonra tarayıcıdan `http://localhost:5000`.

## Özellikler
- Herkes için **kayıtsız** gezinti + filtreleme
- **Sahip girişi**: barınak seçimi + şifre (şifre `shelters` sayfasındaki `password` kolonundan okunur)
- Sahibin kendi barınağı için **Hayvan/Çalışan Ekle-Düzenle-Sil**
- Veriler Excel'e **persist** edilir (overwrite).

```

