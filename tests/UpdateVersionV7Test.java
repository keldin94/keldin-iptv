import com.keldin.iptv.updates.UpdateVersion;
public class UpdateVersionV7Test {
    static void ok(boolean value,String message) {
        if(!value)throw new AssertionError(message);
    }
    public static void main(String[] args) {
        ok(UpdateVersion.compare("v0.7.1","0.7.0")>0,"patch increase");
        ok(UpdateVersion.compare("v0.8.0","0.7.99")>0,"minor increase");
        ok(UpdateVersion.compare("1.0.0","v0.99.99")>0,"major increase");
        ok(UpdateVersion.compare("v0.7.0","0.7.0")==0,"same version");
        ok(UpdateVersion.compare("0.6.9","0.7.0")<0,"older version");
        ok(UpdateVersion.parse("https://example.com") == null,"bad tag rejected");
        ok(UpdateVersion.parse("v0.7.0-preview")!=null,"preview parsed");
        System.out.println("PASS: updater semantic version ordering");
    }
}
