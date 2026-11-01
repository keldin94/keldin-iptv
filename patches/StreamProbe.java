package com.keldin.iptv.playback;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

/**
 * Short, explicit diagnosis initiated by the viewer.
 * Does not log or display credentials, URLs or response bodies.
 */
public final class StreamProbe {
    private StreamProbe() { }

    public static final class Result {
        public final int statusCode;
        public final String contentType;
        public final String format;
        public final String explanation;

        Result(int code, String mime, String detected, String detail) {
            statusCode = code;
            contentType = mime;
            format = detected;
            explanation = detail;
        }

        public String summary() {
            return "HTTP: " + (statusCode > 0 ? statusCode : "nema odgovora") +
                   "\nContent-Type: " + contentType +
                   "\nPrepoznato: " + format +
                   "\n" + explanation;
        }

        public boolean isHls() { return "HLS playlist".equals(format); }
    }

    public static Result inspect(String rawUrl, String userAgent) {
        HttpURLConnection conn = null;
        try {
            URL url = new URL(rawUrl);
            conn = (HttpURLConnection) url.openConnection();
            conn.setConnectTimeout(10000);
            conn.setReadTimeout(10000);
            conn.setInstanceFollowRedirects(true);
            conn.setRequestProperty("User-Agent", userAgent == null || userAgent.isEmpty() ? "VLC/3.0.21 LibVLC/3.0.21" : userAgent);
            conn.setRequestProperty("Accept", "*/*");
            conn.setRequestProperty("Accept-Encoding", "identity");
            int code = conn.getResponseCode();
            String ct = conn.getContentType();
            if (ct == null || ct.isEmpty()) ct = "(nije naveden)";
            if (code == 401 || code == 403)
                return new Result(code, ct, "odbijen zahtjev", "Server odbija pristup streamu. Provjeri prijavu, aktivne sesije ili ograničenja IPTV usluge.");
            if (code >= 400)
                return new Result(code, ct, "HTTP greška", "Server nije poslao video stream.");
            byte[] bytes = new byte[2048];
            int n = 0;
            try (InputStream in = conn.getInputStream()) {
                while (n < bytes.length) {
                    int read = in.read(bytes, n, bytes.length - n);
                    if (read <= 0) break;
                    n += read;
                    if (n >= 564) break;
                }
            }
            if (n == 0)
                return new Result(code, ct, "prazan odgovor", "Server nije poslao podatke za reprodukciju.");
            String head = new String(bytes, 0, Math.min(n, 200), StandardCharsets.UTF_8).trim();
            String lower = head.toLowerCase(Locale.ROOT);
            if (head.startsWith("#EXTM3U") || head.startsWith("\uFEFF#EXTM3U"))
                return new Result(code, ct, "HLS playlist", "Stream je HLS. U playeru odaberi način HLS.");
            if (n >= 377 && bytes[0] == 0x47 && bytes[188] == 0x47 && bytes[376] == 0x47)
                return new Result(code, ct, "MPEG-TS", "Server isporučuje transport stream. Potreban je MPEG-TS/progressive način.");
            if (n >= 8 && bytes[4] == 'f' && bytes[5] == 't' && bytes[6] == 'y' && bytes[7] == 'p')
                return new Result(code, ct, "MP4", "Server isporučuje MP4 video.");
            if (n >= 3 && bytes[0] == 'F' && bytes[1] == 'L' && bytes[2] == 'V')
                return new Result(code, ct, "FLV", "Server vraća FLV; ovaj format ExoPlayer ne podržava direktno.");
            if (lower.startsWith("<!doctype") || lower.startsWith("<html") || ct.toLowerCase(Locale.ROOT).contains("text/html"))
                return new Result(code, ct, "HTML stranica", "Server vraća web stranicu umjesto TV streama. Player to ne može reprodukovati.");
            if (lower.startsWith("{") || lower.startsWith("["))
                return new Result(code, ct, "JSON/tekst", "Server vjerovatno vraća poruku o grešci umjesto video streama.");
            if (lower.startsWith("#") || ct.toLowerCase(Locale.ROOT).startsWith("text/"))
                return new Result(code, ct, "tekstualni odgovor", "Server ne vraća video u prepoznatom formatu.");
            return new Result(code, ct, "nepoznat binarni format", "Format nije jasno prepoznat. Probaj vanjski VLC player.");
        } catch (IOException | RuntimeException error) {
            return new Result(-1, "(nedostupno)", "mrežna greška", error.getClass().getSimpleName() +
                " – provjeri internet, server i pristup IPTV usluzi.");
        } finally {
            if (conn != null) conn.disconnect();
        }
    }
}
