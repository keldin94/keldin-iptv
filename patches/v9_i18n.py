from pathlib import Path
import re
p=Path("app/src/main/java/com/keldin/iptv/ui/I18n.java")
s=p.read_text()
assert '"en","bs","es"' in s
s=s.replace('"en","bs","es"','"en","bs","sl","es"',1)
s=s.replace('"English","Bosanski","Español"','"English","Bosanski","Slovenščina","Español"',1)
sl_existing={
"home":"Domov","live":"TV v živo","movies":"Filmi","series":"Serije",
"radio":"Radio","settings":"Nastavitve","categories":"Kategorije",
"all":"Vse","search":"Iskanje","guide":"TV-spored",
"lists":"Seznami predvajanja","favorites":"Priljubljene",
"continue":"Nadaljuj ogled","add":"Dodaj IPTV seznam",
"empty":"Ni aktivnega seznama","choose":"Izberi vsebino",
"appearance":"Videz","language":"Jezik","exit":"Želite zapreti aplikacijo?",
"cancel":"Prekliči","confirm":"Potrdi","play":"Predvajaj","startup":"Zagon",
"last":"Nadaljuj zadnji kanal","stream":"Predvajanje"
}
def insert_sl(match):
    line=match.group(0)
    values=re.findall(r'"((?:\\.|[^"\\])*)"',line)
    assert len(values)==16,("existing locale count",len(values),line[:30])
    key=values[0]
    values.insert(3,sl_existing.get(key,values[1]))
    return '        put('+','.join('"'+v+'"' for v in values)+');'
s=re.sub(r'(?m)^        put\(".*"\);$',insert_sl,s)
# The first four core languages are fully translated for all new interactive
# player/EPG surfaces; other existing language packs remain available.
terms={
"video":("Video","Video","Video","Video"),
"audio":("Audio","Zvuk","Zvok","Audio"),
"network":("Network","Mreža","Omrežje","Netzwerk"),
"updates":("Updates","Ažuriranja","Posodobitve","Updates"),
"system":("System","Sistem","Sistem","System"),
"tv_channels":("TV Channels","TV kanali","TV-kanali","TV-Sender"),
"all_categories":("All categories","Sve kategorije","Vse kategorije","Alle Kategorien"),
"other":("Other","Ostalo","Drugo","Sonstige"),
"now":("NOW","U TOKU","TRENUTNO","JETZT"),
"items":("items","stavki","elementov","Einträge"),
"channels_count":("channels","kanala","kanalov","Sender"),
"details":("Details","Detalji","Podrobnosti","Details"),
"select_category":("Select category","Odaberi kategoriju","Izberi kategorijo","Kategorie auswählen"),
"guide_unavailable":("TV guide not available","TV vodič nije dostupan","TV-spored ni na voljo","Kein TV-Programm verfügbar"),
"epg_missing_url":("Add an XMLTV / EPG URL in playlist settings.","Dodaj XMLTV / EPG URL u postavkama liste.","V nastavitvah seznama dodaj XMLTV / EPG URL.","XMLTV-/EPG-URL in den Playlist-Einstellungen hinzufügen."),
"epg_no_programs":("No schedule for this channel. Check EPG source or channel ID.","Nema rasporeda za ovaj kanal. Provjeri EPG izvor ili ID kanala.","Ni sporeda za ta kanal. Preveri EPG vir ali ID kanala.","Kein Programm für diesen Sender. EPG-Quelle oder Sender-ID prüfen."),
"no_description":("No program description available.","Nema dodatnog opisa emisije.","Opis oddaje ni na voljo.","Keine Sendungsbeschreibung verfügbar."),
"close":("Close","Zatvori","Zapri","Schließen"),
"add_favorite":("Add to favorites","Dodaj u favorite","Dodaj med priljubljene","Zu Favoriten hinzufügen"),
"remove_favorite":("Remove favorite","Ukloni iz favorita","Odstrani iz priljubljenih","Aus Favoriten entfernen"),
"next":("Next at","Slijedi u","Naslednje ob","Nächste um"),
"group":("Group","Grupa","Skupina","Gruppe"),
"epg_load_error":("Could not load program guide from provider.","Nije moguće učitati EPG od provajdera.","EPG podatkov ponudnika ni mogoče naložiti.","EPG vom Anbieter konnte nicht geladen werden."),
}
# Additional short translations for other selectable locales in the order
# Spanish, Portuguese, Hindi, Arabic, French, Indonesian, Turkish,
# Japanese, Korean, Chinese, Russian, Bengali.
other={
"video":["Vídeo","Vídeo","वीडियो","الفيديو","Vidéo","Video","Video","動画","비디오","视频","Видео","ভিডিও"],
"audio":["Audio","Áudio","ऑडियो","الصوت","Audio","Audio","Ses","音声","오디오","音频","Аудио","অডিও"],
"network":["Red","Rede","नेटवर्क","الشبكة","Réseau","Jaringan","Ağ","ネットワーク","네트워크","网络","Сеть","নেটওয়ার্ক"],
"updates":["Actualizaciones","Atualizações","अपडेट","التحديثات","Mises à jour","Pembaruan","Güncellemeler","更新","업데이트","更新","Обновления","আপডেট"],
"system":["Sistema","Sistema","सिस्टम","النظام","Système","Sistem","Sistem","システム","시스템","系统","Система","সিস্টেম"],
"tv_channels":["Canales de TV","Canais TV","टीवी चैनल","قنوات التلفزيون","Chaînes TV","Saluran TV","TV Kanalları","TVチャンネル","TV 채널","电视频道","Телеканалы","টিভি চ্যানেল"],
"all_categories":["Todas las categorías","Todas as categorias","सभी श्रेणियाँ","جميع الفئات","Toutes les catégories","Semua kategori","Tüm kategoriler","すべてのカテゴリー","전체 카테고리","所有分类","Все категории","সব বিভাগ"],
"other":["Otros","Outros","अन्य","أخرى","Autres","Lainnya","Diğer","その他","기타","其他","Другое","অন্যান্য"],
"now":["AHORA","AGORA","अभी","الآن","EN COURS","SEKARANG","ŞİMDİ","現在","현재","正在播放","СЕЙЧАС","এখন"],
"items":["elementos","itens","आइटम","عناصر","éléments","item","öğe","項目","항목","项","элементов","আইটেম"],
"channels_count":["canales","canais","चैनल","قنوات","chaînes","saluran","kanal","チャンネル","채널","频道","каналов","চ্যানেল"],
"details":["Detalles","Detalhes","विवरण","التفاصيل","Détails","Detail","Ayrıntılar","詳細","세부정보","详情","Подробности","বিস্তারিত"],
"select_category":["Elegir categoría","Selecionar categoria","श्रेणी चुनें","اختر الفئة","Choisir catégorie","Pilih kategori","Kategori seç","カテゴリーを選択","카테고리 선택","选择分类","Выберите категорию","বিভাগ নির্বাচন"],
"guide_unavailable":["Guía TV no disponible","Guia TV indisponível","टीवी गाइड उपलब्ध नहीं","دليل البرامج غير متاح","Guide TV indisponible","Panduan TV tidak tersedia","TV rehberi yok","番組表を利用できません","TV 가이드 없음","电视节目表不可用","Телепрограмма недоступна","টিভি গাইড নেই"],
"close":["Cerrar","Fechar","बंद करें","إغلاق","Fermer","Tutup","Kapat","閉じる","닫기","关闭","Закрыть","বন্ধ"],
"add_favorite":["Añadir a favoritos","Adicionar aos favoritos","पसंदीदा में जोड़ें","أضف للمفضلة","Ajouter aux favoris","Tambah ke favorit","Favorilere ekle","お気に入りに追加","즐겨찾기에 추가","加入收藏","В избранное","পছন্দে যোগ করুন"],
"remove_favorite":["Quitar de favoritos","Remover dos favoritos","पसंदीदा से हटाएँ","إزالة من المفضلة","Retirer des favoris","Hapus dari favorit","Favorilerden çıkar","お気に入りから削除","즐겨찾기 해제","取消收藏","Убрать из избранного","পছন্দ থেকে সরান"],
"group":["Grupo","Grupo","समूह","المجموعة","Groupe","Grup","Grup","グループ","그룹","分组","Группа","গ্রুপ"],
}
# Reuse fully translated guide message for the primary four languages.
# For remaining languages prefer a neutral English explanation rather than
# pretending provider-specific error text has been localized.
original_order=["en","bs","sl","es","pt","hi","ar","fr","id","de","tr","ja","ko","zh","ru","bn"]
other_codes=["es","pt","hi","ar","fr","id","tr","ja","ko","zh","ru","bn"]
lines=[]
for key,(en,bs,sl,de) in terms.items():
    values={"en":en,"bs":bs,"sl":sl,"de":de}
    for code,value in zip(other_codes,other.get(key,[])):
        values[code]=value
    entries=[values.get(code,en) for code in original_order]
    assert all('"' not in entry and '\n' not in entry for entry in entries)
    lines.append('        put("'+key+'",'+','.join('"'+v+'"' for v in entries)+');')
anchor='''    }
    private static void put(String key,String... versions)'''
assert anchor in s
s=s.replace(anchor,'\n'.join(lines)+'\n'+anchor,1)
p.write_text(s)
print("v0.9: Slovenian added as 16th selectable language; translated core TV controls and EPG")
