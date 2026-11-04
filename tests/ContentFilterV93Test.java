import com.keldin.iptv.data.ContentFilterV93;
public final class ContentFilterV93Test {
    static void expect(boolean actual,boolean expected,String label){
        if(actual!=expected)throw new AssertionError(label+" expected="+expected+" got="+actual);
    }
    public static void main(String[] args){
        expect(ContentFilterV93.isExplicit("18+ | Germany","Mainstream movie"),true,"18 plus");
        expect(ContentFilterV93.isExplicit("EXYU | XXX","Test channel"),true,"XXX category");
        expect(ContentFilterV93.isExplicit("MOVIES | Erotik","Test"),true,"erotik");
        expect(ContentFilterV93.isExplicit("MOVIES","Erotic Nights"),true,"title based adult");
        expect(ContentFilterV93.isExplicit("US | Films","Sex and the City"),true,"explicit title token");
        expect(ContentFilterV93.isExplicit("Documentary","Modern architecture"),false,"safe category");
        expect(ContentFilterV93.isExplicit("Essex Travel","Essex Museum"),false,"word boundaries");
        expect(ContentFilterV93.isExplicit("Movies","The Adults"),true,"adult marker");
        expect(ContentFilterV93.isExplicit("Movies","Calm Comedy"),false,"non explicit");
        System.out.println("PASS: explicit classification by category and title, with boundary protection");
    }
}
