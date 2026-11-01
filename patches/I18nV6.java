package com.keldin.iptv.ui;

import android.content.Context;
import android.content.SharedPreferences;
import java.util.HashMap;
import java.util.Map;

/** English-first TV UI. Names delivered by IPTV providers are never auto-translated. */
public final class I18n {
    private I18n(){}
    private static final String[] CODES={"en","bs","es","pt","hi","ar","fr","id","de","tr","ja","ko","zh","ru","bn"};
    private static final String[] NAMES={"English","Bosanski","Español","Português","हिन्दी","العربية","Français","Bahasa Indonesia","Deutsch","Türkçe","日本語","한국어","中文","Русский","বাংলা"};
    private static final Map<String,String[]> TABLE=new HashMap<>();
    static {
        put("home","Home","Početna","Inicio","Início","होम","الرئيسية","Accueil","Beranda","Startseite","Ana sayfa","ホーム","홈","首页","Главная","হোম");
        put("live","Live TV","TV uživo","TV en vivo","TV ao vivo","लाइव टीवी","البث المباشر","TV en direct","TV Langsung","Live-TV","Canlı TV","ライブTV","라이브 TV","直播电视","Прямой эфир","লাইভ টিভি");
        put("movies","Movies","Filmovi","Películas","Filmes","फ़िल्में","أفلام","Films","Film","Filme","Filmler","映画","영화","电影","Фильмы","সিনেমা");
        put("series","Series","Serije","Series","Séries","सीरीज़","مسلسلات","Séries","Serial","Serien","Diziler","シリーズ","시리즈","剧集","Сериалы","সিরিজ");
        put("radio","Radio","Radio","Radio","Rádio","रेडियो","راديو","Radio","Radio","Radio","Radyo","ラジオ","라디오","收音机","Радио","রেডিও");
        put("settings","Settings","Postavke","Ajustes","Configurações","सेटिंग्स","الإعدادات","Paramètres","Pengaturan","Einstellungen","Ayarlar","設定","설정","设置","Настройки","সেটিংস");
        put("categories","Categories","Kategorije","Categorías","Categorias","श्रेणियाँ","الفئات","Catégories","Kategori","Kategorien","Kategoriler","カテゴリー","카테고리","分类","Категории","বিভাগ");
        put("all","All","Sve","Todos","Todos","सभी","الكل","Tous","Semua","Alle","Tümü","すべて","전체","全部","Все","সব");
        put("search","Search","Pretraga","Buscar","Pesquisar","खोजें","بحث","Rechercher","Cari","Suche","Ara","検索","검색","搜索","Поиск","খুঁজুন");
        put("guide","TV Guide","TV vodič","Guía TV","Guia TV","टीवी गाइड","دليل البرامج","Guide TV","Panduan TV","Programmführer","TV rehberi","番組表","TV 가이드","电视指南","Телепрограмма","টিভি গাইড");
        put("lists","Playlists","Moje liste","Listas","Listas","प्लेलिस्ट","القوائم","Listes","Daftar putar","Playlists","Listeler","プレイリスト","재생 목록","播放列表","Плейлисты","প্লেলিস্ট");
        put("favorites","Favorites","Favoriti","Favoritos","Favoritos","पसंदीदा","المفضلة","Favoris","Favorit","Favoriten","Favoriler","お気に入り","즐겨찾기","收藏","Избранное","প্রিয়");
        put("continue","Continue watching","Nastavi gledati","Continuar viendo","Continuar assistindo","देखना जारी रखें","متابعة المشاهدة","Continuer","Lanjut menonton","Weiterschauen","İzlemeye devam et","続きを見る","이어보기","继续观看","Продолжить просмотр","দেখা চালিয়ে যান");
        put("add","Add IPTV playlist","Dodaj IPTV listu","Añadir lista IPTV","Adicionar lista IPTV","IPTV सूची जोड़ें","إضافة قائمة IPTV","Ajouter une liste IPTV","Tambah daftar IPTV","IPTV-Liste hinzufügen","IPTV listesi ekle","IPTVリストを追加","IPTV 목록 추가","添加IPTV列表","Добавить IPTV список","আইপিটিভি তালিকা যোগ");
        put("empty","No playlist is active","Nema aktivne liste","No hay lista activa","Nenhuma lista ativa","कोई सक्रिय सूची नहीं","لا توجد قائمة نشطة","Aucune liste active","Tidak ada daftar aktif","Keine aktive Liste","Aktif liste yok","リストがありません","활성 목록 없음","没有活动列表","Нет активного плейлиста","সক্রিয় তালিকা নেই");
        put("choose","Choose what to watch","Odaberi sadržaj","Elige qué ver","Escolha o que ver","देखने के लिए चुनें","اختر ما تشاهده","Choisir un contenu","Pilih tontonan","Inhalt auswählen","İçerik seç","視聴するものを選択","시청할 콘텐츠 선택","选择观看内容","Выберите, что смотреть","কি দেখবেন বেছে নিন");
        put("appearance","Appearance","Izgled","Apariencia","Aparência","दिखावट","المظهر","Apparence","Tampilan","Darstellung","Görünüm","外観","모양","外观","Внешний вид","চেহারা");
        put("language","Language","Jezik","Idioma","Idioma","भाषा","اللغة","Langue","Bahasa","Sprache","Dil","言語","언어","语言","Язык","ভাষা");
        put("exit","Exit the app?","Izaći iz aplikacije?","¿Salir?","Sair?","ऐप बंद करें?","الخروج؟","Quitter ?","Keluar aplikasi?","App beenden?","Uygulamadan çık?","終了しますか？","앱 종료?","退出应用？","Выйти?","অ্যাপ থেকে বের হবেন?");
        put("cancel","Cancel","Odustani","Cancelar","Cancelar","रद्द करें","إلغاء","Annuler","Batal","Abbrechen","İptal","キャンセル","취소","取消","Отмена","বাতিল");
        put("confirm","Confirm","Potvrdi","Confirmar","Confirmar","पुष्टि करें","تأكيد","Confirmer","Konfirmasi","Bestätigen","Onayla","確認","확인","确认","Подтвердить","নিশ্চিত");
        put("play","Play","Pokreni","Reproducir","Reproduzir","चलाएं","تشغيل","Lire","Putar","Abspielen","Oynat","再生","재생","播放","Смотреть","চালু");
        put("startup","Startup","Pokretanje aplikacije","Inicio","Inicialização","स्टार्टअप","بدء التشغيل","Démarrage","Memulai","Startverhalten","Başlatma","起動","시작","启动","Запуск","চালু");
        put("last","Resume last channel","Pokreni posljednji kanal","Último canal","Último canal","अंतिम चैनल","آخر قناة","Dernière chaîne","Saluran terakhir","Letzter Kanal","Son kanal","前回のチャンネル","마지막 채널","上次频道","Последний канал","শেষ চ্যানেল");
        put("stream","Playback","Reprodukcija","Reproducción","Reprodução","प्लेबैक","التشغيل","Lecture","Pemutaran","Wiedergabe","Oynatma","再生","재생","播放","Воспроизведение","প্লেব্যাক");
    }
    private static void put(String key,String... versions){TABLE.put(key,versions);}
    public static String t(Context context,String key){
        SharedPreferences p=context.getApplicationContext().getSharedPreferences("keldin_settings",Context.MODE_PRIVATE);
        String language=p.getString("ui_lang","en");
        int index=0;for(int i=0;i<CODES.length;i++)if(CODES[i].equals(language)){index=i;break;}
        String[] translations=TABLE.get(key);
        return translations==null?key:translations[index];
    }
    public static String[] languageNames(){return NAMES.clone();}
    public static String[] languageCodes(){return CODES.clone();}
    public static int selectedLanguage(Context context){
        String code=context.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE).getString("ui_lang","en");
        for(int i=0;i<CODES.length;i++)if(CODES[i].equals(code))return i;
        return 0;
    }
}
