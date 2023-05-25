## Türkçe Metin Özetleme ve Sınıflandırma

<p align="justify">Bu uygulama, metin özetleme ve sınıflandırma işlemlerini gerçekleştiren bir Flask uygulamasıdır. Metin özetleme işlemi için frekanslama yöntemini kullanılırken, sınıflandırma işlemi için derin öğrenme modeli kullanılmıştır. </p>

### Kurulum
1. Depoyu yerel makinenize klonlayın:
```bash
git clone https://github.com/rumeysaakbas/Turkish_text_summarization.git
```

2. Sanal ortamı etkinleştirin:
```bash
cd text_summarization
venv\Scripts\activate
```

3. Uygulamayı çalıştırın:
```bash
python app.py
```

4. Tarayıcıda görüntüleyin:
```bash
http://localhost:5000
```

<p align="justify">Ana sayfada metin giriş alanı ve iki buton bulunmaktadır. Metin giriş alanına analiz yapmak istediğiniz metni girin.</p>

<p align="justify">"Özetle" butonuna tıklayarak metnin özetini alabilirsiniz. Özet, metindeki önemli cümlelerden oluşacaktır. </p>

<p align="justify">"Sınıflandır" butonuna tıklayarak metnin sınıflandırılmasını yapabilirsiniz. Sınıflandırma sonucu, metnin hangi kategoriye ait olduğunu gösterecektir.</p>

### Kullanılan Teknolojiler

- Python
- Flask
- Frekanslama yöntemi (metin özetleme)
- Derin öğrenme modeli (metin sınıflandırma)




