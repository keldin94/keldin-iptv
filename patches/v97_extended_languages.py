from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/UiLocaleV9.java")
s=p.read_text()
anchor='''    private static void put16(String... items){'''
assert anchor in s
s=s.replace(anchor,'''    private static void putOthers(String english,String... values){
        if(values.length!=12)throw new IllegalArgumentException("12 locale values required");
        String[] primary=TEXT.get(english);
        if(primary==null)return; // Ignore keys not present in this app version.
        String[] full=new String[16];
        full[0]=primary[0];full[1]=primary[1];full[2]=primary[2];full[9]=primary[3];
        int[] positions={3,4,5,6,7,8,10,11,12,13,14,15};
        for(int i=0;i<positions.length;i++)full[positions[i]]=values[i];
        FULL.put(english,full);
    }

    private static void put16(String... items){''',1)
key='''        put("Connection failed","Povezivanje nije uspjelo","Povezava ni uspela","Verbindung fehlgeschlagen");'''
assert key in s,"translation insertion point"
s=s.replace(key,key+'''\n        putOthers("Accent color","Color de acento","Cor de destaque","एक्सेंट रंग","لون التمييز","Couleur d’accent","Warna aksen","Vurgu rengi","アクセントカラー","강조 색상","强调色","Цвет акцента","বিশেষ রঙ");
        putOthers("Text size","Tamaño de texto","Tamanho do texto","पाठ का आकार","حجم النص","Taille du texte","Ukuran teks","Metin boyutu","文字サイズ","글자 크기","文字大小","Размер текста","লেখার আকার");
        putOthers("Panel transparency","Transparencia del panel","Transparência do painel","पैनल पारदर्शिता","شفافية اللوحة","Transparence du panneau","Transparansi panel","Panel saydamlığı","パネルの透明度","패널 투명도","面板透明度","Прозрачность панели","প্যানেলের স্বচ্ছতা");
        putOthers("Playback & startup","Reproducción e inicio","Reprodução e inicialização","प्लेबैक और शुरुआत","التشغيل وبدء التطبيق","Lecture et démarrage","Pemutaran dan mulai","Oynatma ve başlangıç","再生と起動","재생 및 시작","播放与启动","Воспроизведение и запуск","প্লেব্যাক ও শুরু");
        putOthers("Home screen","Pantalla de inicio","Tela inicial","होम स्क्रीन","الشاشة الرئيسية","Écran d’accueil","Layar beranda","Ana ekran","ホーム画面","홈 화면","主屏幕","Главный экран","হোম স্ক্রিন");
        putOthers("Last live channel","Último canal en directo","Último canal ao vivo","अंतिम लाइव चैनल","آخر قناة مباشرة","Dernière chaîne en direct","Saluran langsung terakhir","Son canlı kanal","最後のライブチャンネル","마지막 실시간 채널","上次直播频道","Последний прямой канал","শেষ লাইভ চ্যানেল");
        putOthers("Buffer","Búfer","Buffer","बफ़र","المخزن المؤقت","Mémoire tampon","Buffer","Tampon","バッファ","버퍼","缓冲","Буфер","বাফার");
        putOthers("Automatic reconnect","Reconexión automática","Reconexão automática","स्वचालित पुनः कनेक्ट","إعادة الاتصال تلقائيًا","Reconnexion automatique","Sambung ulang otomatis","Otomatik yeniden bağlan","自動再接続","자동 재연결","自动重连","Автоподключение","স্বয়ংক্রিয় পুনঃসংযোগ");
        putOthers("Remember last channel","Recordar último canal","Lembrar último canal","पिछला चैनल याद रखें","تذكر آخر قناة","Mémoriser la dernière chaîne","Ingat saluran terakhir","Son kanalı hatırla","最後のチャンネルを記憶","마지막 채널 기억","记住上次频道","Запомнить последний канал","শেষ চ্যানেল মনে রাখুন");
        putOthers("Playlists and country filters","Listas y filtros de países","Listas e filtros de países","प्लेलिस्ट और देश फ़िल्टर","القوائم وفلاتر البلدان","Listes et filtres par pays","Daftar dan filter negara","Listeler ve ülke filtreleri","プレイリストと国フィルター","목록 및 국가 필터","播放列表与国家筛选","Плейлисты и фильтры стран","প্লেলিস্ট ও দেশ ফিল্টার");
        putOthers("EPG time offset","Desfase horario EPG","Ajuste de horário EPG","EPG समय समायोजन","فرق توقيت دليل البرامج","Décalage horaire EPG","Pergeseran waktu EPG","EPG zaman kayması","EPG時刻補正","EPG 시간 오프셋","EPG时间偏移","Сдвиг времени EPG","EPG সময় সমন্বয়");
        putOthers("Parental PIN","PIN parental","PIN parental","अभिभावक पिन","رمز الرقابة الأبوية","Code parental","PIN orang tua","Ebeveyn PIN’i","保護者PIN","보호자 PIN","家长PIN","Родительский PIN","অভিভাবক পিন");
        putOthers("Settings backup","Copia de ajustes","Backup das configurações","सेटिंग्स बैकअप","نسخة احتياطية للإعدادات","Sauvegarde des paramètres","Cadangan pengaturan","Ayar yedeği","設定のバックアップ","설정 백업","设置备份","Резервная копия настроек","সেটিংস ব্যাকআপ");
        putOthers("Crash diagnostics","Diagnóstico de fallos","Diagnóstico de falhas","क्रैश निदान","تشخيص الأعطال","Diagnostic des plantages","Diagnostik kerusakan","Çökme tanılama","クラッシュ診断","충돌 진단","崩溃诊断","Диагностика сбоев","ক্র্যাশ নির্ণয়");
        putOthers("Check for updates","Buscar actualizaciones","Verificar atualizações","अपडेट जाँचें","التحقق من التحديثات","Rechercher des mises à jour","Periksa pembaruan","Güncellemeleri denetle","更新を確認","업데이트 확인","检查更新","Проверить обновления","আপডেট পরীক্ষা করুন");
        putOthers("Automatic update checks","Buscar actualizaciones automáticamente","Verificação automática de atualizações","स्वचालित अपडेट जाँच","التحقق التلقائي من التحديثات","Vérification automatique des mises à jour","Cek pembaruan otomatis","Otomatik güncelleme kontrolü","更新の自動確認","자동 업데이트 확인","自动检查更新","Автопроверка обновлений","স্বয়ংক্রিয় আপডেট পরীক্ষা");
        putOthers("Overlay auto-hide","Ocultar menús automáticamente","Ocultar menus automaticamente","मेनू अपने आप छिपाएँ","إخفاء القوائم تلقائيًا","Masquage automatique des menus","Sembunyikan menu otomatis","Menüleri otomatik gizle","メニューを自動で隠す","메뉴 자동 숨김","自动隐藏菜单","Автоскрытие меню","মেনু নিজে থেকে লুকান");
        putOthers("Preferred audio language","Idioma de audio preferido","Idioma de áudio preferido","पसंदीदा ऑडियो भाषा","لغة الصوت المفضلة","Langue audio préférée","Bahasa audio utama","Tercih edilen ses dili","優先音声言語","선호 오디오 언어","首选音频语言","Предпочтительный язык аудио","পছন্দের অডিও ভাষা");
        putOthers("Playlist connection timeout","Tiempo de conexión de lista","Tempo limite da lista","प्लेलिस्ट कनेक्शन समयसीमा","مهلة اتصال القائمة","Délai de connexion de la liste","Batas waktu koneksi daftar","Liste bağlantı zaman aşımı","リスト接続タイムアウト","목록 연결 시간 초과","列表连接超时","Тайм-аут подключения плейлиста","প্লেলিস্ট সংযোগ সময়সীমা");
        putOthers("On","Activado","Ligado","चालू","تشغيل","Activé","Aktif","Açık","オン","켜짐","开启","Включено","চালু");
        putOthers("Off","Desactivado","Desligado","बंद","إيقاف","Désactivé","Nonaktif","Kapalı","オフ","꺼짐","关闭","Выключено","বন্ধ");
        putOthers("Never","Nunca","Nunca","कभी नहीं","أبدًا","Jamais","Tidak pernah","Asla","しない","안 함","从不","Никогда","কখনো না");
        putOthers("Auto","Automático","Automático","स्वचालित","تلقائي","Auto","Otomatis","Otomatik","自動","자동","自动","Авто","স্বয়ংক্রিয়");
        putOthers("Compact","Compacto","Compacto","संक्षिप्त","مدمج","Compact","Ringkas","Kompakt","コンパクト","간결함","紧凑","Компактный","কম্প্যাক্ট");
        putOthers("Standard","Estándar","Padrão","मानक","قياسي","Standard","Standar","Standart","標準","표준","标准","Стандартный","মানক");
        putOthers("Large","Grande","Grande","बड़ा","كبير","Grand","Besar","Büyük","大","큼","大","Крупный","বড়");
        putOthers("Reconnect stream","Reconectar emisión","Reconectar transmissão","स्ट्रीम पुनः जोड़ें","إعادة اتصال البث","Reconnecter le flux","Sambungkan ulang siaran","Yayını yeniden bağla","配信に再接続","스트림 다시 연결","重连直播流","Переподключить поток","স্ট্রিম পুনঃসংযোগ");
        putOthers("Change playback mode","Cambiar modo de reproducción","Mudar modo de reprodução","प्लेबैक मोड बदलें","تغيير وضع التشغيل","Changer de mode de lecture","Ubah mode pemutaran","Oynatma modunu değiştir","再生モードを変更","재생 모드 변경","切换播放模式","Сменить режим воспроизведения","প্লেব্যাক মোড বদলান");
        putOthers("Open in external player","Abrir en reproductor externo","Abrir no player externo","बाहरी प्लेयर में खोलें","فتح بمشغل خارجي","Ouvrir dans un lecteur externe","Buka di pemutar lain","Harici oynatıcıda aç","外部プレイヤーで開く","외부 플레이어에서 열기","使用外部播放器打开","Открыть во внешнем плеере","বাইরের প্লেয়ারে খুলুন");
        putOthers("Error details","Detalles del error","Detalhes do erro","त्रुटि विवरण","تفاصيل الخطأ","Détails de l’erreur","Detail kesalahan","Hata ayrıntıları","エラーの詳細","오류 세부정보","错误详情","Подробности ошибки","ত্রুটির বিবরণ");
        putOthers("Toggle favorite","Añadir o quitar favorito","Alternar favorito","पसंदीदा बदलें","إضافة أو إزالة المفضلة","Ajouter ou retirer des favoris","Ubah favorit","Favoriyi değiştir","お気に入り切替","즐겨찾기 전환","切换收藏","Добавить или убрать избранное","প্রিয় তালিকা বদলান");
        putOthers("Change aspect ratio","Cambiar formato de imagen","Alterar proporção da imagem","चित्र अनुपात बदलें","تغيير نسبة العرض","Changer le format d’image","Ubah rasio gambar","Görüntü oranını değiştir","画面比率を変更","화면 비율 변경","调整画面比例","Изменить соотношение сторон","ছবির অনুপাত বদলান");
        putOthers("Audio tracks","Pistas de audio","Faixas de áudio","ऑडियो ट्रैक","مسارات الصوت","Pistes audio","Trek audio","Ses parçaları","音声トラック","오디오 트랙","音轨","Аудиодорожки","অডিও ট্র্যাক");
        putOthers("Subtitles","Subtítulos","Legendas","उपशीर्षक","ترجمة نصية","Sous-titres","Takarir","Altyazılar","字幕","자막","字幕","Субтитры","সাবটাইটেল");
        putOthers("Pause / Resume","Pausar / Reanudar","Pausar / Retomar","रोकें / जारी रखें","إيقاف مؤقت / متابعة","Pause / Reprendre","Jeda / Lanjutkan","Duraklat / Sürdür","一時停止 / 再開","일시정지 / 계속","暂停 / 继续","Пауза / Продолжить","বিরতি / চালিয়ে যান");
        putOthers("Previous channel","Canal anterior","Canal anterior","पिछला चैनल","القناة السابقة","Chaîne précédente","Saluran sebelumnya","Önceki kanal","前のチャンネル","이전 채널","上一个频道","Предыдущий канал","আগের চ্যানেল");
        putOthers("Next channel","Canal siguiente","Próximo canal","अगला चैनल","القناة التالية","Chaîne suivante","Saluran berikutnya","Sonraki kanal","次のチャンネル","다음 채널","下一个频道","Следующий канал","পরের চ্যানেল");
        putOthers("Options","Opciones","Opções","विकल्प","الخيارات","Options","Opsi","Seçenekler","オプション","옵션","选项","Параметры","বিকল্প");
        putOthers("Connecting...","Conectando...","Conectando...","जुड़ रहा है...","جارٍ الاتصال...","Connexion...","Menghubungkan...","Bağlanıyor...","接続中...","연결 중...","连接中...","Подключение...","সংযোগ হচ্ছে...");
        putOthers("No available tracks.","No hay pistas disponibles.","Nenhuma faixa disponível.","कोई ट्रैक उपलब्ध नहीं।","لا توجد مسارات متاحة.","Aucune piste disponible.","Tidak ada trek tersedia.","Kullanılabilir parça yok.","利用できるトラックはありません。","사용 가능한 트랙 없음.","没有可用轨道。","Нет доступных дорожек.","কোনো ট্র্যাক নেই।");
        putOthers("No errors recorded.","Sin errores registrados.","Sem erros registrados.","कोई त्रुटि दर्ज नहीं।","لم تُسجل أخطاء.","Aucune erreur enregistrée.","Tidak ada kesalahan tercatat.","Kayıtlı hata yok.","エラー記録なし。","기록된 오류 없음.","未记录错误。","Ошибок не зарегистрировано.","কোনো ত্রুটি নেই।");
        putOthers("Connection failed","Falló la conexión","Falha na conexão","कनेक्शन विफल","فشل الاتصال","Échec de connexion","Koneksi gagal","Bağlantı başarısız","接続に失敗しました","연결 실패","连接失败","Ошибка подключения","সংযোগ ব্যর্থ");
        putOthers("Buffer stall recovery","Recuperación de búfer","Recuperação de buffer","बफ़र पुनर्प्राप्ति","استعادة البث بعد التوقف","Récupération du tampon","Pemulihan buffer","Tampon kurtarma","バッファ停止から復旧","버퍼 중단 복구","缓冲故障恢复","Восстановление буфера","বাফার পুনরুদ্ধার");''',1)
p.write_text(s)
print("PASS: 16-language localized labels and playback controls for 43 additional UI terms")
