package com.keldin.iptv.data;

import java.text.Normalizer;
import java.util.Locale;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.regex.Pattern;

/** Non-credential, local-only media classification: conservative explicit title/group filter. */
public final class ContentFilterV93 {
    private static final Pattern ADULT=Pattern.compile(
        "(?:^|[^\\p{L}\\p{N}])(?:18\\+|18 plus|21\\+|xxx|x{3,}|adult|adults|erotic|erotica|erotik|erotika|erotski|erotska|eroticni|eroticna|erotični|erotična|porno|porn|pornography|pornografski|pornografska|softcore|hardcore|seks|sexual|sex|nudity|nude|onlyfans|nsfw|for adults|odrasli|odrasle|za odrasle|erwachsene)(?:$|[^\\p{L}\\p{N}])",
        Pattern.CASE_INSENSITIVE|Pattern.UNICODE_CASE);
    private ContentFilterV93() {}
    /** Stable opaque identifier: hidden media keys never store source URLs. */
    public static String fingerprint(String raw){
        if(raw==null)return "";
        try{
            byte[] digest=MessageDigest.getInstance("SHA-256")
                .digest(raw.getBytes(StandardCharsets.UTF_8));
            StringBuilder result=new StringBuilder();
            for(byte value:digest)result.append(String.format(Locale.ROOT,"%02x",value&255));
            return result.toString();
        }catch(Exception e){return "";}
    }
    public static boolean isExplicit(String group,String name) {
        return contains(group)||contains(name);
    }
    private static boolean contains(String text) {
        if(text==null||text.isEmpty())return false;
        String normalized=Normalizer.normalize(text,Normalizer.Form.NFKC)
            .toLowerCase(Locale.ROOT).replace('_',' ').replace('-',' ');
        return ADULT.matcher(normalized).find();
    }
}
