# CsvToSql Kurulum Rehberi

Bu proje, Python dilinde yazılmıştır ve çalışmak için iki temel harici kütüphaneye ihtiyaç duyar: `PyQt6` (arayüz için) ve `mysql-connector-python` (veritabanı bağlantısı için).

Aşağıdaki adımları izleyerek projeyi çalıştırmak için gerekli ortamı kurabilirsiniz.

!!! warning "Önemli: Sanal Ortam (Virtual Environment) Kullanın"
    Proje bağımlılıklarını bilgisayarınızdaki diğer Python projelerinden ayırmak için bir sanal ortam (`venv`) kullanmanız şiddetle tavsiye edilir.

    **Sanal ortam oluşturma (Mac/Linux):**
    ```bash
    # Proje klasörünüzün içindeyken
    python3 -m venv venv
    ```

    **Sanal ortamı aktive etme (Mac/Linux):**
    ```bash
    source venv/bin/activate
    ```
    
    **(Windows için aktive etme:** `.\venv\Scripts\activate` **)**

---

## Gerekli Kütüphanelerin Yüklenmesi

İki yöntemden birini seçebilirsiniz. **Önerilen yöntem (requirements.txt)**, projenin yönetimi için daha temiz bir yoldur.

### Yöntem 1: Hızlı Kurulum (Doğrudan PIP ile)

Sanal ortamınızı aktive ettikten sonra, kütüphaneleri `pip` kullanarak doğrudan yükleyebilirsiniz:

```bash
pip install PyQt6 mysql-connector-python